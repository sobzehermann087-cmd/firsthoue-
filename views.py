from datetime import date, timedelta
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, include, reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg
from django.db import models
from .models import Hotel, Chambre, Reservation, Profil
from .forms import RegisterForm, ChambreForm, HotelForm

def est_chambre_disponible(chambre, date_debut, nuits):
    if chambre.est_hors_service:
        return False
    
    if isinstance(date_debut, str):
        date_debut = date.fromisoformat(date_debut)
    
    date_fin = date_debut + timedelta(days=nuits)
    
    # On cherche les réservations qui chevauchent ces dates
    # On ignore les réservations annulées
    reservations = Reservation.objects.filter(chambre=chambre, est_terminee=False, est_payee=True, est_annulee=False)
    
    for res in reservations:
        res_fin = res.date_arrivee + timedelta(days=res.nuits)
        if date_debut < res_fin and date_fin > res.date_arrivee:
            return False
    return True

def verifier_reservations_terminees():
    """
    Optimise la gestion des statuts de toutes les chambres en une seule passe.
    On ignore les réservations annulées pour le calcul de disponibilité.
    """
    aujourdhui = date.today()
    
    # 1. Identifier et terminer les réservations dont le séjour est fini
    # On ignore les annulées
    reservations_actives = Reservation.objects.filter(
        est_terminee=False,
        est_payee=True,
        est_annulee=False,
        chambre__isnull=False
    )
    
    chambres_a_liberer = []
    for res in reservations_actives:
        if res.date_depart <= aujourdhui:
            res.est_terminee = True
            res.save(update_fields=['est_terminee'])
            if res.chambre_id:
                chambres_a_liberer.append(res.chambre_id)
    
    # 2. Mettre les chambres dont le séjour vient de finir en nettoyage
    if chambres_a_liberer:
        Chambre.objects.filter(id__in=chambres_a_liberer).update(en_nettoyage=True, est_disponible=False)

    # 3. Marquer comme OCCUPÉES toutes les chambres ayant une réservation PAYÉE et NON TERMINÉE
    # On ignore les annulées
    ids_reservees = Reservation.objects.filter(
        est_terminee=False,
        est_payee=True,
        est_annulee=False,
        chambre__isnull=False
    ).values_list('chambre_id', flat=True)
    
    # 4. Mise à jour globale des statuts
    Chambre.objects.filter(est_hors_service=False, en_nettoyage=False).update(est_disponible=True)
    
    Chambre.objects.filter(
        models.Q(id__in=ids_reservees) | 
        models.Q(en_nettoyage=True) | 
        models.Q(est_hors_service=True)
    ).update(est_disponible=False)

def is_admin(user):
    return user.is_authenticated and user.is_staff

def est_gestionnaire(user):
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    profil = getattr(user, 'profil', None)
    return profil and (profil.est_receptionniste or profil.est_gerant) and profil.hotel is not None

@user_passes_test(is_admin)
def ajouter_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Hôtel ajouté avec succès !")
            return redirect('profil')
    else:
        form = HotelForm()
    return render(request, 'ajouter_hotel.html', {'form': form})

@user_passes_test(is_admin)
def supprimer_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.delete()
    messages.success(request, "Hôtel supprimé !")
    return redirect('profil')

def index(request):
    verifier_reservations_terminees()
    hotels_raw = Hotel.objects.annotate(raw_prix_moyen=Avg('chambres__prix'))
    for hotel in hotels_raw:
        if hotel.raw_prix_moyen:
            hotel.prix_moyen = round(hotel.raw_prix_moyen / 1000) * 1000
        else:
            hotel.prix_moyen = hotel.prix_nuit
    return render(request, 'index.html', {'hotels': hotels_raw})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profil.objects.create(user=user)
            login(request, user)
            messages.success(request, "Inscription réussie !")
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'inscription.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Bienvenue, {username} !")
                return redirect('index')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
    else:
        form = AuthenticationForm()
    return render(request, 'connexion.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Vous êtes déconnecté.")
    return redirect('index')

@login_required
def profil(request):
    verifier_reservations_terminees()
    profil_user, created = Profil.objects.get_or_create(user=request.user)
    reservations = []
    hotels = None
    all_users = None
    clients_hotel = None
    stats = {}

    if request.user.is_staff:
        hotels = Hotel.objects.all()
        # On exclut les réservations annulées de la vue d'administration
        reservations = Reservation.objects.filter(est_annulee=False).order_by('-date_creation')
        all_users = User.objects.exclude(is_superuser=True).order_by('username')
        chambres = Chambre.objects.select_related('hotel').all()
        stats = {
            'total_hotels': hotels.count(),
            'total_chambres': chambres.count(),
            'total_reservations': reservations.count(),
            'total_users': all_users.count()
        }
    elif (profil_user.est_receptionniste or profil_user.est_gerant) and profil_user.hotel:
        # On exclut les réservations annulées de la vue de l'hôtel
        reservations = Reservation.objects.filter(chambre__hotel=profil_user.hotel, est_annulee=False).order_by('-date_creation')
        chambres = Chambre.objects.filter(hotel=profil_user.hotel)
        clients_hotel = reservations.values('client_nom').distinct()
        stats = {
            'nom_hotel': profil_user.hotel.nom,
            'total_chambres': chambres.count(),
            'total_reservations': reservations.count(),
            'total_clients': clients_hotel.count()
        }
    else:
        # On exclut les réservations annulées de la vue du client
        reservations = Reservation.objects.filter(
            (models.Q(user=request.user) | models.Q(client_nom=request.user.username)),
            est_annulee=False
        ).order_by('-date_creation')
        chambres = None

    return render(request, 'profil.html', {
        'reservations': reservations,
        'hotels': hotels,
        'all_users': all_users,
        'clients_hotel': clients_hotel,
        'chambres': chambres,
        'stats': stats,
        'profil': profil_user
    })

@user_passes_test(is_admin)
def assigner_receptionniste(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        hotel_id = request.POST.get('hotel_id')
        role = request.POST.get('role', 'receptionniste')
        user_to_update = get_object_or_404(User, id=user_id)
        profil_to_update, _ = Profil.objects.get_or_create(user=user_to_update)
        
        if hotel_id:
            hotel = get_object_or_404(Hotel, id=hotel_id)
            profil_to_update.hotel = hotel
            if role == 'gerant':
                profil_to_update.est_gerant = True
                profil_to_update.est_receptionniste = False
                messages.success(request, f"{user_to_update.username} est maintenant Gérant de {hotel.nom}.")
            else:
                profil_to_update.est_receptionniste = True
                profil_to_update.est_gerant = False
                messages.success(request, f"{user_to_update.username} est maintenant Réceptionniste de {hotel.nom}.")
        else:
            profil_to_update.hotel = None
            profil_to_update.est_receptionniste = False
            profil_to_update.est_gerant = False
            messages.success(request, f"{user_to_update.username} est maintenant un client normal.")
        profil_to_update.save()
    return redirect(f"{reverse('profil')}?tab=users")

@login_required
def stats_rentabilite(request):
    profil_user, _ = Profil.objects.get_or_create(user=request.user)
    if not (request.user.is_staff or profil_user.est_gerant):
        messages.error(request, "Accès réservé aux gérants et administrateurs.")
        return redirect('profil')
    
    # Si c'est un gérant, on filtre par son hôtel
    # Si c'est un admin, on peut voir tous les hôtels (ou filtrer par hôtel passé en paramètre)
    hotel_id = request.GET.get('hotel_id')
    hotel_selectionne = None
    
    if request.user.is_staff:
        if hotel_id:
            hotel_selectionne = get_object_or_404(Hotel, id=hotel_id)
        hotels = Hotel.objects.all()
    else:
        hotel_selectionne = profil_user.hotel
        hotels = [hotel_selectionne] if hotel_selectionne else []

    data_rentabilite = []
    labels_mois = []
    
    if hotel_selectionne:
        # Calcul de la rentabilité sur les 6 derniers mois
        aujourdhui = date.today()
        for i in range(5, -1, -1):
            premier_jour_mois = (aujourdhui.replace(day=1) - timedelta(days=i*30)).replace(day=1)
            dernier_jour_mois = (premier_jour_mois + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            reservations_mois = Reservation.objects.filter(
                chambre__hotel=hotel_selectionne,
                date_arrivee__range=[premier_jour_mois, dernier_jour_mois]
            )
            
            CA = 0
            for res in reservations_mois:
                if res.chambre:
                    CA += res.chambre.prix * res.nuits
            
            data_rentabilite.append(CA)
            labels_mois.append(premier_jour_mois.strftime("%B %Y"))

    return render(request, 'stats_rentabilite.html', {
        'hotel_selectionne': hotel_selectionne,
        'hotels': hotels,
        'data_rentabilite': data_rentabilite,
        'labels_mois': labels_mois,
        'zip_data': zip(labels_mois, data_rentabilite),
        'profil': profil_user
    })

@user_passes_test(est_gestionnaire)
def ajouter_chambre(request):
    profil_user = getattr(request.user, 'profil', None)
    if request.method == 'POST':
        form = ChambreForm(request.POST, request.FILES)
        if form.is_valid():
            chambre = form.save(commit=False)
            if not request.user.is_staff and profil_user and profil_user.hotel:
                chambre.hotel = profil_user.hotel
            chambre.save()
            messages.success(request, f"Chambre ajoutée avec succès !")
            return redirect('profil')
    else:
        form = ChambreForm()
        if not request.user.is_staff and profil_user and profil_user.hotel:
            form.fields['hotel'].initial = profil_user.hotel
            form.fields['hotel'].widget.attrs['readonly'] = True
    return render(request, 'ajouter_chambre.html', {'form': form})

@user_passes_test(est_gestionnaire)
def supprimer_chambre(request, chambre_id):
    chambre = get_object_or_404(Chambre, id=chambre_id)
    profil_user = getattr(request.user, 'profil', None)
    autorise = False
    if request.user.is_staff:
        autorise = True
    elif profil_user and (profil_user.est_receptionniste or profil_user.est_gerant) and chambre.hotel == profil_user.hotel:
        autorise = True
    
    if autorise:
        chambre.delete()
        messages.success(request, "Chambre supprimée !")
    else:
        messages.error(request, "Action non autorisée.")
    return redirect('profil')

@login_required
def supprimer_reservation(request, res_id):
    reservation = get_object_or_404(Reservation, id=res_id)
    profil_user, _ = Profil.objects.get_or_create(user=request.user)
    autorise = False
    if request.user.is_staff:
        autorise = True
    elif (profil_user.est_receptionniste or profil_user.est_gerant) and reservation.chambre and reservation.chambre.hotel == profil_user.hotel:
        autorise = True

    if autorise:
        if reservation.chambre:
            reservation.chambre.en_nettoyage = True
            reservation.chambre.est_disponible = False
            reservation.chambre.save()
        
        # On ne supprime plus physiquement la réservation pour garder le CA dans les stats
        reservation.est_annulee = True
        reservation.save()
        
        messages.success(request, "Réservation annulée. La chambre est en cours de nettoyage, mais le revenu est conservé dans les statistiques.")
    else:
        messages.error(request, "Action non autorisée.")
    return redirect('profil')

@user_passes_test(est_gestionnaire)
def finir_nettoyage(request, chambre_id):
    chambre = get_object_or_404(Chambre, id=chambre_id)
    profil_user = getattr(request.user, 'profil', None)
    autorise = False
    if request.user.is_staff:
        autorise = True
    elif profil_user and (profil_user.est_receptionniste or profil_user.est_gerant) and chambre.hotel == profil_user.hotel:
        autorise = True
    
    if autorise:
        chambre.en_nettoyage = False
        chambre.est_disponible = True
        chambre.save()
        messages.success(request, f"La chambre {chambre.categorie} est à nouveau disponible !")
    else:
        messages.error(request, "Action non autorisée.")
    return redirect(f"{reverse('profil')}?tab=rooms")

@user_passes_test(est_gestionnaire)
def basculer_hors_service(request, chambre_id):
    chambre = get_object_or_404(Chambre, id=chambre_id)
    profil_user = getattr(request.user, 'profil', None)
    autorise = False
    
    if request.user.is_staff:
        autorise = True
    elif profil_user and (profil_user.est_receptionniste or profil_user.est_gerant) and chambre.hotel == profil_user.hotel:
        autorise = True
        
    if autorise:
        chambre.est_hors_service = not chambre.est_hors_service
        # Si on met hors service, on rend indisponible
        if chambre.est_hors_service:
            chambre.est_disponible = False
        else:
            # Si on réactive, elle redevient disponible (si elle n'est pas déjà occupée)
            chambre.est_disponible = True
            
        chambre.save()
        status = "mise hors service" if chambre.est_hors_service else "remise en service"
        messages.success(request, f"La chambre {chambre.categorie} a été {status}.")
    else:
        messages.error(request, "Action non autorisée.")
        
    return redirect(f"{reverse('profil')}?tab=rooms")

def hotel_reservation(request, hotel_id):
    verifier_reservations_terminees() # Mise à jour avant affichage
    hotel = get_object_or_404(Hotel, id=hotel_id)
    chambres = hotel.chambres.all()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"{reverse('connexion')}?next={request.path}")
        client_nom = request.POST.get('nom') or request.user.username
        chambre_id = request.POST.get('chambre_id')
        date_arrivee_str = request.POST.get('date_arrivee')
        nuits = int(request.POST.get('nuits', 1))

        date_arrivee = date.fromisoformat(date_arrivee_str)
        if date_arrivee < date.today():
            messages.error(request, "La date d'arrivée ne peut pas être dans le passé.")
            return redirect(request.path)

        chambre = get_object_or_404(Chambre, id=chambre_id)
        
        # Vérification de disponibilité réelle
        if not est_chambre_disponible(chambre, date_arrivee, nuits):
            messages.error(request, "Désolé, cette chambre est déjà réservée pour les dates choisies.")
            return redirect(request.path)
        
        # On stocke tout en session au lieu de créer en base de données
        request.session['pending_res'] = {
            'client_nom': client_nom,
            'chambre_id': chambre.id,
            'hotel_nom': hotel.nom,
            'chambre_type': chambre.categorie,
            'date_arrivee': date_arrivee_str,
            'nuits': nuits,
            'prix_total': chambre.prix * nuits
        }
        
        request.session['total_reservation'] = chambre.prix * nuits
        request.session['hotel_name'] = hotel.nom
        
        return redirect('payement')
    return render(request, 'hotel_reservation.html', {'hotel': hotel, 'chambres': chambres})

def reservation(request):
    verifier_reservations_terminees() # Mise à jour avant affichage
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"{reverse('connexion')}?next={request.path}")
        chambre_id = request.POST.get('chambre_id')
        date_arrivee_str = request.POST.get('date_arrivee')
        nuits = int(request.POST.get('nuits', 1))

        date_arrivee = date.fromisoformat(date_arrivee_str)
        if date_arrivee < date.today():
            messages.error(request, "La date d'arrivée ne peut pas être dans le passé.")
            return redirect(request.path)

        chambre = get_object_or_404(Chambre, id=chambre_id)
        
        # Vérification de disponibilité réelle
        if not est_chambre_disponible(chambre, date_arrivee, nuits):
            messages.error(request, "Désolé, cette chambre est déjà réservée pour les dates choisies.")
            return redirect(request.path)
        
        # Stockage en session
        request.session['pending_res'] = {
            'client_nom': request.user.username,
            'chambre_id': chambre.id,
            'hotel_nom': chambre.hotel.nom,
            'chambre_type': chambre.categorie,
            'date_arrivee': date_arrivee_str,
            'nuits': nuits,
            'prix_total': chambre.prix * nuits
        }
        
        request.session['total_reservation'] = chambre.prix * nuits
        request.session['hotel_name'] = chambre.hotel.nom
        
        return redirect('payement')
    chambres = Chambre.objects.select_related('hotel').all()
    return render(request, 'reservation.html', {'chambres': chambres})

@login_required
def valider_paiement(request):
    pending_res = request.session.get('pending_res')
    if not pending_res:
        messages.error(request, "Aucune réservation en attente de paiement.")
        return redirect('profil')
    
    chambre = get_object_or_404(Chambre, id=pending_res['chambre_id'])
    
    # On vérifie si la chambre est toujours disponible au moment du paiement
    if not est_chambre_disponible(chambre, pending_res['date_arrivee'], pending_res['nuits']):
        messages.error(request, "Désolé, cette chambre vient d'être réservée par quelqu'un d'autre.")
        return redirect('index')

    # Création réelle de la réservation SEULEMENT MAINTENANT
    res = Reservation.objects.create(
        user=request.user,
        client_nom=pending_res['client_nom'],
        chambre=chambre,
        hotel=pending_res['hotel_nom'],
        chambre_type=pending_res['chambre_type'],
        date_arrivee=pending_res['date_arrivee'],
        nuits=pending_res['nuits'],
        est_payee=True
    )
    
    # Mise à jour automatique des statuts de disponibilité
    verifier_reservations_terminees()
    
    # Nettoyage de la session
    del request.session['pending_res']
    
    messages.success(request, "Votre paiement a été validé et votre réservation est confirmée !")
    return redirect('profil')

def payement(request):
    res_id = request.session.get('last_res_id')
    return render(request, 'payement.html', {
        'total': request.session.get('total_reservation', 0), 
        'hotel_nom': request.session.get('hotel_name', "hôtel"),
        'res_id': res_id
    })

@login_required
def certificat_reservation(request, res_id):
    reservation = get_object_or_404(Reservation, id=res_id)
    # Vérification : seul le client de la résa ou l'admin ou le réceptionniste de l'hôtel peut voir le certificat
    profil_user, _ = Profil.objects.get_or_create(user=request.user)
    autorise = False
    if request.user.is_staff or reservation.user == request.user or reservation.client_nom == request.user.username:
        autorise = True
    elif (profil_user.est_receptionniste or profil_user.est_gerant) and reservation.chambre and reservation.chambre.hotel == profil_user.hotel:
        autorise = True
    
    if not autorise:
        messages.error(request, "Accès non autorisé au certificat.")
        return redirect('profil')
        
    return render(request, 'certificat.html', {'res': reservation})

@user_passes_test(is_admin)
def supprimer_utilisateur(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    if user_to_delete.is_superuser:
        messages.error(request, "Impossible de supprimer un super-utilisateur.")
    elif user_to_delete == request.user:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte ici.")
    else:
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f"L'utilisateur {username} a été supprimé.")
    return redirect('profil')

def carte(request):
    return render(request, 'carte.html', {'hotels': Hotel.objects.all()})

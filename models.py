from django.db import models

class Hotel(models.Model):
    nom = models.CharField(max_length=200)
    region = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    prix_nuit = models.IntegerField()
    confort = models.CharField(max_length=50)
    image_url = models.ImageField(upload_to='hotels/')  # Image principale (Bâtiment)
    image_reception = models.ImageField(upload_to='hotels/', null=True, blank=True)
    image_resto = models.ImageField(upload_to='hotels/', null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.nom} - {self.ville}"

    @property
    def est_mensuel(self):
        return "hôtel" not in self.nom.lower() and "hotel" not in self.nom.lower()

class Chambre(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='chambres', on_delete=models.CASCADE)
    numero = models.CharField(max_length=10, verbose_name="N° de chambre", null=True, blank=True)
    categorie = models.CharField(max_length=100)
    prix = models.IntegerField()
    description = models.TextField()
    image_url = models.ImageField(upload_to='chambres/')  # Image principale (Chambre)
    image_salon = models.ImageField(upload_to='chambres/', null=True, blank=True)
    image_douche = models.ImageField(upload_to='chambres/', null=True, blank=True)
    est_disponible = models.BooleanField(default=True)
    en_nettoyage = models.BooleanField(default=False)
    est_hors_service = models.BooleanField(default=False)

    def __str__(self):
        return f"Chambre {self.numero} ({self.categorie}) - {self.hotel.nom}"

class Profil(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profil')
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    est_receptionniste = models.BooleanField(default=False)
    est_gerant = models.BooleanField(default=False)

    def __str__(self):
        return f"Profil de {self.user.username}"

class Reservation(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    client_nom = models.CharField(max_length=200)
    chambre = models.ForeignKey(Chambre, on_delete=models.SET_NULL, null=True, related_name='reservations_set')
    hotel = models.CharField(max_length=200)
    chambre_type = models.CharField(max_length=200)
    date_arrivee = models.DateField()
    nuits = models.IntegerField()
    date_creation = models.DateTimeField(auto_now_add=True)
    est_payee = models.BooleanField(default=False)
    est_terminee = models.BooleanField(default=False)
    est_annulee = models.BooleanField(default=False)

    def __str__(self):
        return f"Réservation de {self.client_nom} - {self.hotel}"

    @property
    def date_depart(self):
        from datetime import timedelta
        return self.date_arrivee + timedelta(days=self.nuits)

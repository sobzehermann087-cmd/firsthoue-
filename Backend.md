# Logique Backend (Vues et Routes)

Le fichier `backend/hotels/views.py` contient toute la logique métier du projet. Voici comment les différentes fonctions sont organisées :

## 1. Gestion de l'Authentification
Django possède son propre système d'utilisateurs. Les fonctions suivantes sont utilisées :
- `register` : Permet l'inscription d'un nouvel utilisateur.
- `login_view` : Permet la connexion des utilisateurs.
- `logout_view` : Permet la déconnexion en toute sécurité.

## 2. Affichage des Hôtels et Réservations
- `index` : La page d'accueil affiche les hôtels disponibles.
- `carte` : Permet de voir les hôtels géographiquement (grâce aux latitudes et longitudes).
- `hotel_reservation` : Affiche les chambres disponibles pour un hôtel spécifique et permet au client de choisir sa chambre.

## 3. Gestion des Réservations et Paiements
- `reservation` : Affiche toutes les réservations d'un utilisateur.
- `payement` : Gère le processus de paiement (simulation de paiement).
- `certificat_reservation` : Génère un reçu ou certificat après une réservation réussie.

## 4. Espace Administration (Hôtels/Chambres)
Ces fonctions permettent de gérer les données sans passer par l'interface d'administration par défaut de Django :
- `ajouter_hotel` / `supprimer_hotel`
- `ajouter_chambre` / `supprimer_chambre`
- `supprimer_utilisateur` / `supprimer_reservation`

## 5. Gestion de l'État des Chambres (Spécifique aux Réceptionnistes)
Les réceptionnistes peuvent changer l'état des chambres en un clic :
- `finir_nettoyage` : Marque une chambre comme prête après son entretien.
- `basculer_hors_service` : Met une chambre en maintenance si nécessaire.

### Routes (URLs)
Toutes ces fonctions sont reliées à des adresses Web dans `backend/config/urls.py`. Par exemple :
- `/admin/` : Administration Django.
- `/carte/` : Page de la carte.
- `/profil/` : Page de profil de l'utilisateur.

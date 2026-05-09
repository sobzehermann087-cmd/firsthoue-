# Interface Utilisateur (Frontend)

L'interface du projet est construite avec des templates Django (`.html`) qui sont transformés dynamiquement avant d'être envoyés au navigateur.

## 1. Modèle de Base (`base.html`)
Ce fichier contient la structure commune à toutes les pages (en-tête, pied de page, liens de navigation). Les autres pages "héritent" de ce fichier pour éviter de répéter le code.

## 2. Pages Clients (Utilisateurs)
- `index.html` : La page d'accueil avec la liste des hôtels.
- `carte.html` : Utilise probablement une bibliothèque (comme Leaflet ou Google Maps) pour afficher les hôtels sur une carte.
- `hotel_reservation.html` : Affiche les détails d'un hôtel et les types de chambres.
- `payement.html` : Formulaire de paiement sécurisé (simulation).
- `certificat.html` : Page de confirmation générée après une réservation.

## 3. Gestion du Compte
- `connexion.html` / `inscription.html` : Formulaires pour l'accès utilisateur.
- `profil.html` : Page centrale pour l'utilisateur. Elle change radicalement selon le rôle :
    - **Client :** Voit ses réservations passées et en cours.
    - **Réceptionniste :** Voit le tableau de bord de son hôtel (état des chambres, nettoyage).
    - **Admin :** Voit les statistiques globales et les outils de gestion.

## 4. Outils d'Administration
- `ajouter_hotel.html` / `ajouter_chambre.html` : Formulaires simplifiés pour l'ajout de nouvelles données.

## 5. Ressources Statiques (`static/`)
- **CSS :** Définit les couleurs, les polices et la disposition (layout).
- **JavaScript :** Gère les interactions dynamiques, comme la carte interactive ou les confirmations de suppression.
- **Images :** Stockage local des logos ou photos d'hôtels.

# Modèles de Données (Base de Données)

Le fichier `backend/hotels/models.py` définit les tables de la base de données. Voici une explication de chaque modèle :

## 1. Modèle `Hotel`
C'est la base du système. Il stocke les informations sur chaque établissement.
- **Champs importants :** Nom, Région, Ville, Prix par nuit, Confort (étoiles), Images (principale, réception, resto), Coordonnées GPS (Latitude, Longitude).
- **Fonction `est_mensuel` :** Une propriété qui identifie si l'établissement est un hôtel classique ou une résidence mensuelle.

## 2. Modèle `Chambre`
Chaque hôtel possède plusieurs chambres.
- **Relation :** Lié à `Hotel` par une **ForeignKey** (Clé Étrangère). Si un hôtel est supprimé, ses chambres le sont aussi (`CASCADE`).
- **Champs importants :** Catégorie (Luxe, Simple, etc.), Prix, État de disponibilité (`est_disponible`), État de nettoyage (`en_nettoyage`).

## 3. Modèle `Profil`
C'est une extension de l'utilisateur standard de Django (`User`).
- **Rôles :** Permet de savoir si un utilisateur est un client classique ou un **réceptionniste**.
- **Relation :** Lié à un `Hotel` spécifique pour les réceptionnistes (chaque réceptionniste gère un hôtel).

## 4. Modèle `Reservation`
Enregistre les détails de chaque séjour réservé.
- **Champs importants :** Utilisateur, Nom du client, Chambre, Date d'arrivée, Nombre de nuits.
- **Statut :** `est_terminee` permet de savoir si le séjour est achevé.

### Schéma Relationnel
Un **Hôtel** contient plusieurs **Chambres**. Un **Utilisateur** (via son **Profil**) peut être lié à un hôtel comme réceptionniste et peut effectuer plusieurs **Réservations** de **Chambres**.

# Scripts Utilitaires

Le projet inclut des scripts pour faciliter l'installation, le démarrage et la gestion initiale des données.

## 1. `Lancer_FirstHoue.bat` (Fichier de commande Windows)
Ce script automatise les étapes de lancement du projet en un seul clic :
- **Activation :** Active l'environnement virtuel Python (`venv`).
- **Migrations :** Met à jour la structure de la base de données (`makemigrations` et `migrate`).
- **Serveur :** Lance le serveur de développement Django sur le port `8000`.
- **Navigation :** Ouvre automatiquement votre navigateur Web à l'adresse `http://127.0.0.1:8000/`.

## 2. `setup_admin.py` (Configuration de l'administrateur)
Ce script Python permet de configurer rapidement l'accès administrateur principal :
- **Utilisateur :** Crée ou met à jour l'utilisateur `hermann` avec les droits de super-utilisateur (`is_superuser`).
- **Sécurité :** Réinitialise le mot de passe (`Tsafack1`).
- **Nettoyage :** Rétrograde automatiquement les autres administrateurs en simples clients pour éviter les conflits d'accès lors des présentations.

## 3. `backend/seed_data.py` (Données de démonstration)
Ce script est utilisé pour remplir la base de données avec des exemples concrets d'hôtels, de chambres et de réservations.
- **Utilité :** Très important lors du premier déploiement du projet ou après une réinitialisation de la base de données, pour ne pas avoir un site vide.

## 4. `backend/manage.py` (L'outil central de Django)
C'est le fichier standard de Django pour toutes les opérations de gestion :
- `python manage.py createsuperuser` : Créer un nouvel administrateur manuellement.
- `python manage.py runserver` : Lancer le serveur manuellement.
- `python manage.py shell` : Accéder à la console Python liée à la base de données.

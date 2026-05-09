# Architecture Globale du Projet

Le projet suit le modèle architectural **MVT (Model-View-Template)**, qui est le standard utilisé par le framework Django.

## Technologies Utilisées

- **Backend :** Django (Python) - Gère la logique métier, la base de données et les routes.
- **Frontend :** HTML5, CSS3, JavaScript (Vanilla) - Gère l'affichage et l'interactivité côté client.
- **Base de Données :** SQLite3 - Système de gestion de base de données relationnelle léger et facile à déployer.

## Organisation des Fichiers

```text
prot-BTS/
├── backend/                # Racine du projet Django
│   ├── config/             # Configuration globale (settings, urls)
│   ├── hotels/             # Application principale (modèles, vues)
│   ├── db.sqlite3          # Fichier de la base de données
│   └── manage.py           # Point d'entrée des commandes Django
├── frontend/               # Contenu visuel
│   ├── templates/          # Fichiers HTML (structure)
│   └── static/             # CSS, Images, JS (style et scripts)
├── venv/                   # Environnement virtuel Python (dépendances)
├── Lancer_FirstHoue.bat    # Script pour lancer le serveur facilement
└── setup_admin.py          # Script de configuration initiale
```

### Avantages de cette structure
Cette séparation permet de bien distinguer ce qui relève de l'affichage (frontend) de ce qui relève du stockage et du traitement des données (backend).

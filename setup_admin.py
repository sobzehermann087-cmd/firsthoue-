import os
import django

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

def setup_single_admin():
    username = "hermann"
    password = "Tsafack1"
    
    # 1. Créer ou mettre à jour l'admin hermann
    user, created = User.objects.get_or_create(username=username)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    
    if created:
        print(f"Succès : L'utilisateur '{username}' a été créé.")
    else:
        print(f"Succès : L'utilisateur '{username}' a été mis à jour.")
        
    # 2. Rétrograder tous les autres admins pour éviter les conflits
    others = User.objects.filter(is_staff=True).exclude(username=username)
    count = 0
    for other in others:
        other.is_staff = False
        other.is_superuser = False
        other.save()
        count += 1
    
    if count > 0:
        print(f"Succès : {count} autre(s) admin(s) ont été rétrogradé(s) en simples clients.")
    else:
        print("Aucun autre admin n'a été trouvé.")

if __name__ == "__main__":
    setup_single_admin()

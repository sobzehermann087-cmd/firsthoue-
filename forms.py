from django import forms
from django.contrib.auth.models import User
from .models import Chambre, Hotel

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Adresse électronique")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmez le mot de passe")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse électronique est déjà utilisée.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username').strip() # Retire les espaces
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(f"Le nom '{username}' est déjà utilisé (même en minuscules/majuscules).")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Les deux mots de passe ne sont pas identiques.")
        return cleaned_data

class HotelForm(forms.ModelForm):
    REGION_CHOICES = [
        ('Adamaoua', 'Adamaoua'),
        ('Centre', 'Centre'),
        ('Est', 'Est'),
        ('Extrême-Nord', 'Extrême-Nord'),
        ('Littoral', 'Littoral'),
        ('Nord', 'Nord'),
        ('Nord-Ouest', 'Nord-Ouest'),
        ('Ouest', 'Ouest'),
        ('Sud', 'Sud'),
        ('Sud-Ouest', 'Sud-Ouest'),
    ]

    CONFORT_CHOICES = [
        ('1 Étoile', '1 Étoile'),
        ('2 Étoiles', '2 Étoiles'),
        ('3 Étoiles', '3 Étoiles'),
        ('4 Étoiles', '4 Étoiles'),
        ('5 Étoiles', '5 Étoiles'),
        ('Luxe', 'Luxe'),
    ]

    region = forms.ChoiceField(choices=REGION_CHOICES, widget=forms.Select(attrs={'class': 'custom-input'}))
    confort = forms.ChoiceField(choices=CONFORT_CHOICES, widget=forms.Select(attrs={'class': 'custom-input'}))

    class Meta:
        model = Hotel
        fields = [
            'nom', 'region', 'ville', 'prix_nuit', 'confort', 
            'image_url', 'image_reception', 'image_resto', 
            'latitude', 'longitude'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Nom de l\'hôtel'}),
            'ville': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Ville (ex: Douala)'}),
            'prix_nuit': forms.NumberInput(attrs={'class': 'custom-input', 'placeholder': 'Prix moyen par nuit'}),
            'image_url': forms.ClearableFileInput(attrs={'class': 'custom-input'}),
            'image_reception': forms.ClearableFileInput(attrs={'class': 'custom-input'}),
            'image_resto': forms.ClearableFileInput(attrs={'class': 'custom-input'}),
            'latitude': forms.NumberInput(attrs={'class': 'custom-input', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'custom-input', 'step': '0.000001'}),
        }

class ChambreForm(forms.ModelForm):
    CATEGORIES = [
        ('Standard', 'Standard'),
        ('Studio', 'Studio'),
        ('Supérieure', 'Supérieure'),
        ('Deluxe', 'Deluxe'),
        ('Chambre Familiale', 'Chambre Familiale'),
        ('Suite Junior', 'Suite Junior'),
        ('Suite Executive', 'Suite Executive'),
        ('Suite Présidentielle', 'Suite Présidentielle'),
    ]
    
    PRIX_CHOICES = [
        (25000, '25 000 FCFA'),
        (30000, '30 000 FCFA'),
        (35000, '35 000 FCFA'),
        (40000, '40 000 FCFA'),
        (45000, '45 000 FCFA'),
        (50000, '50 000 FCFA'),
        (60000, '60 000 FCFA'),
        (70000, '70 000 FCFA'),
    ]

    categorie = forms.ChoiceField(choices=CATEGORIES, widget=forms.Select(attrs={'class': 'custom-input'}))
    prix = forms.ChoiceField(choices=PRIX_CHOICES, widget=forms.Select(attrs={'class': 'custom-input'}))

    class Meta:
        model = Chambre
        fields = ['hotel', 'numero', 'categorie', 'prix', 'description', 'image_url', 'image_salon', 'image_douche', 'est_disponible', 'en_nettoyage']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Ex: 101, B-12...'}),
            'image_url': forms.ClearableFileInput(attrs={'class': 'custom-input'}),
            'image_salon': forms.ClearableFileInput(attrs={'class': 'custom-input'}),
            'image_douche': forms.ClearableFileInput(attrs={'class': 'custom-input'}),
        }

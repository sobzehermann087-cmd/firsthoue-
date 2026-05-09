from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Hotel, Chambre, Reservation, Profil

class ProfilInline(admin.StackedInline):
    model = Profil
    can_delete = False
    verbose_name_plural = 'profil'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfilInline,)

# Ré-enregistrer UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('nom', 'region', 'ville', 'prix_nuit', 'confort')

@admin.register(Chambre)
class ChambreAdmin(admin.ModelAdmin):
    list_display = ('numero', 'categorie', 'hotel', 'prix', 'est_disponible')
    search_fields = ('numero', 'categorie', 'hotel__nom')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('client_nom', 'hotel', 'chambre_type', 'date_arrivee', 'date_creation')
    list_filter = ('hotel', 'date_arrivee')
    search_fields = ('client_nom', 'hotel')

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'est_receptionniste', 'est_gerant')
    list_filter = ('est_receptionniste', 'est_gerant', 'hotel')

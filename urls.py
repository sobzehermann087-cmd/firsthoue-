from django.contrib import admin
from django.urls import path, include
from hotels import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('carte/', views.carte, name='carte'),
    path('reservation/', views.reservation, name='reservation'),
    path('reservation/<int:hotel_id>/', views.hotel_reservation, name='hotel_reservation'),
    path('payement/', views.payement, name='payement'),
    path('valider-paiement/', views.valider_paiement, name='valider_paiement'),
    path('inscription/', views.register, name='inscription'),
    path('connexion/', views.login_view, name='connexion'),
    path('deconnexion/', views.logout_view, name='deconnexion'),
    path('profil/', views.profil, name='profil'),
    path('ajouter-hotel/', views.ajouter_hotel, name='ajouter_hotel'),
    path('supprimer-hotel/<int:hotel_id>/', views.supprimer_hotel, name='supprimer_hotel'),
    path('ajouter-chambre/', views.ajouter_chambre, name='ajouter_chambre'),
    path('supprimer-chambre/<int:chambre_id>/', views.supprimer_chambre, name='supprimer_chambre'),
    path('supprimer-utilisateur/<int:user_id>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    path('supprimer-reservation/<int:res_id>/', views.supprimer_reservation, name='supprimer_reservation'),
    path('finir-nettoyage/<int:chambre_id>/', views.finir_nettoyage, name='finir_nettoyage'),
    path('basculer-hors-service/<int:chambre_id>/', views.basculer_hors_service, name='basculer_hors_service'),
    path('assigner-receptionniste/', views.assigner_receptionniste, name='assigner_receptionniste'),
    path('stats-rentabilite/', views.stats_rentabilite, name='stats_rentabilite'),
    path('certificat-reservation/<int:res_id>/', views.certificat_reservation, name='certificat_reservation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

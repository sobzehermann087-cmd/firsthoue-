import os
import django
import random

# 1. Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# 2. Importer les modèles
from hotels.models import Hotel, Chambre

def seed_data():
    # 3. Supprimer les données existantes
    print("Suppression des anciennes données...")
    Chambre.objects.all().delete()
    Hotel.objects.all().delete()

    # 4. & 5. Liste des hôtels par région (10 par région = 100 hôtels)
    # Données: (Nom, Ville, Prix_Nuit_Base, Confort, Lat, Lon)
    regions_hotels = {
        'Adamaoua': [
            ('Hôtel Transcam', 'Ngaoundéré', 35000, '3 étoiles', 7.3214, 13.5824),
            ('Hôtel de la Vina', 'Ngaoundéré', 25000, '2 étoiles', 7.3250, 13.5850),
            ('Relais St Hubert', 'Ngaoundéré', 45000, '3 étoiles', 7.3180, 13.5790),
            ('Hôtel du Rail', 'Ngaoundéré', 20000, '2 étoiles', 7.3300, 13.5900),
            ('Mansel Hôtel', 'Ngaoundéré', 40000, '3 étoiles', 7.3150, 13.5750),
            ('Hôtel Marhaba', 'Ngaoundéré', 30000, '2 étoiles', 7.3220, 13.5810),
            ('Hôtel de l\'Adamaoua', 'Ngaoundéré', 28000, '2 étoiles', 7.3260, 13.5880),
            ('Hôtel Plateau', 'Ngaoundéré', 22000, '2 étoiles', 7.3280, 13.5840),
            ('Hôtel Emeraude', 'Ngaoundéré', 32000, '3 étoiles', 7.3200, 13.5800),
            ('Meiganga Palace', 'Meiganga', 18000, '1 étoile', 6.5167, 14.3000),
        ],
        'Centre': [
            ('Hilton Yaoundé', 'Yaoundé', 115000, '5 étoiles', 3.8667, 11.5167),
            ('Hôtel Mont Fébé', 'Yaoundé', 85000, '4 étoiles', 3.9000, 11.5000),
            ('Djeuga Palace', 'Yaoundé', 90000, '4 étoiles', 3.8640, 11.5140),
            ('Hôtel Franco', 'Yaoundé', 70000, '3 étoiles', 3.8600, 11.5100),
            ('La Falaise Yaoundé', 'Yaoundé', 100000, '4 étoiles', 3.8680, 11.5180),
            ('Hôtel Safyad', 'Yaoundé', 45000, '3 étoiles', 3.8500, 11.5200),
            ('Hôtel Merina', 'Yaoundé', 65000, '3 étoiles', 3.8650, 11.5150),
            ('Hôtel Azur', 'Yaoundé', 55000, '3 étoiles', 3.8700, 11.5250),
            ('Hôtel des Députés', 'Yaoundé', 40000, '2 étoiles', 3.8620, 11.5120),
            ('Hôtel Somatel', 'Yaoundé', 50000, '3 étoiles', 3.8550, 11.5050),
        ],
        'Est': [
            ('Hôtel Mansa', 'Bertoua', 40000, '3 étoiles', 4.5773, 13.6848),
            ('Hôtel Teerenstra', 'Bertoua', 30000, '2 étoiles', 4.5800, 13.6900),
            ('Hôtel de l\'Est', 'Bertoua', 25000, '2 étoiles', 4.5750, 13.6800),
            ('Palace Hôtel Bertoua', 'Bertoua', 45000, '3 étoiles', 4.5700, 13.6750),
            ('Hôtel Prestige', 'Bertoua', 35000, '2 étoiles', 4.5850, 13.7000),
            ('Hôtel El Dorado', 'Bertoua', 28000, '2 étoiles', 4.5720, 13.6820),
            ('Hôtel Batouri', 'Batouri', 20000, '1 étoile', 4.4333, 14.3667),
            ('Hôtel Abong-Mbang', 'Abong-Mbang', 18000, '1 étoile', 3.9833, 13.1833),
            ('Hôtel de la Paix', 'Bertoua', 22000, '2 étoiles', 4.5780, 13.6870),
            ('Hôtel Oasis', 'Bertoua', 26000, '2 étoiles', 4.5740, 13.6830),
        ],
        'Extrême-Nord': [
            ('Hôtel Zinini', 'Maroua', 35000, '3 étoiles', 10.5916, 14.3159),
            ('Hôtel Mizao', 'Maroua', 45000, '3 étoiles', 10.5950, 14.3200),
            ('Hôtel Le Sahel', 'Maroua', 25000, '2 étoiles', 10.5900, 14.3100),
            ('Maroua Palace', 'Maroua', 55000, '3 étoiles', 10.5850, 14.3050),
            ('Hôtel Porte-Mayo', 'Maroua', 30000, '2 étoiles', 10.5980, 14.3250),
            ('Hôtel de l\'Aéroport', 'Maroua', 40000, '3 étoiles', 10.4500, 14.2500),
            ('Hôtel Le Saré', 'Maroua', 32000, '2 étoiles', 10.5920, 14.3180),
            ('Campement de Waza', 'Waza', 50000, '3 étoiles', 11.4167, 14.5667),
            ('Hôtel de la Frontière', 'Kousseri', 20000, '1 étoile', 12.0667, 15.0333),
            ('Hôtel Mokolo', 'Mokolo', 15000, '1 étoile', 10.7410, 13.8020),
        ],
        'Littoral': [
            ('Hôtel Sawa', 'Douala', 100000, '4 étoiles', 4.0435, 9.6896),
            ('Pullman Douala Rabingha', 'Douala', 120000, '5 étoiles', 4.0450, 9.6850),
            ('Akwa Palace', 'Douala', 95000, '4 étoiles', 4.0480, 9.6950),
            ('Star Land Hôtel', 'Douala', 80000, '4 étoiles', 4.0550, 9.7100),
            ('Résidence La Falaise', 'Douala', 90000, '4 étoiles', 4.0420, 9.6880),
            ('Onomo Hôtel Douala', 'Douala', 75000, '3 étoiles', 4.0400, 9.6800),
            ('Ibis Douala', 'Douala', 70000, '3 étoiles', 4.0410, 9.6920),
            ('Best Western Plus', 'Douala', 110000, '4 étoiles', 4.0350, 9.7000),
            ('Hôtel de l\'Air', 'Douala', 40000, '2 étoiles', 4.0050, 9.7200),
            ('Prince de Galles', 'Douala', 55000, '3 étoiles', 4.0470, 9.6980),
        ],
        'Nord': [
            ('Hôtel Benoué', 'Garoua', 45000, '3 étoiles', 9.3034, 13.3924),
            ('Relais St Hubert Garoua', 'Garoua', 40000, '3 étoiles', 9.3050, 13.3950),
            ('Hôtel du Plateau', 'Garoua', 30000, '2 étoiles', 9.3100, 13.4000),
            ('Hôtel de l\'Etoile', 'Garoua', 25000, '2 étoiles', 9.3000, 13.3900),
            ('Hôtel Shalom', 'Garoua', 28000, '2 étoiles', 9.3020, 13.3910),
            ('Hôtel Ribadou', 'Garoua', 35000, '2 étoiles', 9.3080, 13.3980),
            ('Hôtel Touristique', 'Garoua', 32000, '2 étoiles', 9.3060, 13.3960),
            ('Hôtel de la Ville', 'Garoua', 20000, '1 étoile', 9.3010, 13.3930),
            ('Hôtel Guider', 'Guider', 18000, '1 étoile', 9.9333, 13.9500),
            ('Hôtel Poli', 'Poli', 15000, '1 étoile', 8.4833, 13.2333),
        ],
        'Nord-Ouest': [
            ('Ayaba Hôtel', 'Bamenda', 55000, '3 étoiles', 5.9631, 10.1591),
            ('Mawa Hôtel', 'Bamenda', 45000, '3 étoiles', 5.9650, 10.1650),
            ('Azam Hôtel', 'Bamenda', 40000, '3 étoiles', 5.9600, 10.1550),
            ('Skyline Hôtel', 'Bamenda', 35000, '2 étoiles', 5.9700, 10.1700),
            ('Pelican Hôtel', 'Bamenda', 30000, '2 étoiles', 5.9550, 10.1500),
            ('Victory Hôtel', 'Bamenda', 25000, '2 étoiles', 5.9620, 10.1580),
            ('Mountain View', 'Bamenda', 32000, '2 étoiles', 5.9680, 10.1620),
            ('Savannah Hôtel', 'Bamenda', 28000, '2 étoiles', 5.9610, 10.1570),
            ('Hilltop Hôtel', 'Bamenda', 22000, '1 étoile', 5.9750, 10.1750),
            ('Hôtel Bamenda', 'Bamenda', 20000, '1 étoile', 5.9640, 10.1600),
        ],
        'Ouest': [
            ('Zingana Hôtel', 'Bafoussam', 65000, '4 étoiles', 5.4777, 10.4176),
            ('Hôtel Vallée de Bana', 'Bana', 95000, '4 étoiles', 5.1481, 10.2736),
            ('Tagidor Garden', 'Bangou', 120000, '4 étoiles', 5.2345, 10.4000),
            ('Hôtel Altitel', 'Bafoussam', 45000, '3 étoiles', 5.4800, 10.4200),
            ('Palace Hôtel Bafoussam', 'Bafoussam', 40000, '3 étoiles', 5.4750, 10.4150),
            ('Hôtel de l\'Ouest', 'Bafoussam', 35000, '2 étoiles', 5.4700, 10.4100),
            ('Hôtel Foumban', 'Foumban', 30000, '2 étoiles', 5.7283, 10.9000),
            ('Hôtel Dschang', 'Dschang', 25000, '2 étoiles', 5.4439, 10.0533),
            ('Hôtel Mbouda', 'Mbouda', 22000, '1 étoile', 5.6267, 10.2500),
            ('Hôtel Résidence', 'Bafoussam', 28000, '2 étoiles', 5.4820, 10.4220),
        ],
        'Sud': [
            ('Tara Plage', 'Kribi', 75000, '3 étoiles', 2.9506, 9.9123),
            ('Les Gîtes de Kribi', 'Kribi', 85000, '3 étoiles', 2.9400, 9.9050),
            ('Framotel', 'Kribi', 65000, '3 étoiles', 2.9600, 9.9200),
            ('Résidence Phénix', 'Kribi', 55000, '3 étoiles', 2.9550, 9.9150),
            ('Hôtel de l\'Océan', 'Kribi', 45000, '2 étoiles', 2.9700, 9.9300),
            ('Ebolowa Palace', 'Ebolowa', 50000, '3 étoiles', 2.9228, 11.1522),
            ('Hôtel Bengo', 'Ebolowa', 60000, '3 étoiles', 2.9250, 11.1600),
            ('Hôtel de la Paix Sud', 'Ebolowa', 30000, '2 étoiles', 2.9200, 11.1500),
            ('Hôtel Sangmélima', 'Sangmélima', 25000, '2 étoiles', 2.9333, 11.9833),
            ('Hôtel de la Vallée Kribi', 'Kribi', 40000, '2 étoiles', 2.9450, 9.9100),
        ],
        'Sud-Ouest': [
            ('Mountain Hôtel', 'Buea', 65000, '3 étoiles', 4.1500, 9.2400),
            ('Parliamentarian Flats', 'Buea', 55000, '3 étoiles', 4.1550, 9.2450),
            ('Fini Hôtel', 'Limbe', 70000, '3 étoiles', 4.0167, 9.2167),
            ('Seme Beach Hôtel', 'Limbe', 95000, '4 étoiles', 4.0000, 9.1500),
            ('Atlantic Beach Hôtel', 'Limbe', 60000, '3 étoiles', 4.0100, 9.2100),
            ('Coastline Hôtel', 'Limbe', 45000, '2 étoiles', 4.0200, 9.2200),
            ('Victoria Guest House', 'Limbe', 35000, '2 étoiles', 4.0150, 9.2150),
            ('Hôtel Buea', 'Buea', 30000, '2 étoiles', 4.1450, 9.2350),
            ('Hôtel Limbe', 'Limbe', 25000, '2 étoiles', 4.0180, 9.2180),
            ('Hôtel Kumba', 'Kumba', 22000, '1 étoile', 4.6361, 9.4469),
        ],
    }

    images_hotel = [
        "https://images.unsplash.com/photo-1566073771259-6a8506099945",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa",
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4",
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb",
        "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9"
    ]
    
    images_reception = [
        "https://images.unsplash.com/photo-1517841905240-472988babdf9",
        "https://images.unsplash.com/photo-1568495248636-6432b97bd949",
        "https://images.unsplash.com/photo-1571896349842-33c89424de2d"
    ]

    images_resto = [
        "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b",
        "https://images.unsplash.com/photo-1550966841-3ee7adac1af0",
        "https://images.unsplash.com/photo-1559339352-11d035aa65de"
    ]

    images_chambre = [
        "https://images.unsplash.com/photo-1590490360182-c33d57733427",
        "https://images.unsplash.com/photo-1566665797739-1674de7a421a",
        "https://images.unsplash.com/photo-1611892440504-42a792e24d32"
    ]

    room_types = [
        ('Standard', 25000, 'Une chambre confortable avec tous les équipements de base.'),
        ('Studio', 30000, 'Parfait pour les longs séjours avec une kitchenette intégrée.'),
        ('Supérieure', 35000, 'Plus d\'espace et une meilleure vue pour un séjour relaxant.'),
        ('Deluxe', 40000, 'Luxe et confort supérieurs avec des équipements haut de gamme.'),
        ('Chambre Familiale', 45000, 'Espace optimisé pour accueillir toute la famille.'),
        ('Suite Junior', 50000, 'Idéal pour les voyages d\'affaires ou les escapades romantiques.'),
        ('Suite Executive', 60000, 'Le summum du confort avec un coin salon séparé.'),
        ('Suite Présidentielle', 70000, 'Une expérience royale avec des services exclusifs.'),
    ]

    total_hotels = 0
    for region, hotels in regions_hotels.items():
        print(f"Création des hôtels pour la région : {region}...")
        for h_data in hotels:
            nom, ville, prix_base_hotel, confort, lat, lon = h_data
            
            hotel = Hotel.objects.create(
                nom=nom,
                region=region,
                ville=ville,
                prix_nuit=prix_base_hotel,
                confort=confort,
                image_url=random.choice(images_hotel),
                image_reception=random.choice(images_reception),
                image_resto=random.choice(images_resto),
                latitude=lat,
                longitude=lon
            )
            
            # On définit un décalage aléatoire pour cet hôtel (-2000 à +3000)
            # pour que les hôtels de même base soient quand même différents
            offset_hotel = random.choice([-2000, -1000, 0, 1000, 2000, 3000, 4000, 5000])
            
            # 6. Créer les 8 types de chambres avec des prix basés sur l'hôtel
            supplements = [0, 5000, 10000, 15000, 20000, 30000, 45000, 70000]
            
            for i, (rt_name, _, desc) in enumerate(room_types):
                # Prix = Prix de base hôtel + supplément catégorie + offset hôtel
                prix_final = prix_base_hotel + supplements[i] + offset_hotel
                
                # On s'assure que le prix reste un multiple de 1000 et raisonnable
                prix_final = max(15000, round(prix_final / 1000) * 1000)
                
                Chambre.objects.create(
                    hotel=hotel,
                    categorie=rt_name,
                    prix=prix_final,
                    description=desc,
                    image_url=random.choice(images_chambre),
                    image_salon="https://images.unsplash.com/photo-1582719508461-905c673771fd",
                    image_douche="https://images.unsplash.com/photo-1584622650111-993a426fbf0a",
                    est_disponible=True
                )
            total_hotels += 1

    # 7. Afficher un message de succès
    print(f"\nSuccès ! {total_hotels} hôtels et {total_hotels * 8} chambres ont été créés.")

if __name__ == '__main__':
    seed_data()

from datetime import datetime, time, timedelta

# API Configuration
SNCF_API_URL = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records"
API_LIMIT = 100

# Date Configuration
MIN_DATE = datetime.now().date()
MAX_DATE = MIN_DATE + timedelta(days=30)  # Fenêtre glissante de 30 jours

# Time Configuration
DEFAULT_START_TIME = time(6, 0)
DEFAULT_END_TIME = time(23, 0)

# Search Configuration
DEFAULT_ORIGIN = "PARIS"
MAX_RANGE_DAYS = 30  # Maximum de 30 jours
DEFAULT_RANGE_DAYS = 7  # Une semaine par défaut

# Cache Configuration
CACHE_TTL = 3600  # 1 hour in seconds

STATIONS = [
    "PARIS (intramuros)",
    "LYON (intramuros)",
    "MARSEILLE (intramuros)",
    "BORDEAUX",
    "TOULOUSE",
    "NANTES",
    "STRASBOURG",
    "LILLE",
    "NICE",
    "RENNES"
]

# Coordonnées approximatives des gares pour la carte
STATIONS_COORDS = {
    "PARIS (intramuros)": [48.8566, 2.3522],
    "LYON (intramuros)": [45.7578, 4.8320],
    "MARSEILLE (intramuros)": [43.2965, 5.3698],
    "BORDEAUX": [44.8378, -0.5792],
    "TOULOUSE": [43.6047, 1.4442],
    "NANTES": [47.2184, -1.5536],
    "STRASBOURG": [48.5734, 7.7521],
    "LILLE": [50.6292, 3.0573],
    "NICE": [43.7102, 7.2620],
    "RENNES": [48.1173, -1.6778]
} 
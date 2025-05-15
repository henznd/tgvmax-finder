import pandas as pd
from datetime import datetime, time, timedelta
from typing import List, Dict
import requests
import streamlit as st
from config import SNCF_API_URL, API_LIMIT, CACHE_TTL
from bs4 import BeautifulSoup
import random
import time

def duration_to_minutes(duration_str: str) -> int:
    """
    Convertit une durée au format 'XhYY' en minutes.
    Par exemple: '2h15' -> 135
    """
    try:
        if 'h' in duration_str:
            hours, minutes = duration_str.split('h')
            return int(hours) * 60 + (int(minutes) if minutes else 0)
        return int(duration_str)
    except:
        return 0

@st.cache_data(ttl=CACHE_TTL)
def get_tgvmax_trains(date: str, origin: str = None, destination: str = None) -> List[Dict]:
    """
    Récupère les trains TGV Max disponibles pour une date donnée.
    Utilise le cache Streamlit pour optimiser les performances.
    """
    where_conditions = [f"date = date'{date}'", "od_happy_card = 'OUI'"]
    
    if origin:
        where_conditions.append(f"origine LIKE '{origin}%'")
    if destination:
        where_conditions.append(f"destination LIKE '{destination}%'")
    
    params = {
        'where': ' AND '.join(where_conditions),
        'limit': API_LIMIT,
        'order_by': 'heure_depart'
    }
    
    try:
        response = requests.get(SNCF_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la requête API: {str(e)}")
        return []

def calculate_duration(departure: str, arrival: str) -> str:
    """
    Calcule la durée entre deux heures au format HH:MM.
    """
    dep = pd.to_datetime(departure, format='%H:%M')
    arr = pd.to_datetime(arrival, format='%H:%M')
    duration = arr - dep
    hours = duration.components.hours
    minutes = duration.components.minutes
    return f"{hours}h{minutes:02d}"

def filter_trains_by_time(df: pd.DataFrame, depart_start: time, depart_end: time, 
                         return_start: time = None, return_end: time = None, 
                         is_round_trip: bool = True) -> pd.DataFrame:
    """
    Filtre les trains selon les plages horaires spécifiées.
    """
    if df.empty:
        return df
        
    # Conversion des heures en objets time pour la comparaison
    if is_round_trip:
        df['Aller_Time'] = pd.to_datetime(df['Aller_Heure'], format='%H:%M').dt.time
        mask_aller = (df['Aller_Time'] >= depart_start) & (df['Aller_Time'] <= depart_end)
        
        if return_start and return_end:
            df['Retour_Time'] = pd.to_datetime(df['Retour_Heure'], format='%H:%M').dt.time
            mask_retour = (df['Retour_Time'] >= return_start) & (df['Retour_Time'] <= return_end)
            mask = mask_aller & mask_retour
        else:
            mask = mask_aller
    else:
        df['Depart_Time'] = pd.to_datetime(df['heure_depart'], format='%H:%M').dt.time
        mask = (df['Depart_Time'] >= depart_start) & (df['Depart_Time'] <= depart_end)
    
    filtered_df = df[mask].copy()
    # Suppression des colonnes temporaires
    cols_to_drop = ['Aller_Time', 'Retour_Time', 'Depart_Time']
    filtered_df.drop([col for col in cols_to_drop if col in filtered_df.columns], axis=1, inplace=True)
    return filtered_df

def format_single_trips(trains: List[Dict]) -> pd.DataFrame:
    """
    Formate les trajets simples en DataFrame.
    """
    if not trains:
        return pd.DataFrame()
    
    df = pd.DataFrame(trains)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%d/%m/%Y')
    df['duree'] = df.apply(lambda x: calculate_duration(x['heure_depart'], x['heure_arrivee']), axis=1)
    df['duree_minutes'] = df['duree'].apply(duration_to_minutes)
    
    return df[['origine', 'destination', 'date', 'heure_depart', 'heure_arrivee', 'duree', 'duree_minutes']]

def handle_error(func):
    """
    Décorateur pour gérer les erreurs de manière uniforme.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"Une erreur est survenue : {str(e)}")
            return pd.DataFrame()
    return wrapper

def search_trains(departure, arrival, date, min_time, max_time, max_duration, max_connections):
    """
    Recherche les trains disponibles selon les critères donnés.
    Simule une recherche pour le moment avec des données aléatoires.
    """
    trains = []
    num_trains = random.randint(0, 10)  # Nombre aléatoire de trains
    
    for _ in range(num_trains):
        # Génère une heure de départ aléatoire entre min_time et max_time
        departure_hour = random.randint(min_time.hour, max_time.hour)
        departure_minute = random.randint(0, 59)
        departure_time = datetime.combine(date, datetime.strptime(f"{departure_hour}:{departure_minute}", "%H:%M").time())
        
        # Génère une durée aléatoire
        duration_minutes = random.randint(60, max_duration * 60)
        arrival_time = departure_time + timedelta(minutes=duration_minutes)
        
        # Génère un nombre aléatoire de correspondances
        connections = random.randint(0, max_connections)
        
        # Format les heures pour l'affichage
        departure_str = departure_time.strftime("%H:%M")
        arrival_str = arrival_time.strftime("%H:%M")
        duration_str = format_duration(duration_minutes)
        
        trains.append([departure_str, arrival_str, duration_str, connections])
    
    return trains

def format_duration(minutes):
    """
    Formate une durée en minutes en format heures et minutes.
    """
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}h{remaining_minutes:02d}" 
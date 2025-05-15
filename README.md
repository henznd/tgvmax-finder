# TGV Max Finder 🚅

Une application web pour trouver facilement les trajets disponibles avec votre abonnement TGV Max.

## Fonctionnalités

- 📊 **Vue détaillée** : Consultez tous les trajets disponibles avec leurs horaires
- 📈 **Résumé par destination** : Visualisez les trajets groupés par destination
- 📊 **Statistiques** : Analysez les durées moyennes et les destinations les plus desservies

### Fonctionnalités à venir
- ⭐ Favoris - Sauvegardez vos trajets préférés
- 🗺️ Carte interactive - Visualisez vos trajets sur une carte

## Installation

1. Clonez le repository :
```bash
git clone https://github.com/henznd/tgvmax-finder.git
cd tgvmax-finder
```

2. Créez un environnement virtuel et activez-le :
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Unix/macOS
# ou
.\venv\Scripts\activate  # Sur Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Lancez l'application :
```bash
streamlit run tgvmax_app.py
```

L'application sera accessible à l'adresse : http://localhost:8501

## Structure du projet

```
tgvmax-finder/
├── tgvmax_app.py    # Application principale
├── config.py        # Configuration
├── utils.py         # Fonctions utilitaires
├── requirements.txt # Dépendances
└── README.md        # Documentation
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 
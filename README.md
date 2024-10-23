## Scraping Books to Scrape
# Description
Ce projet récupère les informations des livres sur le site Books to Scrape. Il parcourt toutes les catégories, extrait les détails de chaque livre (titre, prix, disponibilité, etc.), télécharge les images de couverture, et enregistre les données dans des fichiers CSV distincts pour chaque catégorie.

# Prérequis
Python 3.x
Bibliothèques Python :
requests
beautifulsoup4
csv

# Installation des modules :
pip install requests beautifulsoup4

# Utilisation
Clonez le dépôt.
Exécutez le script main.py :
python main.py
Les informations des livres seront enregistrées dans des fichiers CSV pour chaque catégorie, et les images dans des dossiers nommés par catégorie.

# Organisation des fichiers
Chaque catégorie a son propre dossier avec :
Un fichier CSV contenant les détails des livres.
Les images de couverture des livres.

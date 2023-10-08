# Nous importons le module csv, présent dans la bibliothèque standard de Python et 
# qui fournit des fonctionnalités pour lire et écrire des fichiers CSV.
# Il sera utilisé pour écrire les données extraites dans un fichier CSV.
import csv

# Nous importons requests, qui est une bibliothèque cliente HTTP, spécialement conçue pour le langage de programmation Python. 
import requests

# Nous importons la classe BeautifulSoup du module bs4. BeautifulSoup est une bibliothèque qui est utiisée pour 
# le parsing (analyse) de documents HTML ou XML. Ici, elle est utilisée pour extraire des informations spécifiques de la page web.
from bs4 import BeautifulSoup


# PHASE 1 

page_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

# Récupération du contenu HTML de la main_page_url
response = requests.get(page_url)

soup = BeautifulSoup(response.content, 'html.parser')


# product_page_url = 'http://books.toscrape.com/
universal_product_code = soup.find('td').text
title = soup.find('h1').text
price_excluding_tax = soup.find('th', string="Price (excl. tax)").find_next('td').text
price_including_tax = soup.find('th', string="Price (incl. tax)").find_next('td').text
number_available = soup.find('th', string="Availability").find_next('td').text
product_description = soup.find('div', id='product_description').find_next('p').text
category = soup.find('ul', class_= 'breadcrumb').find_all('li')[2].text
review_rating = soup.find("p", class_="star-rating")["class"][-1]
image_url = soup.find('img')["src"]

print(price_excluding_tax, price_including_tax, number_available, category, review_rating, image_url)

#Création d'un objet qui nous servira à transmettre les données au format CSV 
donnees_produit = {
    'Universal Product Code': universal_product_code,
    'Title': title,
    'Price (Excluding Tax)': price_excluding_tax,
    'Price (Including Tax)': price_including_tax,
    'Number Available': number_available,
    'Product Description': product_description,
    'Category': category,
    'Review Rating': review_rating,
    'Image URL': image_url
}

# Nous ouvrons un fichier CSV (s'il n'existe pas, il sera crée) les données dans un fichier CSV avec des en-têtes
with open('donnees_produit.csv', 'w', newline='', encoding='utf-8') as csvfile:
    #On crée la variable fieldnames, qui contient les clefs présentes dans l'objet données produit
    #utilise la bibliotheque csv pour créer un dictionnaire 
    fieldnames = donnees_produit.keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Ecriture des en-têtes avec les paramètres passés ci-dessus 
    writer.writeheader()

    writer.writerow(donnees_produit)

print("Données exportées avec succès dans le fichier CSV.")
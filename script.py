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
# product_type= soup.find('th', text="Product Type").find_next('td').text
price_excluding_tax = soup.find('th', string="Price (excl. tax)").find_next('td').text
price_including_tax = soup.find('th', string="Price (incl. tax)").find_next('td').text
number_available = soup.find('th', string="Availability").find_next('td').text
product_description = soup.find('div', id='product_description').find_next('p').text
category = soup.find('ul', class_= 'breadcrumb').find_all('li')[2].text
review_rating = soup.find("p", class_="star-rating")["class"][-1]
image_url = soup.find('img')["src"]

print(price_excluding_tax, price_including_tax, number_available, category, review_rating, image_url).__format__

# Price (excl. tax)
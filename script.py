# Nous importons le module csv, présent dans la bibliothèque standard de Python et 
# qui fournit des fonctionnalités pour lire et écrire des fichiers CSV.
# Il sera utilisé pour écrire les données extraites dans un fichier CSV.
import csv

# Nous importons requests, qui est une bibliothèque cliente HTTP, spécialement conçue pour le langage de programmation Python. 
import requests

# Nous importons la classe BeautifulSoup du module bs4. BeautifulSoup est une bibliothèque qui est utiisée pour 
# le parsing (analyse) de documents HTML ou XML. Ici, elle est utilisée pour extraire des informations spécifiques de la page web.
from bs4 import BeautifulSoup


#import de pprint afin d'améliorer la lisibilité des print / faciliter le debug
from pprint import pprint

import os

# On obtient le chemin absolu du fichier actuel, afin de pouvoir y écrire les données scrappées 
path = os.path.abspath(__file__)

# On obtient le répertoire racine en utilisant os.path.dirname
parent_directory = os.path.dirname(path)

print(f"Répertoire racine : {parent_directory}")

# On crée un dictionnaire pour les fichiers CSV
fichiers_csv = {}


print(f"Chemin absolu du fichier actuel : {path}")
pprint("Hi ! Please be patient, the programm is running")



# # # # # # # # #  PHASE 3 # # # # # # # # #

homepage = 'http://books.toscrape.com/'
response = requests.get(homepage)
soup = BeautifulSoup(response.content, 'html.parser')
prefix = 'https://books.toscrape.com/'


container = soup.find('div', class_='side_categories')
links = container.find_all('a')



link_list = []
for link in links:
    link = link['href']
    link = prefix + link
    link_list.append(link)  

link_list.pop(0)

all_pages = []

pprint("Nous sommes actuellement en train de récupérer les URLs de chacune des pages...")

for link in link_list:
    all_pages.append(link)
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    next_page = soup.find("li", class_='next')
    #  If we find another page, then we need to get the URL of it. We do this until there is no more next page
    if next_page : 
        splitted_link = link.rsplit('/', 1)
        new_link = next_page.find("a")["href"]
        link_to_add = splitted_link[0] + "/" + new_link
        link_list.append(link_to_add)

    else : 
        continue

all_pages = sorted(all_pages)

pprint("Toutes les URLs des pages produits ont été récupérés.")
pprint("Nous récupérons actuellement les URLs de chacun des produits")

all_products = []
for page in all_pages :
    response = requests.get(page)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_products_pods = soup.find_all('article', class_="product_pod")
    for pod in all_products_pods :
            product_link = pod.find("a")["href"]                            
            texte_a_remplacer = '../../../' 
            nouveau_texte = 'https://books.toscrape.com/catalogue/'
            nouveau_lien = product_link.replace(texte_a_remplacer, nouveau_texte)

            all_products.append(nouveau_lien)
            
pprint('Tous les URLs produits ont été récupérés')
            
            
         
for product in all_products : 
    response = requests.get(product)
    soup = BeautifulSoup(response.content, 'html.parser') 
    universal_product_code = soup.find('td').text
    title = soup.find('h1').text
    price_excluding_tax = soup.find('th', string="Price (excl. tax)").find_next('td').text
    price_including_tax = soup.find('th', string="Price (incl. tax)").find_next('td').text
    number_available = soup.find('th', string="Availability").find_next('td').text
     # Extraire la description du produit (si elle existe)
    product_description_element = soup.find('div', id='product_description')
    product_description = product_description_element.find_next('p').text if product_description_element else ''
    category = soup.find('ul', class_= 'breadcrumb').find_all('li')[2].text
    review_rating = soup.find("p", class_="star-rating")["class"][-1]
    image_url = soup.find('img')["src"]
    prefix = 'https://books.toscrape.com/'
    relative_path = image_url
    # Construction du chemin complet
    image_url = os.path.join(prefix, relative_path)

    print(f"Chemin complet : {image_url}")
    print(image_url)
    cleaned_category = category.strip().replace("\n", "").lower().replace(" ", "_")
    print("Actually scrapping this product information : ", title, "Category : ", cleaned_category )
    nom_fichier_csv = cleaned_category + ".csv"
    with open(parent_directory + '/fichiers_csv/' + nom_fichier_csv, 'a', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Product Page URL', 'Title', 'Price excluding tax', 'Price including tax', 'Number available', 'Product description', 'Category', 'Review rating']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if csvfile.tell() == 0:
                        writer.writeheader()
                    fichiers_csv[cleaned_category] = writer
                    fichiers_csv[cleaned_category].writerow({
                    'Product Page URL': product,
                    'Title': title,
                    'Price excluding tax': price_excluding_tax,
                    'Price including tax': price_including_tax,
                    'Number available': number_available,
                    'Product description': product_description,
                    'Category': category,
                    'Review rating': review_rating
                    }),
    response = requests.get(image_url)
    #  contenu binaire de l'image
    image_content = response.content
    image_filename = image_url.split("/")[-1]
    with open(parent_directory + '/images_folder/' + image_filename , 'wb') as image_file:
        image_file.write(image_content)

    print(f"L'image a été enregistrée sous le nom : {image_filename}")
    

pprint(len(all_products))
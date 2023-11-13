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

# Créez un dictionnaire pour les fichiers CSV
fichiers_csv = {}
pprint("Hello ! I'm actually analyzing the website. Please be patient, I'm doing my best :)")


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
print(len(all_pages))
pprint(all_pages)


all_products = []
for page in all_pages :
    response = requests.get(page)
    soup = BeautifulSoup(response.content, 'html.parser')
    pprint("Récupération des liens produits de la page " + page)
    all_products_pods = soup.find_all('article', class_="product_pod")
    for pod in all_products_pods :
            product_link = pod.find("a")["href"]                            
            texte_a_remplacer = '../../../' 
            nouveau_texte = 'https://books.toscrape.com/catalogue/'
            nouveau_lien = product_link.replace(texte_a_remplacer, nouveau_texte)

            all_products.append(nouveau_lien)
            
            
         
for product in all_products : 
    response = requests.get(product)
    soup = BeautifulSoup(response.content, 'html.parser') 
    universal_product_code = soup.find('td').text
    title = soup.find('h1').text
    # print(title)
    price_excluding_tax = soup.find('th', string="Price (excl. tax)").find_next('td').text
    price_including_tax = soup.find('th', string="Price (incl. tax)").find_next('td').text
    number_available = soup.find('th', string="Availability").find_next('td').text
     # Extraire la description du produit (si elle existe)
    product_description_element = soup.find('div', id='product_description')
    product_description = product_description_element.find_next('p').text if product_description_element else ''
    category = soup.find('ul', class_= 'breadcrumb').find_all('li')[2].text
    review_rating = soup.find("p", class_="star-rating")["class"][-1]
    cleaned_category = category.strip().replace("\n", "").lower().replace(" ", "_")
    pprint("Actually scrapping this product information : ", title, "Category : ", cleaned_category )
    nom_fichier_csv = cleaned_category + ".csv"
    # if cleaned_category not in fichiers_csv:
    with open('C:/Projets_Open_Classrooms_PYTHON/BooksOnline_Jeulin_Clement/fichiers_csv/'+nom_fichier_csv, 'a', newline='', encoding='utf-8') as csvfile:
                    # On crée un fichier CSV pour cette catégorie
                    fieldnames = ['Product Page URL', 'Title', 'Price excluding tax', 'Price including tax', 'Number available', 'Product description', 'Category', 'Review rating']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    # Écrivez les en-têtes seulement si le fichier vient d'être créé
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

pprint(len(all_products))
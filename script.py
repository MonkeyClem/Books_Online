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
# title = soup.find('h1').text
# price_excluding_tax = soup.find('th', string="Price (excl. tax)").find_next('td').text
# price_including_tax = soup.find('th', string="Price (incl. tax)").find_next('td').text
# number_available = soup.find('th', string="Availability").find_next('td').text
# product_description = soup.find('div', id='product_description').find_next('p').text
# category = soup.find('ul', class_= 'breadcrumb').find_all('li')[2].text
# review_rating = soup.find("p", class_="star-rating")["class"][-1]
# image_url = soup.find('img')["src"]

# print(price_excluding_tax, price_including_tax, number_available, category, review_rating, image_url)

#Création d'un objet qui nous servira à transmettre les données au format CSV 
# donnees_produit = {
#     'Universal Product Code': universal_product_code,
#     'Title': title,
#     'Price (Excluding Tax)': price_excluding_tax,
#     'Price (Including Tax)': price_including_tax,
#     'Number Available': number_available,
#     'Product Description': product_description,
#     'Category': category,
#     'Review Rating': review_rating,
#     'Image URL': image_url
# }

# # Nous ouvrons un fichier CSV (s'il n'existe pas, il sera crée) les données dans un fichier CSV avec des en-têtes
# with open('donnees_produit.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     #On crée la variable fieldnames, qui contient les clefs présentes dans l'objet données produit
#     #utilise la bibliotheque csv pour créer un dictionnaire 
#     fieldnames = donnees_produit.keys()
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     # Ecriture des en-têtes avec les paramètres passés ci-dessus 
#     writer.writeheader()

#     writer.writerow(donnees_produit)

# print("Données exportées avec succès dans le fichier CSV.")

#####################  PHASE 2 #####################



category_url = "http://books.toscrape.com/catalogue/category/books/fiction_10/index.html"

response = requests.get(category_url)

soup = BeautifulSoup(response.content, 'html.parser')

# def get_all_pages(a = str)

link_array = []
link_array.append(category_url)

while True : 
    pages = soup.find("li", class_="next")
    # print(pages)
    if pages == None :  break
    link_to_next_page = pages.find("a")['href']
    # print("link_to_next_page: " + link_to_next_page)
    splitted_url = category_url.split("index.html")
    # print(splitted_url)
    to_next_page =  splitted_url[0]+link_to_next_page
    # link_array.append(to_next_page)
    link_array.append(to_next_page)
    response = requests.get(to_next_page)
    soup = BeautifulSoup(response.content, 'html.parser')


# print(link_array)

product_list = []
prefix = "http://books.toscrape.com/catalogue/"


for link in link_array:
    print(link)
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_pods = soup.find_all("div", class_="image_container")
    for pod in all_pods:   
        # On récupere tous les éléments <a> à l'intérieur de l'article avec la classe "product_pod"
        links_inside_pod = pod.find_all('a')
        # print(links_inside_pod)
        # Puis on itère sur les liens à l'intérieur de chaque product_pod
        for link in links_inside_pod:
                # Récupérer l'URL du lien
                url = link['href']
                splitted_url = url.split('../../../')
                product_url = prefix+splitted_url[1]
                # print(prefix+splitted_url[1])
                product_list.append(product_url)
                # # print("URL du lien :", prefix + splitted_url)

# print(product_list)


for product in product_list : 
    response = requests.get(product)
    soup = BeautifulSoup(response.content, 'html.parser')
    universal_product_code = soup.find('td').text
    # print(universal_product_code)
    title = soup.find('h1').text
    price_excluding_tax = soup.find('th', string="Price (excl. tax)").find_next('td').text
    price_including_tax = soup.find('th', string="Price (incl. tax)").find_next('td').text
    number_available = soup.find('th', string="Availability").find_next('td').text
    product_description = soup.find('div', id='product_description').find_next('p').text
    category = soup.find('ul', class_= 'breadcrumb').find_all('li')[2].text
    review_rating = soup.find("p", class_="star-rating")["class"][-1]
    image_url = soup.find('img')["src"]

    # print(title, price_excluding_tax, price_including_tax, number_available, category, review_rating)

# Création d'un objet qui nous servira à transmettre les données au format CSV 
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

# Nous ouvrons un fichier CSV (s'il n'existe pas, il sera crée) 
with open('donnees_produit.csv', 'w', newline='', encoding='utf-8') as csvfile:
    #On crée la variable fieldnames, qui contient les clefs présentes dans l'objet données produit
    #utilise la bibliotheque csv pour créer un dictionnaire 
    fieldnames = donnees_produit.keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Ecriture des en-têtes avec les paramètres passés ci-dessus 
    writer.writeheader()

    writer.writerow(donnees_produit)

print("Données exportées avec succès dans le fichier CSV.")
   
 

    # pages = soup.find("li", class_="next")
    # link_to_next_page = pages.find("a")['href']

    # if pages : None 
    # break


# if pages: 
#     link_to_next_page = pages.find("a")['href']
#     print(link_to_next_page)
#     splitted_url = category_url.split("index.html")
#     # print(splitted_url)
#     to_next_page =  splitted_url[0]+link_to_next_page
#     # print(to_next_page)


#     pages = soup.find("li", class_="next")
#     if link_to_next_page : 
#         link_to_next_page = pages.find("a")['href']
#         print(link_to_next_page)
#         splitted_url = category_url.split("index.html")
#         # print(splitted_url)
#         response = requests.get(to_next_page)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         print(to_next_page)

#     else : 
#         print("No next page found")
  
    


# article_list = soup.find_all("article", class_="product_pod")
# article_array = soup.find_all("div", class_="image_container").find('a')


# for article in article_list:
#     link = article.find("a")["href"]
#     # print(link)
#     link = link.split("../../../")
#     link = link[1]
   
#     if pagination : 
#             link_to_next_page = pagination.find("a")["href"]  
#             # print(link_to_next_page) 
#             splitted_url = category_url.split("index.html")
#             # print(splitted_url) 
#             url_to_next_page = splitted_url[0]+link_to_next_page
#             print(url_to_next_page) 
#             # next_page = pagination.find("li", class_="next")
#         # product_title = product_container.find('h3').get_text()
#         # link_to_product.click()
#         # print(product_title)
#     prefix = 'http://books.toscrape.com/catalogue/'
#     product_url = prefix+link
#     print(product_url)
#     response = requests.get(product_url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     title = soup.find("h1").text
#     price_excluding_tax = soup.find('th', string="Price (excl. tax)").find_next('td').text
#     price_including_tax = soup.find('th', string="Price (incl. tax)").find_next('td').text
#     number_available = soup.find('th', string="Availability").find_next('td').text
#     product_description = soup.find('div', id='product_description').find_next('p').text
#     category = soup.find('ul', class_= 'breadcrumb').find_all('li')[2].text
#     review_rating = soup.find("p", class_="star-rating")["class"][-1]
#     prefix = "http://books.toscrape.com/"
#     image_url = soup.find('img')["src"]
#     image_url = image_url.split("../../")
#     image_url = prefix+image_url[1]
#     # print(title, price_excluding_tax, price_including_tax, number_available, category, review_rating, image_url)
    

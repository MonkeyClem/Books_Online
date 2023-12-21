Ce script Python permet de récupérer des informations sur les produits du site web "https://books.toscrape.com/" en utilisant les bibliothèques BeautifulSoup et requests.

ETAPE 1 : Configuration de l'Environnement
Clonez le répertoire du projet depuis GitHub, en utilisant cette commande dans votre terminal : git clone https://github.com/MonkeyClem/Books_Online.git
Une fois cela effectué, rendez vous dans le fichier à l'aide de la commande : cd Books_Online




ETAPE 2. Création de l'Environnement Virtuel
Créez un environnement virtuel à l'aide de venv? en entrant cette commande dans votre terminal : python -m venv venv

Activez l'environnement virtuel à l'aide de la commande :

Sur Windows :
venv\Scripts\activate

Sur macOS/Linux :
source venv/bin/activate




ETAPE 3. Installation des Dépendances
Installez les dépendances à partir du fichier requirements.txt avec la commande : pip install -r requirements.txt

Une fois l'environnement virtuel activé et les dépendances installées, vous pouvez exécuter le script Python avec : python script.py

Les données seront extraites, organisées dans des fichiers CSV, et les images des produits seront téléchargées.



Une fois cela terminé, n'oubliez pas de désactiver votre environnement virtuel à l'aide de la commande "deactivate". 

import requests
from bs4 import BeautifulSoup
import csv

url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1').text
    price_including_tax = soup.find('p', class_='price_color').text
    availability = soup.find('p', class_='instock availability').text.strip()
    upc = soup.find('tr').find('td').text
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()

    with open('books.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'price_including_tax', 'availability', 'upc', 'category'])
        writer.writerow([title, price_including_tax, availability, upc, category])

    print(f"Données écrites dans books.csv : {title}, {price_including_tax}, {availability}, {upc}, {category}")
else:
    print("Erreur lors du téléchargement de la page.")

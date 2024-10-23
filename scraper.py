import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import urllib.parse  

base_url = 'https://books.toscrape.com/'

def create_img_folder(category_name):
    img_folder = os.path.join('img', category_name)
    try:
        os.makedirs(img_folder, exist_ok=True)
        print(f"Dossier '{img_folder}' créé.")
    except FileExistsError:
        print(f"Dossier '{img_folder}' existe déjà.")
    return img_folder

def extract_book_data(book_url):
    response = requests.get(book_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1').text
        price_including_tax = soup.find('p', class_='price_color').text
        availability = soup.find('p', class_='instock availability').text.strip()
        upc = soup.find('tr').find('td').text
        category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
        image_url = base_url + soup.find('img')['src'].replace('../', '')
        return [title, price_including_tax, availability, upc, category, image_url]
    return None

def get_books_urls_from_category_page(category_url):
    response = requests.get(category_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
        book_urls = [base_url + "catalogue/" + book.find('h3').find('a')['href'].replace('../../../', '') for book in books]
        return book_urls
    return []

def get_next_page(soup):
    next_button = soup.find('li', class_='next')
    if next_button:
        next_page_url = next_button.find('a')['href']
        return next_page_url
    return None

def download_image(image_url, title, img_folder):
    safe_title = re.sub(r'[\\/*?:"<>|\' ]', "_", title)
    
    image_filename = os.path.join(img_folder, f"{safe_title}.jpg")
    
    image_url = urllib.parse.quote(image_url, safe=':/')

    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_filename, 'wb') as img_file:
            img_file.write(response.content)
        print(f"Image téléchargée : {image_filename}")
    else:
        print(f"Erreur lors du téléchargement de l'image : {image_url}")

def scrape_category_books(category_url, category_name):
    page_url = category_url
    all_books_data = []
    img_folder = create_img_folder(category_name)

    while page_url:
        response = requests.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            book_urls = get_books_urls_from_category_page(page_url)

            for book_url in book_urls:
                book_data = extract_book_data(book_url)
                if book_data:
                    all_books_data.append(book_data)
                    download_image(book_data[5], book_data[0], img_folder)

            next_page_url = get_next_page(soup)
            if next_page_url:
                page_url = category_url.replace('index.html', '') + next_page_url
            else:
                page_url = None

    return all_books_data

def get_all_categories():
    response = requests.get(base_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        category_links = soup.find('ul', class_='nav nav-list').find('ul').find_all('a')
        categories = {link.text.strip(): base_url + link['href'] for link in category_links}
        return categories
    return {}

def scrape_all_categories():
    categories = get_all_categories()
    
    for category_name, category_url in categories.items():
        print(f"Scraping la catégorie : {category_name}")
        books_data = scrape_category_books(category_url, category_name)

        csv_filename = f'{category_name}.csv'
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'price_including_tax', 'availability', 'upc', 'category'])
            for book in books_data:
                writer.writerow(book)

        print(f"Données écrites dans {csv_filename} pour la catégorie {category_name}")

scrape_all_categories()

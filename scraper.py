import requests
from bs4 import BeautifulSoup
import csv

def extract_book_data(book_url):
    """Extrait les données d'un livre à partir de son URL."""
    response = requests.get(book_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1').text
        price_including_tax = soup.find('p', class_='price_color').text
        availability = soup.find('p', class_='instock availability').text.strip()
        upc = soup.find('tr').find('td').text
        category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
        return [title, price_including_tax, availability, upc, category]
    return None

def get_books_urls_from_category_page(category_url):
    """Récupère les URLs des livres à partir de la page de la catégorie."""
    response = requests.get(category_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
        book_urls = ["https://books.toscrape.com/catalogue/" + book.find('h3').find('a')['href'].replace('../../../', '') for book in books]
        return book_urls
    return []

def get_next_page(soup):
    """Récupère l'URL de la page suivante s'il y en a une."""
    next_button = soup.find('li', class_='next')
    if next_button:
        next_page_url = next_button.find('a')['href']
        return next_page_url
    return None

def scrape_category_books(base_url):
    """Scrape les livres d'une catégorie."""
    page_url = base_url
    all_books_data = []

    while page_url:
        response = requests.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            book_urls = get_books_urls_from_category_page(page_url)
            for book_url in book_urls:
                book_data = extract_book_data(book_url)
                if book_data:
                    all_books_data.append(book_data)

            next_page_url = get_next_page(soup)
            if next_page_url:
                page_url = base_url.replace('index.html', '') + next_page_url
            else:
                page_url = None

    return all_books_data

category_url = 'https://books.toscrape.com/catalogue/category/books/poetry_23/index.html'

books_data = scrape_category_books(category_url)

with open('category_books.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['title', 'price_including_tax', 'availability', 'upc', 'category'])
    for book in books_data:
        writer.writerow(book)

print(f"Données écrites dans category_books.csv pour la catégorie {category_url}")

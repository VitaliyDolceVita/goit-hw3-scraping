import requests
from bs4 import BeautifulSoup
import json

# Функція для отримання даних з однієї сторінки
def scrape_page(page_url):
    quotes_data = []
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    quotes = soup.find_all('div', class_='quote')

    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        quotes_data.append({
            'tags': tags,
            'author': author,
            'quote': text
        })

    return quotes_data

# Функція для скрапінга інформації про авторів
def scrape_author(author_page_url):
    authors_data = []
    page = requests.get(author_page_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    authors = soup.find_all('div', class_='author-details')

    for author in authors:
        fullname = author.find('h3', class_='author-title').text.strip()
        born_date = author.find('span', class_='author-born-date').text.strip()
        born_location = author.find('span', class_='author-born-location').text.strip()
        description = author.find('div', class_='author-description').text.strip()
        authors_data.append({
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description
        })

    return authors_data

# Збираємо цитати з усіх сторінок
all_quotes = []
base_url = 'http://quotes.toscrape.com'
current_page = '/page/1/'

while current_page:
    all_quotes.extend(scrape_page(base_url + current_page))
    soup = BeautifulSoup(requests.get(base_url + current_page).text, 'html.parser')
    next_button = soup.find('li', class_='next')
    current_page = next_button.find('a')['href'] if next_button else None

# Збираємо інформацію про авторів (у цьому прикладі скрапляємо тільки з однієї сторінки)
authors_url = 'http://quotes.toscrape.com/authors'
all_authors = scrape_author(authors_url)

# Зберігаємо дані у JSON файл
with open('quotes.json', 'w', encoding ='utf-8') as f:
    json.dump(all_quotes, f, ensure_ascii=False, indent=2)

with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(all_authors, f, ensure_ascii=False, indent=2)

print('Scraping done. Data saved to quotes.json and authors.json')

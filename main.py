import requests
from bs4 import BeautifulSoup
import json

# Функція для отримання даних з однієї сторінки
def scrape_page(page_url):
    quotes_data = []
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, 'lxml')
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
    soup = BeautifulSoup(page.text, 'lxml')
    authors = soup.find_all('div', class_='author-details')


    for author in authors:
        # print(author)
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
all_authors = []
base_url = 'http://quotes.toscrape.com'
current_page = '/page/1/'

while current_page:
    print(base_url + current_page)
    all_quotes.extend(scrape_page(base_url + current_page))
    soup = BeautifulSoup(requests.get(base_url + current_page).text, 'lxml')
    next_button = soup.find('li', class_='next')
    current_page = next_button.find('a')['href'] if next_button else None

    # Збираємо інформацію про авторів (у цьому прикладі скрапляємо тільки з однієї сторінки)
    authors_urls = []
    # authors_url = 'https://quotes.toscrape.com/author/J-K-Rowling/'


    response = requests.get('http://quotes.toscrape.com')
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    # Знайти всі span елементи, які мають клас 'author', а потім знайти всі 'a' елементи в них
    authors_spans = soup.find_all('small', class_='author')

    # Ітерувати по кожному span та отримати 'href' атрибут з внутрішнього 'a' елемента
    for author_span in authors_spans:
        # print(author_span)
        link = author_span.find_next('a')['href']
        print(link)
        authors_urls.append(base_url+link)


    print(authors_urls)

    for authors_url in authors_urls:
        author_result = scrape_author(authors_url)
        print(*author_result)
        all_authors.extend(author_result)


# Зберігаємо дані у JSON файл
with open('quotes.json', 'w', encoding ='utf-8') as f:
    json.dump(all_quotes, f, ensure_ascii=False, indent=2)


with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(all_authors, f, ensure_ascii=False, indent=2)

print('Scraping done. Data saved to quotes.json and authors.json')


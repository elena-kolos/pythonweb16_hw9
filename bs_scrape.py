import requests
from bs4 import BeautifulSoup
import json

from mongoengine import connect
from connect import *
# Підключення до MongoDB
connect(db='scrapsoup', host=uri, port=27017)

db = client["scrapsoup"] 

base_url = 'http://quotes.toscrape.com'

quotes_data = []
authors_data = []

# Функція для отримання даних з однієї сторінки
def scrape_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Отримання цитат зі сторінки
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
        
        # Перевірка, чи автор вже доданий у список
        if not any(a['fullname'] == author for a in authors_data):
            authors_data.append({'fullname': author, 'url': base_url + quote.find_previous('a')['href']})

    # Отримання посилання на наступну сторінку
    next_page = soup.find('li', class_='next')
    if next_page:
        next_page_url = base_url + next_page.find('a')['href']
        scrape_quotes(next_page_url)

# Виклик функції для скрапінгу даних зі сторінок
scrape_quotes(base_url)

# Запис у файл quotes.json
with open('quotes.json', 'w', encoding='utf-8') as quotes_file:
    json.dump(quotes_data, quotes_file, ensure_ascii=False, indent=2)

# Запис у файл authors.json
with open('authors.json', 'w', encoding='utf-8') as authors_file:
    json.dump(authors_data, authors_file, ensure_ascii=False, indent=2)

# Завантаження даних з файлу у колекцію бази даних
def load_json_data(file_name, collection_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
        collection = db[collection_name]  
        collection.insert_many(data)

# Завантаження даних з quotes.json у колекцію quotes
load_json_data('quotes.json', 'quotes')

# Завантаження даних з authors.json у колекцію authors
load_json_data('authors.json', 'authors')

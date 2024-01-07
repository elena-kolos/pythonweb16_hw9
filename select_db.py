from connect import *
from mongoengine import connect

# Підключення до MongoDB
connect(db='scrapsoup', host=uri, port=27017)
db = client["scrapsoup"] 


# Пошук цитат за ім'ям автора
def search_by_author(author_fullname):
    collection = db["quotes"]
    quotes_by_author = collection.find({'author': author_fullname})
    print(f"Всі цитати автора {author_fullname}:")
    for quote in quotes_by_author:
        print(quote['quote'])
    
# Пошук цитат за тегом
def search_by_tag(tag_name):
    collection = db["quotes"]
    # quotes_by_tag = collection.find({'tags': tag_name})
    quotes_by_tag = collection.find({'tags': tag_name})
    print(f"Цитати з тегом '{tag_name}'")
    # print(list(quotes_by_tag))
    for quote in quotes_by_tag:
        print(quote['quote'])

# Пошук цитат за тегами
def search_by_tags(tags):
    tag_list = tags.split(',')
    collection = db["quotes"]
    quotes_by_tags = collection.find({'tags': {'$in': tag_list}})
    print(f"Цитати з тегами '{tag_list}':")    
    for quote in quotes_by_tags:
        print(quote['quote'])
   
# # Основний цикл виконання скрипту
if __name__ == '__main__':
   
    while True:
        command = input("Введіть ім'я автора або тег: name:<author>, tag:<tag>, tags:<tag1,tag2>, або exit для виходу: ")
        parse_com = command.split(':')

        if parse_com[0] == 'name':
            author = parse_com[1].strip()
            search_by_author(author)
        elif parse_com[0] == 'tag':
            tag = parse_com[1].strip()
            search_by_tag(tag)
        elif parse_com[0] == 'tags':           
            tags = parse_com[1].strip()         
            search_by_tags(tags)
        elif parse_com[0] == 'exit':
            break
        else:
            print("Команда невідома, спробуйте ще раз, будь ласка!")






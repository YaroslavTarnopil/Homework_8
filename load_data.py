import json
from mongoengine import connect
from models import Author, Quote

# Підключення до MongoDB Atlas
connect(host="mongodb+srv://yaroslavtarnopil:<password>@cluster0.kqcceae.mongodb.net/")


# Завантаження даних з файлів JSON
def load_authors_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Author(
                fullname=author_data['fullname'],
                born_date=author_data['born_date'],
                born_location=author_data['born_location'],
                description=author_data['description']
            )
            author.save()

def load_quotes_from_json(file_path):
    authors_dict = {author.fullname: author for author in Author.objects}

    with open(file_path, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data['author']
            author = authors_dict.get(author_name)
            if author:
                quote = Quote(
                    tags=quote_data['tags'],
                    author=author,
                    quote=quote_data['quote']
                )
                quote.save()

# Завантаження даних у колекції authors
load_authors_from_json('authors.json')

# Завантаження даних у колекції quotes
load_quotes_from_json('quotes.json')

import re
import redis
from mongoengine import connect
from models import Author, Quote

# Підключення до MongoDB Atlas
connect(host="mongodb+srv://yaroslavtarnopil:<password>@cluster0.kqcceae.mongodb.net/")

# Підключення до Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def search_quotes(command):
    cached_result = redis_client.get(command)
    if cached_result:
        print("Знайдено в кеші:")
        return cached_result.splitlines()

    command_parts = command.split(':', 1)
    if len(command_parts) != 2:
        return []

    search_type, search_value = command_parts
    search_value = search_value.strip()

    if search_type == 'name':
        if len(search_value) >= 2:
            regex = re.compile(f".*{re.escape(search_value)}.*", re.IGNORECASE)
            authors = Author.objects(fullname__regex=regex)
        else:
            authors = Author.objects(fullname__startswith=search_value)

        author_ids = [author.id for author in authors]
        quotes = Quote.objects(author__in=author_ids)
    elif search_type == 'tag':
        tags = search_value.split(',')
        quotes = Quote.objects(tags__in=tags)
    elif search_type == 'tags':
        tags = search_value.split(',')
        quotes = Quote.objects(tags__in=tags)
    else:
        return []

    result = []
    for quote in quotes:
        result.append(f"Quote: {quote.quote}")
        result.append(f"Tags: {', '.join(quote.tags)}")
        result.append("-" * 80)

    redis_client.set(command, '\n'.join(result), ex=3600)  # Кешування на годину (3600 секунд)
    return result

if __name__ == '__main__':
    while True:
        command = input("Введіть команду (наприклад, name: Steve Martin або tag: life): ")
        if command.lower() == 'exit':
            break

        quotes = search_quotes(command)
        if quotes:
            for line in quotes:
                print(line)
        else:
            print("Нічого не знайдено.")

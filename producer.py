import pika
import json
from faker import Faker
from models import Contact
from mongoengine import connect

# Підключення до MongoDB
connect(host="mongodb+srv://yaroslavtarnopil:<password>@cluster0.kqcceae.mongodb.net/")

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Створення черг для SMS та email
channel.queue_declare(queue='sms_queue')
channel.queue_declare(queue='email_queue')

# Генерація фейкових контактів
fake = Faker()
num_contacts = 10  # Кількість контактів для створення

for _ in range(num_contacts):
    fullname = fake.name()
    email = fake.email()
    phone = fake.phone_number()

    # Випадкове вибирання способу надсилання
    send_via = fake.random_element(elements=('SMS', 'email'))

    # Збереження контакту у MongoDB
    contact = Contact(fullname=fullname, email=email, phone=phone, send_via=send_via)
    contact.save()

    # Відправка ID контакту у відповідну чергу RabbitMQ
    if send_via == 'SMS':
        queue_name = 'sms_queue'
    else:
        queue_name = 'email_queue'

    message = {'contact_id': str(contact.id)}
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=json.dumps(message))

    print(f"Added contact {fullname} with email {email} and phone {phone} to {queue_name}")

connection.close()

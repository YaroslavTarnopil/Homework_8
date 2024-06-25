import pika
import json
from models import Contact
from mongoengine import connect

# Підключення до MongoDB
connect(host="mongodb+srv://yaroslavtarnopil:<password>@cluster0.kqcceae.mongodb.net/")

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Створення черги для email
channel.queue_declare(queue='email_queue')

def send_email(contact_id):
    # Імітація відправки email
    contact = Contact.objects.get(id=contact_id)
    print(f"Sending email to {contact.email}...")

    # Позначення, що повідомлення відправлено
    contact.message_sent = True
    contact.save()
    print(f"Email sent to {contact.email}")

def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    
    # Обробка повідомлення
    send_email(contact_id)
    
    # Підтвердження обробки повідомлення
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Прослуховування черги для email
channel.basic_consume(queue='email_queue', on_message_callback=callback)

print('Waiting for email messages...')
channel.start_consuming()

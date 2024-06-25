import pika
import json
from models import Contact
from mongoengine import connect

# Підключення до MongoDB
connect(host="mongodb+srv://yaroslavtarnopil:<password>@cluster0.kqcceae.mongodb.net/")

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Створення черги для SMS
channel.queue_declare(queue='sms_queue')

def send_sms(contact_id):
    # Імітація відправки SMS
    contact = Contact.objects.get(id=contact_id)
    print(f"Sending SMS to {contact.phone}...")

    # Позначення, що повідомлення відправлено
    contact.message_sent = True
    contact.save()
    print(f"SMS sent to {contact.phone}")

def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    
    # Обробка повідомлення
    send_sms(contact_id)
    
    # Підтвердження обробки повідомлення
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Прослуховування черги для SMS
channel.basic_consume(queue='sms_queue', on_message_callback=callback)

print('Waiting for SMS messages...')
channel.start_consuming()

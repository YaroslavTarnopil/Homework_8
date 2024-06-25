from mongoengine import Document, StringField, ListField, ReferenceField, BooleanField

# Модель для автора
class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

# Модель для цитати
class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)
    
class Contact(Document):
    fullname = StringField(required=True)
    email = StringField()
    phone = StringField()
    message_sent = BooleanField(default=False)
    send_via = StringField(choices=('SMS', 'email'), default='email')    

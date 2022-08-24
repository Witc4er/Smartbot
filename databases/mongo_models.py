from datetime import datetime


from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField


class Tag(EmbeddedDocument):
    name = StringField()


class Record(EmbeddedDocument):
    description = StringField()
    done = BooleanField(default=False)


class Note(Document):
    name = StringField()
    created = DateTimeField(default=datetime.now())
    records = ListField(EmbeddedDocumentField(Record))
    tags = ListField(EmbeddedDocumentField(Tag))
    meta = {'allow_inheritance': True,
            'indexes': [
                {'fields': ['$name', '$records', '$tags'],
                 'default_language': 'russian',
                 'weights': {'name': 10, 'records': 5, 'tags': 2}}
            ]}
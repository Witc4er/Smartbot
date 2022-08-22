from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, text, JSON, Date
from sqlalchemy.sql.sqltypes import DateTime

from sqlalchemy.dialects.mysql import INTEGER
from datetime import datetime


Base = declarative_base()
metadata = Base.metadata


class AddressBook(Base):
    __tablename__ = 'addressbook'
    id = Column(INTEGER, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    address = Column(String)
    email = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f'1.Id: {self.id}\n2.Name: {self.name}\n3.Birthday: {self.birthday}\n4.Address: {self.address}\n5.Email: {self.email}\n6.Phone: {self.phone}\n'

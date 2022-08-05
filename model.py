from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, text, JSON, Date
from sqlalchemy.dialects.mysql import INTEGER


Base = declarative_base()
metadata = Base.metadata


class AddressBook(Base):

    __tablename__ = 'addressbook'

    id = Column(INTEGER(11), primary_key=True)
    personal_info = Column(JSON)
    created_on = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
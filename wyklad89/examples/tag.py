#!/usr/bin/env python
# coding=utf-8

from sqlalchemy import Column, String, SmallInteger, Integer, ForeignKey, create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Tag(Base):
    __tablename__ = "TAG"
    key = Column(String(), primary_key=True)
    label = Column(String())

    def __init__(self, key, label):
        self.key = key
        self.label = label

    def __eq__(self, other):
        return self.key == other.key and self.label == other.label

    def __repr__(self):
        return repr(u"<Tag {0.key}:{0.label}>".format(self))

engine = create_engine("sqlite://") # Baza danych w pamięci

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine) #Stworzenie tabeli Tag

session = Session()

session.add(Tag("status:student",  "Student")) # Tag dodany do sesji
session.add(Tag("status:doktorant",  "Doktorant"))
session.add(Tag("praca:inz",  u"Praca Inżynierska"))
session.commit() # Tagi wysłane do bazy danych i zapisany

query = session.query(Tag).filter(Tag.key.like("status:%"))

print(u"Treść zapytania")

print(query)

print(u"Wynoiki zapytania wybierającego wszystkie tagi")

print(session.query(Tag).all())

print(u"Wynoiki zapytania wybierającego statusy")

print(query.all())

print(u"Usuwamy tagi (te które są opisywane przez zapytanie query)")

print(query.delete('fetch'))

print(u"Wybieramy ponownie wszstkie tagi:")

print(session.query(Tag).all())








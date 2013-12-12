# coding=utf8
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine, Column, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer

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

class Student(Base):
    __tablename__ = "STUDENT"

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    surname = Column(String())
    gender = Column(SmallInteger())
    status = Column(String(), ForeignKey("TAG.key"))
    message = Column(String())


class Pracownik(Base):

    __tablename__ = "PRACOWNIK"

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    surname = Column(String())
    gender = Column(SmallInteger())
    tel_no = Column(String())


class PracaDyplomowa(Base):
    __tablename__ = "PRACA_DYPLOMOWA"


    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    tytul = Column(String(), nullable=False)
    type = Column(String(), ForeignKey("TAG.key"), primary_key=True)
    student_id = Column(Integer(), ForeignKey("STUDENT.id"), nullable=False, primary_key=True)
    promotor_id = Column(Integer(), ForeignKey("PRACOWNIK.id"), nullable=True)
    dyplomant = relation("Student", backref="prace_dyplomowe")
    promotor = relation("Pracownik", backref="prace_promowane")



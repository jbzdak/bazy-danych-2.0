# coding=utf8
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine, Column, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer

Base = declarative_base()

# Tu piszecie klasy modeli
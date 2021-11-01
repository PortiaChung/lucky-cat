from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from . import base

from .position import position

engine = create_engine("mysql+pymysql://root:password@localhost:3306/transaction")

if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(bind=engine, expire_on_commit=True)

base.Base.metadata.create_all(engine)
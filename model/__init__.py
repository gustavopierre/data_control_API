from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# import elements from model
from model.base import Base
# import elements from model.data
from model.data import Data

db_path = "database/"
# verify if the path exists
if not os.path.exists(db_path):
    # then create it
    os.makedirs(db_path)

# database url (this is a local sqlite url)
db_url = f'sqlite:///{db_path}/db.sqlite3'

# create a connection engine with the database
engine = create_engine(db_url, echo=False)

# Instance a session maker with the database
Session = sessionmaker(bind=engine)

# create the database if it doesn't exist
if not database_exists(engine.url):
    create_database(engine.url)

# create the tables in the database, if they don't exist
Base.metadata.create_all(engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

url= "sqlite:///./Database/popcorn.db"

Engine  = create_engine(url,connect_args ={"check_same_thread":False})
Session_ = sessionmaker(bind = Engine, autocommit = False, autoflush= False)
Base    = declarative_base()

def get_db():
    db = Session_()
    try:
        yield db
    finally:
        db.close()
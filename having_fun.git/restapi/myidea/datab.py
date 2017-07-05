from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()

class User(Base):
    __tablename__ = 'puppy'


    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    hash_password = Column(String(250))
   
    def hash_password(self, password):
      self.password_hash = pwd_content.encrypt(password)
    
    def verify_password(self, password):
      return pwd_context.verify(password,self.password_hash)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
       		'id': self.id,
           'name': self.name
       }
 


engine = create_engine('sqlite:///user.db')
Base.metadata.create_all(engine)

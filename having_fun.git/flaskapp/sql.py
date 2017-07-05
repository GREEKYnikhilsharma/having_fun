from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base as dec_b
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.orm import relationship, sessionmaker
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = dec_b()

from Crypto import Random
from random import randint
randomm = Random.new().read(randint(100,120438))

#testing
#import random,string
#randomm = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

class User(Base):
 __tablename__ = 'users'
 username = Column(String(20), nullable = False)
 userpassword = Column(String(50), nullable =False)
 userid = Column(String(20), primary_key = True)
 # user_username = Column(String(20), nullable = False)
 
 @property
 def serialize(self):
  return { 'email id':self.userid, 'name':self.username, 'password': self.userid }

 def hash_password(self, password):
        self.userpassword = pwd_context.encrypt(password)

 def verify_password(self, password):
        return pwd_context.verify(password, self.userpassword)

 def generate_auth_token(self, expiration=500):
  s = Serializer(randomm, expires_in = expiration) 
  return s.dumps({'emailid': self.userid})

 @staticmethod
 def verify_auth_token(token):
  s = Serializer(randomm)
  try:
   data = s.loads(token)
  except SignatureExpired:
   print('SignatureExpired')
   return None
  except BadSignature:
   print('BadSignature')
   return None
  user_id = data['emailid']
  return user_id

engine =  create_engine('sqlite:///users.db')

Base.metadata.create_all(engine)


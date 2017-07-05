from datab import Base, User
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from httplib2 import Http
from passlib.apps import custom_app_context as pwd_context

#dynamic url's
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

h=Http()

engine = create_engine('sqlite:///users.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


res_flag = False

@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@app.route('/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    hash = pwd_context.encrypt(password)
    if username is None or password is None:
        print "missing arguments"
        abort(400) 
        
    if session.query(User).filter_by(username = username).first() is not None:
        print "existing user"
        user = session.query(User).filter_by(username=username).first()
        return jsonify({'message':'user already exists'}), 200#, {'Location': url_for('get_user', id = user.id, _external = True)}
    data = dict(username = username, password = hash)
    data = json.dump(data)
     
    resp, content = h.request('http://localhost:5001/userAdd','POST',body = data, header = {"Content-Type : application/json"})
   # user = User(username = username)
   # user.hash_password(password)
   # session.add(user)
   # session.commit()
   # return jsonify({ 'username': user.username }), 201#, {'Location': url_for('get_user', id = user.id, _external = True)}

@app.route('/api/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.username })

nik = '/verifyy'
@app.route(nik,methods = ['POST'])
def display():
 
 if request.json.get('flag') == 'true':
  userID = request.json.get('id')
  userName = request.json.get('username')
  print('%s user successfully created with id = %s'%(username,userID))
  data = desc(ack='true')
  data = json.dump(data)
  resp, content = h.request(URL, 'POST', body = data, header = {"Content-Type" : "application/json"})
  return 0 #god knows

@app.route('/error')
def err():
  erro = request.json.get('error')
  print(erro)
  return 0
 
if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)

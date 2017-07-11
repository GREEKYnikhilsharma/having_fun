import json,httplib2,string,random
from sql import Base, User
from flask import Flask, jsonify, request, url_for, abort, g, redirect, make_response
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask_restful import Resource, Api
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from flask_security import auth_token_required
from requests import get,post
CLIENT_ID = json.loads(open('client_secrets.json','r').read())

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

engine = create_engine('sqlite:///users.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@auth.verify_password
def verify_password(username, password):
    user_id = User.verify_auth_token(username)
    print(user_id)
    if user_id:
     user = session.query(User).filter_by(userid = user_id).one()
    else:
     user = session.query(User).filter_by(userid = username).first()
     if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@app.route('/users', methods = ['POST'])
def new_user():
    username = request.json['username']#.get('username').encode('utf-8')
    password = request.json['password']#.get('password').encode('utf-8')
    emailid = request.json['emailid']#.get('emailid').encode('utf-8')
    if username is None or password is None or emailid is None:
        print "missing arguments"
        abort(400) 
        
    if session.query(User).filter_by(userid = emailid).first() is not None:
        print "existing user"
        user = session.query(User).filter_by(userid=emailid).first()
        return jsonify({'message':'user already exists'})        
    user = User(username = username,userid = emailid)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({'message': user.username })#,200 


@app.route('/api/users/<string:id>')
def get_user(id):
    try:
     user = session.query(User).filter_by(userid=id).one()
     if not user:
        abort(400)
     return jsonify({'username': user.username}),200
    except Exception as e:
      return jsonify({'username':'Anonymous'})
      abort(400)

#maintain another method for login and token return?

@app.route('/api/resource',methods = ['POST'])
@auth.login_required
def get_resource():
 try:
    return jsonify({ 'data': 'Hello, %s!' % g.user.username }),200
 except Exception as e:
    return jsonify({'data':'Welcome user'})

@app.route('/token')
@auth.login_required
def get_auth_token():
 token = g.user.generate_auth_token()
 return jsonify({'token': token.decode('ascii')})

@app.route('/oauth/<provider>', methods = ['POST'])
def login(provider):
 auth_code = request.json.get('token')
 
 print "Step 1 - Parse the auth code"
 if provider == 'google':
  
  try:
   
   oauth_flow = flow_from_clientsecrets('client_secrets.json',scope='')
   
   oauth_flow.redirect_uri = 'postmessage'
   
   credentials = oauth_flow.step2_exchange(auth_code)
  
  except FlowExchangeError:
   #response = json.dumps("Failed to upgrade the authorization code.")
   #response.headers['Content-Type'] = 'application/json'
   return {'aa':'yayaya'}
  access_token = credentials.access_token
  
  url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
  h = httplib2.Http()
  
  result = json.loads(h.request(url,'GET')[1])
  
  
  if result.get('error') is not None:
   print('Test failed after access token')
   return json.dumps(result.get('error'))
  gplus_id = credentials.id_token['sub']
  
  if result['user_id'] != gplus_id:
   print('trap 1')
   return json.dumps("Token's user ID doesn't match given user ID.")

  if result['issued_to'] != CLIENT_ID['web']['client_id']:
    print('trap 2')
    return json.dumps("Token's client ID doesn't match app's.")
  
  print('STEP 2 complete ! Access token : %s' % credentials.access_token)
  h = httplib2.Http()
  userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
  params = {'access_token' : credentials.access_token, 'alt':'json'}
  answer  = get(userinfo_url,params=params)
  data = answer.json()
  name = data['name']
  email = data['email']
  # continued 
  user = session.query(User).filter_by(userid=email).first()
  if not user:
   user = User(username = name, userid = email)
   user.hash_password(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(1000)))
   print('passed1')
   session.add(user)
   session.commit()
  
  token = user.generate_auth_token()
  print('success')
  #a=post('http://localhost:5009/api/resource',json={'token':token},auth=(token,'anon')).json()
  return jsonify({'token':token.decode('ascii'),'email':email})
  
 else:
  return 'Unrecognised Provider'

if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True,port=5009)

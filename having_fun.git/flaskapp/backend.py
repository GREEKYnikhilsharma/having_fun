from sql import Base, User
from flask import Flask, jsonify, request, url_for, abort, g, redirect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask_restful import Resource, Api


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
    username = request.json.get('username').encode('utf-8')
    password = request.json.get('password').encode('utf-8')
    emailid = request.json.get('emailid').encode('utf-8')
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
    return jsonify({ 'message': user.username }),200 

@app.route('/api/users/<string:id>')
def get_user(id):
    user = session.query(User).filter_by(userid=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username}),200

@app.route('/api/resource',methods = ['POST'])
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.username }),200

@app.route('/token')
@auth.login_required
def get_auth_token():
 token = g.user.generate_auth_token()
 return jsonify({'token': token.decode('ascii')})


if __name__ == '__main__':
    app.debug = True
    app.run( port=5009)

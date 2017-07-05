from datab import Base, User
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import httplib2,json
from flask.ext.httpauth import HTTPBasicAuth

from passlib.apps import custom_app_context as pwd_context

auth = HTTPBasicAuth()

h = httplib2.Http()

engine = create_engine('sqlite:///users.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@app.route('/userAdd', methods = ['POST'])
def new_user():
    usernam = request.json.get('username')
    passwor = request.json.get('password')
    if usernam is None or passwor is None:
        print "missing arguments"
        data = dict(error='missing arguments')
        data = json.dump(data)
        return h.request('http://localhost:5000/error','POST',body=data,header={'Content-Type:application/json'})
         
        
    if session.query(User).filter_by(usernam = usernam).first() is not None:
        print "existing user"
        user = session.query(User).filter_by(usernam=usernam).first()
        return jsonify({'message':'user already exists'}), 200#, {'Location': url_for('get_user', id = user.id, _external = True)}
        
    user = User(usernam = usernam)
    user.hash_password(passwor)
    session.add(user)
    session.commit()
    return jsonify({ 'username': user.username }), 201#, {'Location': url_for('get_user', id = user.id, _external = True)}

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



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)

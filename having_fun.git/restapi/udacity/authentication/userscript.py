from usersql import Base, User
from flask import Flask, jsonify, request, url_for, abort,g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from flask.ext.httpauth import HTTPBasicAuth as hba
auth=hba()

engine = create_engine('sqlite:///users.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@auth.verify_password
def verify_password(username_or_token, password):
    #Try to see if it's a token first
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id = user_id).one()
    else:
        user = session.query(User).filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route('/token')
@auth.login_required
def get_auth_login():
  token = g.user.generate_auth_token()
  return jsonify({'token':token.decode('ascii')})

@app.route('/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
     print('Missing argument')   
     abort(400) # missing arguments
    if session.query(User).filter_by(username = username).first() is not None:
     print('Existing user')
     user = session.query(User).filter_by( username = username ).first()  
     return jsonify({'message':'user already exists'}), 200, {'Location': url_for('get_user', id = user.id, _external = True)}
    user = User(username = username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}

@app.route('/api/allusers')
@auth.login_required
def all_user():
 usr = session.query(User).all()
 return jsonify(ps = [i.serialize for i in usr])

@app.route('/api/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/resource')
@auth.login_required
def get_resource():
 return jsonify({'data':'Hello,%s!!' % g.user.username})

if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)

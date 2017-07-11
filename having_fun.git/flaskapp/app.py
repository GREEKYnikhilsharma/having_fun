from flask import Flask, render_template, json, request,redirect,session, url_for,jsonify
#from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask_restful import Resource,Api
import httplib2 as http
import json,re
from requests import put,get,post
#from urlparse import urlparse

import webbrowser,pyautogui

#generating_random_numbers
#from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256
random_generated = Random.new().read(1234)
#key = RSA.generate(1024, random_generator)
undefined=SHA256.new(Random.get_random_bytes(100000)).hexdigest()

app=Flask(__name__)
app.secret_key = random_generated

#task: OAuTH authentication

@app.route('/')
def main():
    if session.get('user'):
     return redirect('/userHome')
    else:
     return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    #undefined=SHA256.new(Random.get_random_bytes(100000)).hexdigest()
    if session.get('user'):
     #someday open the secret pathway 
     #return redirect('/' + undefined)
     return redirect('/userHome')
    else:
     return render_template('signup.html')

@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('signin.html')

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user',None)
    #session['logged_in'] = False
    return redirect('/')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    
    try:
        _useremail = request.form['inputEmail']
        _password = request.form['inputPassword']
         
        #its better to send only one request work on it
        a11=get('http://localhost:5009/token',auth=(_useremail,_password)).json()
        a1=post('http://localhost:5009/api/resource',auth=(a11['token'].encode('utf-8'),'Anon')).json()
        print(a1)
        
        p = re.compile('Hello,*')
        print('testing')
        if p.match(a1['data'].encode('utf-8')):
          print('Welcome user')
          #session['logged_in'] = True
          session['user'] = _useremail
          return redirect('/userHome')
        else:
          print('Probably incorrect credentials ')
          return render_template('error.html',error = 'Wrong Email address or Password.')        
    except Exception as e:
      print(e)
      return render_template('error.html',error = str(e))

@app.route('/signUp',methods=['POST'])
def signUp():
    try:
        
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        
        if _name and _email and _password:
         res = post('http://localhost:5009/users',json={"emailid":_email,"username":_name,"password":_password}).json()        
         print(res)
         
         
         if res['message'].encode('utf-8') == _name:
                aaaa = json.dumps({'message':'User created successfully !'})                
                return render_template('NewUser.html')
         elif res['message'].encode('utf-8') == 'user already exists':
                bbb = json.dumps({'error':res['message']})
                print(bbb)
                return render_template('error.html',error = 'User already exists')
                #return json.dumps({'html':'<span>user already exist</span>'})
         else:
           print('out of the box')
        else:
           print('aaa')
           return render_template('error.html',error = "Enter the required fields") 
           #return json.dumps({'html':'<span>Enter the required fields</span>'})
    
    except Exception as e:
        print('hi')
        print(e)
        return render_template('error.html', error = e)
        #return json.dumps({'error':str(e)})

@app.route('/oauth/send',methods=['POST'])
def send():
 try:
  onetimeauth = request.data  
  token = post('http://localhost:5009/oauth/google',json={ 'token' : onetimeauth }).json()
  print('hohohohoho')
  a1=post('http://localhost:5009/api/resource',auth=(token['token'],'Anon')).json()
  print(a1)
  p = re.compile('Hello,*')
  if p.match(a1['data'].encode('utf-8')):
     print('Welcome user')
     session['user'] = token['email']
     return redirect('/userHome')
  else:
     print('Probably incorrect credentials ')
     return render_template('error.html',error = 'Wrong Email address or Password.')
 except Exception as e:
   print(e)
   return render_template('error.html',error = str(e))

@app.route('/' + undefined)
def aa():
   return "Welcome Anon"

if __name__ == "__main__":
    app.run(threaded=True,port=5002)

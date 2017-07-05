from flask import Flask, render_template, json, request,redirect,session, url_for
#from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask_restful import Resource,Api
import httplib2 as http
import json,re
from requests import put,get,post
#from urlparse import urlparse

#generating_random_numbers
#from Crypto.PublicKey import RSA
from Crypto import Random
random_generated = Random.new().read(1234)
#key = RSA.generate(1024, random_generator)


app = Flask(__name__)
app.secret_key = random_generated

@app.route('/')
def main():
    if session.get('user'):
     return redirect('/userHome')
    else:
     return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    if session.get('user'):
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
    return redirect('/')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _useremail = request.form['inputEmail']
        _password = request.form['inputPassword']
       
        a1=post('http://localhost:5009/api/resource',auth=(_useremail,_password)).json()
        print(a1)
        # connect to mysql
        p = re.compile('Hello,*')
        print('testing')
        if p.match(a1['data'].encode('utf-8')):
          print('Welcome user')
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
                print(aaaa)
                return redirect('/')
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
        print(e)
        return render_template('error.html', error = e)
        #return json.dumps({'error':str(e)})

if __name__ == "__main__":
    app.run(port=5002)

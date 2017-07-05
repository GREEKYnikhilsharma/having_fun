from flask import Flask,request
import json
app=Flask(__name__)

@app.route('/')
def aa():
 d={username'nik',pas='pass'}

 d=json.load(d)

 return d

if __name__ == '__main__':
 app.run()

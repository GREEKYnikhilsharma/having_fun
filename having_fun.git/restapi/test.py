from __future__ import with_statement
from flask import Flask,request,jsonify
import pickle

app=Flask(__name__)

#base data set
#language=[{'quote':'anything_is_possible'},{'quote':'will_power'},{'quote':'Stay_true'}]

#reading the file
with open('data.json','rb') as fox:
 language = pickle.load(fox)

#language=[e.strip() for e in language]

#Writing the File
#filee=open('data.json','wb')
#pickle.dump(language, filee, protocol=pickle.HIGHEST_PROTOCOL)

#sample
#for item in language:
# filee.write("%s\n"%item)
#for item in language:
# json.dump(item,filee)
#filee.close()

@app.route('/',methods=['GET'])
def testing():
 return jsonify({'hi':'bye'})

@app.route('/l',methods=['GET'])
def display():
 return jsonify({'quote':language})

@app.route('/<string:name>',methods=['GET'])
def data(name):
 lang=[la for la in language if la['quote'] == name]
 return jsonify({'language':lang[0]})

#Now POST methods!!!!!!!!!! and  database!!!!!!!!!!!!!!
@app.route('/',methods=['POST'])
def inp():
 lang={'quote':request.json['quote']}
 language.append(lang)
 return jsonify({'languages':language})

@app.route('/save',methods=['POST'])
def savee():
 f=open('data.json','wb')
 pickle.dump(language, f, protocol=pickle.HIGHEST_PROTOCOL)
 return jsonify({'languages':language})

#PUT method
@app.route('/putm/<string:name>',methods=['PUT'])
def editt(name):
 langs = [lanz for lanz in language if lanz['quote'] == name]
 langs[0]['quote']=request.json['quote']
 return jsonify({'quote':langs[0]})

#DELETE method
@app.route('/del/<string:name>',methods=['DELETE'])
def remo(name):
 lang = [lanz for lanz in language if lanz['quote'] == name ]
 language.remove(lang[0])
 return jsonify({'quote':language})

if __name__=='__main__':
 app.run()

from flask import Flask,request
app = Flask(__name__)
 
@app.route('/puppies',methods=['GET','POST'])
def puppiesFunction():
 if request.method == 'GET':
  return getAllPuppies()
 elif request.method == 'POST':
  return makeANewPuppy()

@app.route('/puppies/<int:id>',methods=['GET','PUT','DELETE'])
def puppiesFunctionId(id):
 if request.method == 'GET':
  return getPuppy(id)
 elif request.method == 'PUT':
  return updatePuppy(id)
 elif request.method == 'DELETE':
  return deletePuppy(id)


def getAllPuppies():
 return "Getting puppies"

def makeANewPuppy():
 return "making a new puppy"

def getPuppy(id):
 return "getting Puppy with id %s" % id

def updatePuppy(id):
 return "updating puppy with id %s" % id

def deletePuppy(id):
 return "Removing Puppy with id %s" % id

if __name__ == '__main__':
 app.run(port=5000)

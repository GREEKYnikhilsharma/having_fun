from flask import Flask
app = Flask(__name__)

@app.route('/puppies',methods=['GET'])
def puppiesFunction():
 return "Hello puppies"
 
@app.route('/puppies/<int:id>',methods=['GET'])
def puppiesFunctionId(id):
 return "This method will return %s puppies"%id

if __name__ == "__main__":
 app.run(host='0.0.0.0')

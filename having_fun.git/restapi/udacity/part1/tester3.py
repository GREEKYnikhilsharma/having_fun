import httplib2,json,sys

print("Running endpoint tester\n")
address = raw_input('Please enterthe address:')
if address == '':
 address ='http://localhost:5000'

print('Making POST request to /puppies')
try:
 url =address+'/puppies?name=Fido&description=Playful+Little+Puppy' 
 h = httplib2.Http()
 resp, result = h.request(url, 'POST')
 obj = json.load(result)
 puppyID = obj['Puppy']['id']
 if resp['status'] != "200":
  raise Exception('Recieved an unsuccessful sattus code of %s'% resp['status'])
except Exception as err:
 print('Test 1 failed')
 print(err.args)
 sys.exit()
else:
 print('Test1 passed successfullY')

print('Making GET request for /puppies')
try:
 url =  address + '/puppies'
 h = httplib2.Http()
 resp, result = h.request(url, 'GET')
 if resp['status']!= "200":
  raise Exception('Received an wrong status code %s'%resp['status'])
except Exception as err:
 print('Test 2 failed ')
 print(err.args)
 sys.exit() 
else:
 print('TEst 2 is successful')

print('Making GET request to puppies/id')
try:
 id = puppyID 
 url = address + '/puppies/%s' % id
 h = httplib2.Http()
 resp, result = h.request(url,'GET')
 if resp['status'] != "200":
  raise Exception("Wrong status code %s" % resp['status'])
except Exception as err:
 print('Test 3 will succedd')
 print(err.args)
 sys.exit()
else:
 print('Test 3 is successful')

print('Sending PUT request on puppies/id')
try:
 id = puppyID
 url = address + 'puppies/%s?name=wilma&description=A+sleepy+bundle+of+joy' % id
 h = httplib2.Http()
 resp, result = h.request(url,'PUT')
 if resp['status'] != "200":
  raise Exception('wrong status code %s'%resp['status'])
except Exception as err:
 print('Test 4 will be successful')
 print(err.args)
 sys.exit()
else:
 print('Test 4 is successful')

print("making DELETE request to /puppies/id")
try:
 id = puppyID
 url = address + '/puppies/%s' % id
 h = httplib2.Http()
 resp, result = h.request(url,'DELETE')
 if resp['status']!='200':
  raise Exception('Wrong status code %s'%resp['status'])
except Exception as err:
 print('Test 5 cannot make GET request')
 print(err.args)
 sys.exit()
else:
 print('Test 5 is successful') 

print('all test clear')

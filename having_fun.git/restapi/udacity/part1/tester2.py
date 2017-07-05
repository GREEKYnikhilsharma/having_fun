import httplib2,json,sys

print("running endpoint tester\n")
address = raw_input('Enter the address')
if address == '':
 address = 'http://localhost:5000'
print("making the GET request for /puppies")
try:
 url = address +'/puppies'
 h = httplib2.Http()
 resp, result = h.request(url, 'GET')
 print('Header = %s \n body = %s \n' % (resp,result))
 if resp['status'] != '200':
  raise Exception('Received an uncessful staus code of %s' % resp['status'])
except Exception as err:
 print('Test1 failed')
 print(err.args)
 sys.exit()
else:
 print('Test1 pass: Successfully made get request to /puppies')

print('MAking POST request to puppies')

try:
 url = address + '/puppies'
 h = httplib2.Http()
 resp, result = h.request(url, 'POST')
 print('Header = %s \n Body = %s \n'%(resp,result))
 if resp['status'] != '200':
  raise Exception('Received an uncessful satus code of %s' % resp['status'])

except Exception as err:
 print 'TEst 2 failed'
 print err.args
 sys.exit()

else:
 print('TEst 2 passsed')

print('Now making GET request to specific puppy')
try:
 id = 1
 while id<=10:
  url = address +'/puppies/%s' % id
  h = httplib2.Http()
  resp,result = h.request(url, 'GET')
  if resp['status'] != '200':
   raise Exception('Reciende an uncessful staus code of %s' % resp['status'])
  id = id + 1
 
except Exception as err:
 print('Test 3 - failure are the stepping stone to success')
 print(err.args)
 sys.exit()
else:
 print('Test 3 passed')

print('NOw making PUT request to specific puppy')
try:
 id = 1
 while id <=10:
  url = address + '/puppies/%s' % id
  h = httplib2.Http()
  resp, result = h.request(url,'PUT')
  if resp['status'] != '200':
   raise Exception('Received an uncessful status code of %s'%resp['status'])
  id = id + 1
except Exception as err:
 print('Test 4 - keep on  movingn forward')
 print(err.args)
 sys.exit()

else:
 print('TEst 4 is successful')

print('Now making DELETE request to specific puppy')
try:
 id = 1
 while id <= 10:
  url = address + '/puppies/%s' % id
  h = httplib2.Http()
  resp, result = h.request(url, 'DELETE')
  if resp['status'] != '200':
   raise Exception('Received an uncessful staus code of %s' % id)
  id = id + 1

except Exception as err:
 print('TEst 5 - failure are learining')
 print(err.args)
 sys.exit()
else:
 print('Test 5 passed')
print('All TEst done')

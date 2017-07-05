import httplib2
import json
import sys
print("Running the tester")
address = raw_input("Enter the address:")
if address == '':
 address = 'http://0.0.0.0:5000'
print('Making a GET request for /puppies')
try:
  url = address + '/puppies'
  h = httplib2.Http()
  resp, result = h.request(url, 'GET')
  if resp['status'] != '200':
   raise Exception('Received an unsuccessful status code of %s' % resp['status'])
except Exception as err:
  print('Test1 dailed')
  print(err.args)
  sys.exit()
else:
  print('Test1 passed successfully header=%s \n body=%s \n' %(resp,result) )

print('NOw making GET request to /pupies/id')
try:
 id = 1
 for id in range(8):
  url = address +'/puppies/%s' % id
  resp, result = h.request(url, 'GET')
  print('Header = %s\n body = %s\n' % (resp,result))
  if resp['status'] != '200':
   raise Exception('Reived an uncessful status code %s' % resp['status'])
except Exception as err:
 print('Test 2 Failed: could not make a GET request')
 print(err.args)
 sys.exit()
else:
 print('All test passed !!!!!!')

import httplib2,json,sys
#print(sys.argv[1:3])
aa = ''.join(sys.argv[1:2])
bb = ''.join(sys.argv[2:3])
print ('%s %s\n' % (aa,bb))
data = dict(username = aa, password = bb)
data =json.dumps(data)
h = httplib2.Http()
url = 'http://localhost:5000/users'
a,b = h.request(url,'POST',body = data, headers = {"Content-Type":"application/json"})

print(a)
print(b)

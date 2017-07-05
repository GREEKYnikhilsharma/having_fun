import httplib2,json,sys
def getData(inputd):
 url = ('http://localhost:5000/%s'% (inputd))
 h = httplib2.Http()
 response, content = h.request(url,'GET')
 result = json.loads(content)
 #print('header ',response)
 return result

if __name__ == '__main__':
 print(getData(sys.argv[1:]))

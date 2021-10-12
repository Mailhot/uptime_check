import httplib2
h = httplib2.Http()



resp = h.request("http://www.google.com", 'HEAD')
assert int(resp[0]['status']) < 400
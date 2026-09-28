import urllib

url = 'https://gdcatalog.go.th/api/3/action/datastore_search?limit=5&resource_id=e4f2616f-b405-4178-8491-9f4744b7bd29&q=title:jones'
fileobj = urllib.request.urlopen(url)
print(fileobj.read())
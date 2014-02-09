import urllib2
import simplejson as json
response=urllib2.urlopen('https://graph.facebook.com/htc/feed?access_token=334601356657560|ecff84f4f5701accddb66546a8a83a6e')
html=response.read()

test = json.loads(html)

#file=open('jsondecode.txt','w')
#for i in test:
#    file.write(i+'\n')
#file.close()

print test['data'][0]['id']

for message in test['data']:
	print message.get('like')

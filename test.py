import csv  
f = open('Opview.csv', 'r') 
leaders={}
count=0
for row in csv.reader(f):
	if row[9] in leaders:
		leaders[row[9]]=leaders[row[9]]+1
	else:
		leaders[row[9]]=1
sortleaders= sorted(leaders.iteritems(), key=lambda d:d[1], reverse = True)
print sortleaders 
f.close()

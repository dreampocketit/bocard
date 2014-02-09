<<<<<<< HEAD
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
=======
import pygal                                                       # First import pygal
from datetime import datetime, timedelta
datey = pygal.DateY(x_label_rotation=20)
datey.add("Visits", [
    (datetime(2013, 1, 2), 300),
    (datetime(2013, 1, 12), 412),
    (datetime(2013, 2, 2), 823),
    (datetime(2013, 2, 22), 672)
])
datey.render_to_file('test.svg')
#bar_chart.render_to_file('bar_chart.svg')                          # Save the svg to a file
>>>>>>> 41b3ae03ace694cde860feaf2074c2f3a8998dcf

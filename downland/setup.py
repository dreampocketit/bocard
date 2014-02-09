import urllib2
 
# file to be written to
file = "downloaded_file.html"
 
url = "https://www.google.com.tw/"
response = urllib2.urlopen(url)
 
#open the file for writing
fh = open(file, "w")
 
# read from request while writing to file
fh.write(response.read())
fh.close()
 
# You can also use the with statement:

import urllib2,urllib  
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import urllib2
from dateutil import parser
#!/usr/bin/python
# -*- coding: utf-8 -*-
  
url = 'http://www.google.com/trends/explore#q=氣炸鍋&cmpt=q'  
req = urllib2.Request(url)  
content = urllib2.urlopen(req).read() 
print content

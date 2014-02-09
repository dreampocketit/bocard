# -*- coding: big5 -*-
# This module is used to decompose a character's linguistic component
# 2011/12/6 created by Bo-Shun Liao
# 2012/1/5 new version has integrated with previous NLTK tools in one command
import codecs, sys, os, re
from collections import defaultdict
import NLTK_tools
if sys.getdefaultencoding() != 'utf-8':
  reload(sys)
  sys.setdefaultencoding('utf-8') 

class Char2Any():

  def __init__(self):
    self.char2strokes = defaultdict(int)
    self.char2consonant = defaultdict(list)
    self.char2vowel = defaultdict(list)
    self.char2phone = defaultdict(list)
    self.char2tone = defaultdict(list)
    self.char2up_tone = defaultdict(list)
    self.char2down_tone = defaultdict(list)
    self.char2number = defaultdict(int)
    self.consonant = defaultdict(int)
    self.vowel = defaultdict(int)
    self.consonant.update(# �n���r��
      {u'�t':1,u'�u':1,u'�v':1,u'�w':1,u'�x':1,u'�y':1,u'�z':1,u'�{':1,
       u'�|':1,u'�}':1,u'�~':1,u'��':1,u'��':1,u'��':1,u'��':1,u'��':1,
       u'��':1,u'��':1,u'��':1,u'��':1,u'��':1}
    )
    self.vowel.update(# �����r��
      {u'��':1,u'��':1,u'��':1,u'��':1,u'��':1,u'��':1,u'��':1,u'��':1,
       u'��':1,u'��':1,u'��':1,u'��':1,u'��':1,u'��':1,u'��':1,u'��':1}
    )
    self.char2number.update(
      {u'�@':1,u'�G':2,u'�T':3,u'�|':4,u'��':5,u'��':6,u'�C':7,u'�K':8,
       u'�E':9,u'�Q':10,u'��':12,u'�d':13,u'�U':14}
    )
    f1 = codecs.open('char2stroke.txt', 'rb', 'big5', 'ignore')
    for line in f1:
      if line[0] != '?': # for now only handle chinese traditional characters
        #print line[0]
        #print line[line.find("\t", 0)+1:line.find("\t", line.find("\t", 0)+1)]
        self.char2strokes[line[0]] = int(line[line.find("\t", 0)+1:line.find("\t", line.find("\t", 0)+1)])
    self.char2strokes.update(# punctuations
      {u'�C':u'�C', u'�H':u'�H', u'�I':u'�I', u'�A':u'�A', u'�B':u'�B',
      ',':',', '.':'.', '?':'?', '!':'!'}
    )
    f2 = codecs.open('char2phone.txt', 'rb', 'big5', 'ignore')
    for line in f2:
      #for p in line[4:line.find("\s", 4)].split(' '): print p
      #print len(line[4:line.find("\s", 4)])
      phone = ''; phone = line[4:line.find("\s", 4)]
      for i in range(len(phone)):
        #print 'i=',phone[i],'i-1=',phone[i-1]
        if self.consonant.has_key(phone[i]):
          self.char2consonant[line[0]].append(phone[i]) # �r�����n���r��
        elif self.vowel.has_key(phone[i]):
          self.char2vowel[line[0]].append(phone[i]) # �r���������r��
        # �r�����n�զr��
        elif phone[i] in u'��':
          self.char2tone[line[0]].append('2') # �O�_���G�n
          self.char2up_tone[line[0]].append('2')
        elif phone[i] in u'��':
          self.char2tone[line[0]].append('3') # �O�_���T�n
          self.char2down_tone[line[0]].append('3')
        elif phone[i] in u'��':
          self.char2tone[line[0]].append('4') # �O�_���|�n
          self.char2down_tone[line[0]].append('4')
        elif phone[i] in u'��':
          self.char2tone[line[0]].append('5') # �O�_�����n
        elif phone[i] not in "\n\r":
          self.char2vowel[line[0]].append(phone[i])# �ϧO�����������ť�
        elif phone[i] in " \r" and phone[i-1] not in u'��������':
          self.char2tone[line[0]].append('1') # �O�_���@�n
          self.char2up_tone[line[0]].append('1')

      if len(line[4:line.find("\s", 4)]) > 4: 
        self.char2phone[line[0]] = line[4:line.find("\s", 4)].split() # ���}���r
      else:
        self.char2phone[line[0]] = line[4:line.find(' ', 4)] # �S���}���r 

  def char2stroke(self, word):
    if self.char2strokes[word] > 0:
      return self.char2strokes[word]
    else:
      return 'no strokes or an English word'
  
  def phonetic_symbols(self, word):
    if isinstance(self.char2phone[word], list):
      symbols = word+':'
      for phones in self.char2phone[word]: symbols += phones
      return symbols
    else:
      return word+':'+self.char2phone[word]

  def phones(self, word):
    if len(self.char2consonant[word]) > 0 and len(self.char2vowel[word]) > 0:
      phones = word+'<consonant>: '
      for cons in self.char2consonant[word]: phones += cons
      phones += "\n"+word+'<vowels>: '
      for vows in self.char2vowel[word]: phones += vows
      return phones
    elif len(self.char2consonant[word]) == 0:
      phones = word+'<consonant>: no consonant'
      phones += "\n"+word+'<vowels>: '
      for vows in self.char2vowel[word]: phones += vows
      return phones
    else:
      phones = word+'<consonant>: '
      for cons in self.char2consonant[word]: phones += cons
      phones += "\n"+word+'<vowels>: no vowels'
      return phones

  def tones(self, word):
    tones = word+'<tone>: '
    for tone in self.char2tone[word]: tones += tone
    return tones
  
  def sumofstroke1(self, text):
    strokesum = 0
    for t in text:
      if isinstance(self.char2stroke(t), int): strokesum += self.char2stroke(t)
    print 'The sum of all stroke: ',strokesum
  
  def sumofstroke2(self, text):
    strokesum = 0
    for t in text:
      for w in t:
        if isinstance(self.char2stroke(w), int): strokesum += self.char2stroke(w)
    print 'The sum of all stroke: ',strokesum
   
  def showallstroke1(self, text, dir_name , num=40):
    num = min(len(text),num)
    if num == len(text):
      for t in text:
        if isinstance(self.char2stroke(t), int): print t+':'+str(self.char2stroke(t))
    else:
      if os.name == 'nt':
        print 'too many to show, save to file :\nall_stroke.txt(in '+os.getcwd()+'\\result\\'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result\\'+dir_name+'\\all_stroke.txt', 'w')
      elif os.name == 'posix':
        print 'too many to show, save to file :\nall_stroke.txt(in '+os.getcwd()+'/result/'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result//'+dir_name+'//all_stroke.txt', 'w')
      for t in text:
        if isinstance(self.char2stroke(t), int): result.write(t+':'+str(self.char2stroke(t)))
      result.close()

  def showallstroke2(self, text, dir_name , num=40):
    num = min(len(text),num)
    if num == len(text):
      for t in text:
      	for w in t:
          if isinstance(self.char2stroke(w), int): print w+':'+str(self.char2stroke(w))
    else:
      if os.name == 'nt':
        print 'too many to show, save to file :\nall_stroke.txt(in '+os.getcwd()+'\\result\\'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result\\'+dir_name+'\\all_stroke.txt', 'w')
      elif os.name == 'posix':
        print 'too many to show, save to file :\nall_stroke.txt(in '+os.getcwd()+'/result/'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result//'+dir_name+'//all_stroke.txt', 'w')
      for t in text:
        for w in t:
          if isinstance(self.char2stroke(w), int): result.write(w+':'+str(self.char2stroke(w))+'\n')
      result.close()

  def showallphonesymbol1(self, text, dir_name , num=40):
    num = min(len(text),num)
    if num == len(text):
      for t in text:
        if isinstance(self.char2stroke(t), int): print self.phonetic_symbols(t)
    else:
      if os.name == 'nt':
        print 'too many to show, save to file :\nall_phonetic_symbols.txt(in '+os.getcwd()+'\\result\\'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result\\'+dir_name+'\\all_phonetic_symbols.txt', 'w')
      elif os.name == 'posix':
        print 'too many to show, save to file :\nall_phonetic_symbols.txt(in '+os.getcwd()+'/result/'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result//'+dir_name+'//all_phonetic_symbols.txt', 'w')
      for t in text:
        if isinstance(self.char2stroke(t), int): result.write(self.phonetic_symbols(t)+"\n")
      result.close()

  def showallphonesymbol2(self, text, dir_name , num=40):
    num = min(len(text),num)
    if num == len(text):
      for t in text:
      	for w in t:
          if isinstance(self.char2stroke(w), int): print self.phonetic_symbols(w)
    else:
      if os.name == 'nt':
        print 'too many to show, save to file :\nall_phonetic_symbols.txt(in '+os.getcwd()+'\\result\\'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result\\'+dir_name+'\\all_phonetic_symbols.txt', 'w')
      elif os.name == 'posix':
        print 'too many to show, save to file :\nall_phonetic_symbols.txt(in '+os.getcwd()+'/result/'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result//'+dir_name+'//all_phonetic_symbols.txt', 'w')
      for t in text:
        for w in t:
          if isinstance(self.char2stroke(w), int): result.write(self.phonetic_symbols(w)+"\n")
      result.close()

  def showallphone1(self, text, dir_name , num=40):
    num = min(len(text),num)
    if num == len(text):
      for t in text:
        if isinstance(self.char2stroke(t), int): print self.phones(t)
    else:
      if os.name == 'nt':
        print 'too many to show, save to file :\nall_phones.txt(in '+os.getcwd()+'\\result\\'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result\\'+dir_name+'\\all_phones.txt', 'w')
      elif os.name == 'posix':
        print 'too many to show, save to file :\nall_phones.txt(in '+os.getcwd()+'/result/'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result//'+dir_name+'//all_phones.txt', 'w')
      for t in text:
        if isinstance(self.char2stroke(t), int): result.write(self.phones(t)+'\n')
    result.close()

  def showallphone2(self, text, dir_name , num=40):
    num = min(len(text),num)
    if num == len(text):
      for t in text:
      	for w in t:
          if isinstance(self.char2stroke(w), int): print self.phones(w)
    else:
      if os.name == 'nt':
        print 'too many to show, save to file :\nall_phones.txt(in '+os.getcwd()+'\\result\\'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result\\'+dir_name+'\\all_phones.txt', 'w')
      elif os.name == 'posix':
        print 'too many to show, save to file :\nall_phones.txt(in '+os.getcwd()+'/result/'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result//'+dir_name+'//all_phones.txt', 'w')
      for t in text:
        for w in t:
          if isinstance(self.char2stroke(w), int): result.write(self.phones(w)+'\n')
      result.close()

  def showalltone1(self, text, dir_name , num=40):
    num = min(len(text),num)
    if num == len(text):
      for t in text:
        if isinstance(self.char2stroke(t), int): print self.tones(t)
    else:
      if os.name == 'nt':
        print 'too many to show, save to file :\nall_tones.txt(in '+os.getcwd()+'\\result\\'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result\\'+dir_name+'\\all_tones.txt', 'w')
      elif os.name == 'posix':
        print 'too many to show, save to file :\nall_tones.txt(in '+os.getcwd()+'/result/'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result//'+dir_name+'//all_tones.txt', 'w')
      for t in text:
        if isinstance(self.char2stroke(t), int): result.write(self.tones(t)+'\n')
      result.close()

  def showalltone2(self, text, dir_name , num=40):
    num = min(len(text),num)
    if num == len(text):
      for t in text:
      	for w in t:
          if isinstance(self.char2stroke(w), int): print self.tones(w)
    else:
      if os.name == 'nt':
        print 'too many to show, save to file :\nall_tones.txt(in '+os.getcwd()+'\\result\\'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result\\'+dir_name+'\\all_tones.txt', 'w')
      elif os.name == 'posix':
        print 'too many to show, save to file :\nall_tones.txt(in '+os.getcwd()+'/result/'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result//'+dir_name+'//all_tones.txt', 'w')
      for t in text:
        for w in t:
          if isinstance(self.char2stroke(w), int): result.write(self.tones(w)+'\n')
      result.close()

  def show_repeat_finals1(self, text, dir_name , num=40):
    num = min(len(text),num)
    if num == len(text):
      for i in range(len(text)-1):
        tt = ''; tt = text[i]+text[i+1]
        if c2a.char2vowel[tt[0]] == c2a.char2vowel[tt[1]] and c2a.char2tone[tt[0]] == c2a.char2tone[tt[1]]:
          if len(c2a.char2vowel[tt[0]]) > 0: print tt,
    else:
      if os.name == 'nt':
        print 'too many to show, save to file :\nall_repeat_finals.txt(in '+os.getcwd()+'\\result\\'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result\\'+dir_name+'\\all_repeat_finals.txt', 'w')
      elif os.name == 'posix':
        print 'too many to show, save to file :\nall_repeat_finals.txt(in '+os.getcwd()+'/result/'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result//'+dir_name+'//all_repeat_finals.txt', 'w')
      for i in range(len(text)-1):
        tt = ''; tt = text[i]+text[i+1]
        if c2a.char2vowel[tt[0]] == c2a.char2vowel[tt[1]] and c2a.char2tone[tt[0]] == c2a.char2tone[tt[1]]:
          if len(c2a.char2vowel[tt[0]]) > 0: result.write(tt+'\n') 
      result.close()     

  def show_repeat_finals2(self, text, dir_name , num=20):
    i = 0
    for t in text:
      if len(t) == 2:
        i += 1
        if c2a.char2vowel[t[0]] == c2a.char2vowel[t[1]] and c2a.char2tone[t[0]] == c2a.char2tone[t[1]]:
          if len(c2a.char2vowel[t[0]]) > 0: print t,
#        if i > num: 
#          break
    if os.name == 'nt':
      print 'too many to show, save to file :\nall_repeat_finals.txt(in '+os.getcwd()+'\\result\\'+dir_name+')'
      print 'file in progress...'
      if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
      result = codecs.open('result\\'+dir_name+'\\all_repeat_finals.txt', 'w')
    elif os.name == 'posix':
      print 'too many to show, save to file :\nall_repeat_finals.txt(in '+os.getcwd()+'/result/'+dir_name+')'
      print 'file in progress...'
      if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
      result = codecs.open('result//'+dir_name+'//all_repeat_finals.txt', 'w')
    for t in text:
      if len(t) == 2:
        if c2a.char2vowel[t[0]] == c2a.char2vowel[t[1]] and c2a.char2tone[t[0]] == c2a.char2tone[t[1]]:
          if len(c2a.char2vowel[t[0]]) > 0: result.write(t+'\n')
    result.close()
          	
  def show_repeatwords1(self, text, dir_name , num=40):
    num = min(len(text),num)
    if num == len(text):
      for i in range(len(text)-1):
        tt = ''; tt = text[i]+text[i+1]
        if text[i] == text[i+1]: print tt,
    else:
      if os.name == 'nt':
        print 'too many to show, save to file :\nall_repeat_words.txt(in '+os.getcwd()+'\\result\\'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result\\'+dir_name+'\\all_repeat_words.txt', 'w')
      elif os.name == 'posix':
        print 'too many to show, save to file :\nall_repeat_words.txt(in '+os.getcwd()+'/result/'+dir_name+')'
        print 'file in progress...'
        if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
        result = codecs.open('result//'+dir_name+'//all_repeat_words.txt', 'w')
      for i in range(len(text)-1):
        tt = ''; tt = text[i]+text[i+1]
        if text[i] == text[i+1]: result.write(tt+'\n')
      result.close()  
      
  def show_repeatwords2(self, text, dir_name , num=20):
    i = 0
    for t in text:
      if len(t) == 2:
        i += 1
        if t[0] == t[1]: print t,
        if i > num: 
          break
    if os.name == 'nt':
      print 'too many to show, save to file :\nall_repeat_words.txt(in '+os.getcwd()+'\\result\\'+dir_name+')'
      print 'file in progress...'
      if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
      result = codecs.open('result\\'+dir_name+'\\all_repeat_words.txt', 'w')
    elif os.name == 'posix':
      print 'too many to show, save to file :\nall_repeat_words.txt(in '+os.getcwd()+'/result/'+dir_name+')'
      print 'file in progress...'
      if not os.path.exists('result/'+dir_name): os.makedirs('result/'+dir_name)
      result = codecs.open('result//'+dir_name+'//all_repeat_words.txt', 'w')
    for t in text:
      if len(t) == 2:
        if t[0] == t[1]: result.write(t+'\n')    
    result.close()   


## ����G�O�_�ŦX�������y��
#�������y������֪��@��,����Y��,�C���|�y,�C�y���r,�@�G�Q�r.
#�����W,�ĤG�B�|�y�@�w�n����,�ĤT�y�@�w���i����,�Ĥ@�y�h�i��i����.
#�Ҧ�����ֳ����D����,�������y��,
#�C�y��2,4�Ӧr�@�G�y �T�|�y�����������ۤ�,�G�T�y�����ۦP,��������,�������i�q��. �H�ϥH�W��ߺ٬��ǫ�
  def IsPoem(self):
    for f in os.listdir(os.getcwd()+'/MyCorpus'):
      text = codecs.open(os.getcwd()+'/MyCorpus/'+f, 'rb', 'big5', 'ignore').read()
      cleantext = []; samevowel = 0; diffvowel = 0; sametone = 0; difftone = 0
      for w in unicode(text):
        if w not in u"\s\n\r�C�A�B�H�I �@":
          cleantext.append(w)
      if len(cleantext) == 20:
        # �P�_�ĤG�B�|�y�O�_�ҦP��
        for v in self.char2vowel[cleantext[19]]:
          if v in self.char2vowel[cleantext[9]]:
            samevowel = 1
        for v in self.char2vowel[cleantext[9]]:
          if v in self.char2vowel[cleantext[19]] and samevowel == 1:
            samevowel = 1
        # �P�_�ĤT�y�O�_���P��
        for v in self.char2vowel[cleantext[14]]:
          if v not in self.char2vowel[cleantext[19]] and v not in self.char2vowel[cleantext[9]]:
            diffvowel = 1
        # �P�_�@�G�y�ΤT�|�y���C�y��2,4�Ӧr���������O�_�ۤ�
        if len(self.char2down_tone[cleantext[1]]) != len(self.char2down_tone[cleantext[6]]):
          difftone = 1 # �Ĥ@�y��ĤG�y����2�Ӧr�������O�_�ۤ�
        else: sametone = 2
        if len(self.char2down_tone[cleantext[3]]) != len(self.char2down_tone[cleantext[8]]) and difftone == 1:
          difftone = 1 # �Ĥ@�y��ĤG�y����4�Ӧr�������O�_�ۤ�
        else: sametone = 3
        if len(self.char2down_tone[cleantext[11]]) != len(self.char2down_tone[cleantext[16]]) and difftone == 1:
          difftone = 1 # �ĤT�y��ĥ|�y����2�Ӧr�������O�_�ۤ�
        else: sametone = 4
        if len(self.char2down_tone[cleantext[13]]) != len(self.char2down_tone[cleantext[18]]) and difftone == 1:
          difftone = 1 # �ĤT�y��ĥ|�y����4�Ӧr�������O�_�ۤ�
        else: sametone = 5
        # �P�_�G�T�y���C�y��2,4�Ӧr���������O�_�ۦP
        if len(self.char2down_tone[cleantext[6]]) > 0 and len(self.char2down_tone[cleantext[11]]) > 0:
          sametone = 1 # �ĤG�y��ĤT�y����2�Ӧr�O�_���O���n
        elif len(self.char2down_tone[cleantext[6]]) == 0 and len(self.char2down_tone[cleantext[11]]) == 0:
          sametone = 1 # �ĤG�y��ĤT�y����2�Ӧr�O�_���O���n
        else: difftone = 2
        if len(self.char2down_tone[cleantext[8]]) > 0 and len(self.char2down_tone[cleantext[13]]) > 0 and sametone == 1:
          sametone = 1 # �ĤG�y��ĤT�y����4�Ӧr�O�_���O���n
        elif len(self.char2down_tone[cleantext[8]]) == 0 and len(self.char2down_tone[cleantext[13]]) == 0 and sametone == 1:
          sametone = 1 # �ĤG�y��ĤT�y����4�Ӧr�O�_���O���n
        else: difftone = 3
        # �H�U�ھګe���P�_���G�@��X
        if samevowel == 1 and diffvowel == 1 and sametone == 1 and difftone == 1: 
          print "�ɮ�:",f,"�A���p�U:\n",text,"\n�o�O�������y\n"
        else: 
          print "�ɮ�:",f,"�A���p�U:\n",text,"\n�o���O�������y�A�]��:"
        if samevowel == 0:
          print cleantext[9],'�M',cleantext[19],'���������P'
        if diffvowel == 0:
          print cleantext[14],'�M',cleantext[19],'��',cleantext[9],'�������ۦP\n'
        if sametone == 2:
          print cleantext[1],'�M',cleantext[6],'�������ۦP\n'
        if sametone == 3:
          print cleantext[3],'�M',cleantext[8],'�������ۦP\n'
        if sametone == 4:
          print cleantext[11],'�M',cleantext[16],'�������ۦP\n'
        if sametone == 5:
          print cleantext[13],'�M',cleantext[18],'�������ۦP\n'
        if difftone == 2:
          print cleantext[6],'�M',cleantext[11],'�������ۤ�\n'
        if difftone == 3:
          print cleantext[8],'�M',cleantext[13],'�������ۤ�\n'
      elif len(cleantext) < 20:
        print "�ɮ�:",f,"�A���p�U:\n",text,'��r�榡���@�ˡA�������y�C�y���r�A�|�y�@20�Ӧr\n'
      else:
        print "�ɮ�:",f,'�A��r�L�����C�X���:\n��r�榡���@�ˡA�������y�C�y���r�A�|�y�@20�Ӧr\n'
  #    print cleantext[13], len(c2a.char2down_tone[cleantext[13]])


if __name__ == '__main__':
  c2a = Char2Any()
  words = []; words_tagged = []; MoreMenu = ''; corpus = ''
  print '? :',c2a.char2stroke('?')
  print u'�� :',c2a.char2stroke(u'��')
  print u'�@ :',c2a.char2stroke(u'�@')
  print c2a.phonetic_symbols(u'��')
  print c2a.phonetic_symbols(u'�@')
  print c2a.phonetic_symbols(u'�F')
  print c2a.phones(u'�F')
  print c2a.phones(u'�M')
  print c2a.phones(u'�G')
  print c2a.phones(u'�Q')
  print c2a.tones(u'�F')
  print c2a.tones(u'�M')
  while 1:
    print '''
    ==============================================
    LACC toolkit(Load and Analysis Chinese Corpus)
    ==============================================
      
    Corpora for linguistic analysis:
      1. Standard Segmented Corpus from Academia Sinica 
      2. Academia Sinica Balanced Corpus with tagged texts
      3. Your own corpus (raw data)
    '''
    inp = raw_input("Select a corpus for transfer (enter one of the above number and 0 for exit):")
    if inp == '1':
      # only accept 2 or 3 characters of extension name. 
      stbp = NLTK_tools.SyntaxCorpusReader_LACC(os.getcwd()+'/SSC', '.*\..{2,3}', encoding='utf8')
      words = stbp.words()
      print 'loading corpus: SSC'; corpus = 'SSC'; break
    elif inp == '2': 
    	# only accept ascii characters of file name. 
      stbp = NLTK_tools.SyntaxCorpusReader_LACC(os.getcwd()+'/ASBC', '[\w*\d*].*', encoding='utf8')
      words_tagged = stbp.tagged_words()
      words = [w for (w, t) in words_tagged]
      print 'loading corpus: ASBC'; corpus = 'ASBC'; break
    elif inp == '3':
      words = ''
      for f in os.listdir(os.getcwd()+'/MyCorpus'):
        words += codecs.open(os.getcwd()+'/MyCorpus/'+f, 'rb', 'big5', 'ignore').read()
      print 'loading corpus: MyCorpus'; corpus = 'MyCorpus'; MoreMenu = '8. poem validation'; break  
    elif inp == '0': exit(0)
    else: print 'please select a corpus...'; continue

  if corpus == 'MyCorpus':
    print '''
    linguistic component decomposition:
      strokes:
        1. sum of all word's stroke
        2. show all word's stroke
      phones:
        3. show all word's phone
        4. show all word's consonat or vowel
      tones:
        5. show all word's tone
      applications:
        6. show all repeat-final in bi-words
        7. show all repeated bi-words
        {0}
    '''.format(MoreMenu)
    inp = raw_input('Select a number from the above for decomposition (0 to exit):')
    if inp == '0': exit(0)
#    if inp in '1234567' and cp == 0: print 'no corpus loaded'; break
    if inp == '1': c2a.sumofstroke1(words)
    if inp == '2': c2a.showallstroke1(words, corpus)
    if inp == '3': c2a.showallphonesymbol1(words, corpus)
    if inp == '4': c2a.showallphone1(words, corpus)
    if inp == '5': c2a.showalltone1(words, corpus)
    if inp == '6': c2a.show_repeat_finals1(words, corpus)
    if inp == '7': c2a.show_repeatwords1(words, corpus) 
    if inp == '8': c2a.IsPoem() 	
  else:
    print "type(words)=", type(words), "\ntype(words_tagged)=", type(words_tagged)
    text = NLTK_tools.MyText(words)
    print "The first 20 words of words:", ','.join(w for w in words[:20])
    print "The first 20 words of text:", ','.join(w for w in text[:20])
    print "The first 20 tuples of words_tagged:", ','.join('/'.join([w,t]) for (w,t) in words_tagged[:20])
    if corpus == 'ASBC': MoreMenu = '8. Find text patterns with POS tags'
    while 1:
      print '''
      Text Analysis:
        1. Concordance
        2. Collocations
        3. Similar words
        4. Common contexts
        5. Find text patterns
        6. Right and left terms of a Chinese character
        7. Generate a random text
        {0} 
      '''.format(MoreMenu)
      print '''
      linguistic component decomposition:
        strokes:
          a. sum of all word's stroke
          b. show all word's stroke
        phones:
          c. show all word's phone
          d. show all word's consonat or vowel
        tones:
          e. show all word's tone
        applications:
          f. show all repeat-final in bi-words
          g. show all repeated bi-words
      '''
      print "Number of words:", len(words), ", len(text)=", len(text)
      print "Number of tagged words:", len(words_tagged)
      inp = raw_input('Select a number or alphabet from the above for analysis (0 to exit):'); 
      print "inp='" + inp + "'"
      if inp == '0': exit(0)
      if inp == '1': NLTK_tools.demo_concordance(text, "")
      if inp == '2': NLTK_tools.demo_collocations(text)
      if inp == '3': NLTK_tools.demo_similar(text, "")
      if inp == '4': NLTK_tools.demo_common_context(text)
      if inp == '5': NLTK_tools.demo_findall(text)
      if inp == '6': 
        print '''
        1. show all RLgrams depends on user's input (display on screen or save to text file)
        2. show all RLgrams for all bi-words in a corpus (save to text file)
              '''
        mode = raw_input('Select a mode for RLgrams:'); 
        print "mode='" + mode + "'"
        if mode == '1': NLTK_tools.demo_RLgrams(words, corpus)
        if mode == '2':
          print 'file in progress...'
          if os.name == 'nt':
            if not os.path.exists('result/'+corpus): os.makedirs('result/'+corpus)
            result = codecs.open('result\\'+corpus+'\\all_RLgrams.txt', 'w')
          elif os.name == 'posix':
            if not os.path.exists('result/'+corpus): os.makedirs('result/'+corpus)
            result = codecs.open('result//'+corpus+'//all_RLgrams.txt', 'w')
          for w in words:
            if len(w) == 2: NLTK_tools.RLgramsALL(words, result, w)
          result.close()
      if inp == '7': NLTK_tools.demo_generate(text)
      if inp == '8' and MoreMenu: NLTK_tools.demo_findPOSpattern(words_tagged)
      if inp == 'a': c2a.sumofstroke2(words)
      if inp == 'b': c2a.showallstroke2(words, corpus)
      if inp == 'c': c2a.showallphonesymbol2(words, corpus)
      if inp == 'd': c2a.showallphone2(words, corpus)
      if inp == 'e': c2a.showalltone2(words, corpus)
      if inp == 'f': c2a.show_repeat_finals2(words, corpus)
      if inp == 'g': c2a.show_repeatwords2(words, corpus)		
      if inp == 'h': c2a.IsPoem()

#  end of interactive ui
    	
## �]�\ cs �~�O���T������r
## �D�G�Q���Q���B�@�r�@�y�B�T�ߤG�N�B�A�T�˥|�B���T���|�����X��
#idiom = [(c1, c2, c3, c4) for (c1, c2, c3, c4) in chars \
#if (re.match(u'�@-�Q', c1) and re.match(u'�@-�Q', c3)) or \
#(re.match(u'�@-�Q', c2) and re.match(u'�@-�Q', c4))]
#  idioms = []; SingleWords = []; t4 = ''
#  for c in words:
#    for t in c:
#      SingleWords.append(t)
#  for i in range(len(SingleWords)-3):
#    t4 = SingleWords[i]+SingleWords[i+1]+SingleWords[i+2]+SingleWords[i+3]
#    if t4[0] in c2a.char2number and t4[2] in c2a.char2number or t4[1] in c2a.char2number and t4[3] in c2a.char2number:
#      idioms.append(t4)
#    t4 = ''
#  for t in idioms: print t

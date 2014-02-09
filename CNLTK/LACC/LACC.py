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
    self.consonant.update(# 聲母字典
      {u'ㄅ':1,u'ㄆ':1,u'ㄇ':1,u'ㄈ':1,u'ㄉ':1,u'ㄊ':1,u'ㄋ':1,u'ㄌ':1,
       u'ㄍ':1,u'ㄎ':1,u'ㄏ':1,u'ㄐ':1,u'ㄑ':1,u'ㄒ':1,u'ㄓ':1,u'ㄔ':1,
       u'ㄕ':1,u'ㄖ':1,u'ㄗ':1,u'ㄘ':1,u'ㄙ':1}
    )
    self.vowel.update(# 韻母字典
      {u'ㄧ':1,u'ㄨ':1,u'ㄩ':1,u'ㄚ':1,u'ㄛ':1,u'ㄜ':1,u'ㄝ':1,u'ㄞ':1,
       u'ㄟ':1,u'ㄠ':1,u'ㄡ':1,u'ㄢ':1,u'ㄣ':1,u'ㄤ':1,u'ㄥ':1,u'ㄦ':1}
    )
    self.char2number.update(
      {u'一':1,u'二':2,u'三':3,u'四':4,u'五':5,u'六':6,u'七':7,u'八':8,
       u'九':9,u'十':10,u'百':12,u'千':13,u'萬':14}
    )
    f1 = codecs.open('char2stroke.txt', 'rb', 'big5', 'ignore')
    for line in f1:
      if line[0] != '?': # for now only handle chinese traditional characters
        #print line[0]
        #print line[line.find("\t", 0)+1:line.find("\t", line.find("\t", 0)+1)]
        self.char2strokes[line[0]] = int(line[line.find("\t", 0)+1:line.find("\t", line.find("\t", 0)+1)])
    self.char2strokes.update(# punctuations
      {u'。':u'。', u'？':u'？', u'！':u'！', u'，':u'，', u'、':u'、',
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
          self.char2consonant[line[0]].append(phone[i]) # 字詞轉聲母字典
        elif self.vowel.has_key(phone[i]):
          self.char2vowel[line[0]].append(phone[i]) # 字詞轉韻母字典
        # 字詞轉聲調字典
        elif phone[i] in u'ˊ':
          self.char2tone[line[0]].append('2') # 是否為二聲
          self.char2up_tone[line[0]].append('2')
        elif phone[i] in u'ˇ':
          self.char2tone[line[0]].append('3') # 是否為三聲
          self.char2down_tone[line[0]].append('3')
        elif phone[i] in u'ˋ':
          self.char2tone[line[0]].append('4') # 是否為四聲
          self.char2down_tone[line[0]].append('4')
        elif phone[i] in u'˙':
          self.char2tone[line[0]].append('5') # 是否為輕聲
        elif phone[i] not in "\n\r":
          self.char2vowel[line[0]].append(phone[i])# 區別複韻母間的空白
        elif phone[i] in " \r" and phone[i-1] not in u'ˊˇˋ˙':
          self.char2tone[line[0]].append('1') # 是否為一聲
          self.char2up_tone[line[0]].append('1')

      if len(line[4:line.find("\s", 4)]) > 4: 
        self.char2phone[line[0]] = line[4:line.find("\s", 4)].split() # 有破音字
      else:
        self.char2phone[line[0]] = line[4:line.find(' ', 4)] # 沒有破音字 

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


## 檢驗：是否符合五言絕句詩
#五言絕句為近體詩的一種,格律嚴格,每首四句,每句五字,共二十字.
#押韻上,第二、四句一定要押韻,第三句一定不可押韻,第一句則可押可不押.
#所有近體詩都講求平仄,五言絕句中,
#每句第2,4個字一二句 三四句的平仄必須相反,二三句必須相同,押韻部分,平仄不可通押. 違反以上格律稱為犯律
  def IsPoem(self):
    for f in os.listdir(os.getcwd()+'/MyCorpus'):
      text = codecs.open(os.getcwd()+'/MyCorpus/'+f, 'rb', 'big5', 'ignore').read()
      cleantext = []; samevowel = 0; diffvowel = 0; sametone = 0; difftone = 0
      for w in unicode(text):
        if w not in u"\s\n\r。，、？！ 　":
          cleantext.append(w)
      if len(cleantext) == 20:
        # 判斷第二、四句是否皆同韻
        for v in self.char2vowel[cleantext[19]]:
          if v in self.char2vowel[cleantext[9]]:
            samevowel = 1
        for v in self.char2vowel[cleantext[9]]:
          if v in self.char2vowel[cleantext[19]] and samevowel == 1:
            samevowel = 1
        # 判斷第三句是否不同韻
        for v in self.char2vowel[cleantext[14]]:
          if v not in self.char2vowel[cleantext[19]] and v not in self.char2vowel[cleantext[9]]:
            diffvowel = 1
        # 判斷一二句及三四句中每句第2,4個字中的平仄是否相反
        if len(self.char2down_tone[cleantext[1]]) != len(self.char2down_tone[cleantext[6]]):
          difftone = 1 # 第一句跟第二句的第2個字的平仄是否相反
        else: sametone = 2
        if len(self.char2down_tone[cleantext[3]]) != len(self.char2down_tone[cleantext[8]]) and difftone == 1:
          difftone = 1 # 第一句跟第二句的第4個字的平仄是否相反
        else: sametone = 3
        if len(self.char2down_tone[cleantext[11]]) != len(self.char2down_tone[cleantext[16]]) and difftone == 1:
          difftone = 1 # 第三句跟第四句的第2個字的平仄是否相反
        else: sametone = 4
        if len(self.char2down_tone[cleantext[13]]) != len(self.char2down_tone[cleantext[18]]) and difftone == 1:
          difftone = 1 # 第三句跟第四句的第4個字的平仄是否相反
        else: sametone = 5
        # 判斷二三句中每句第2,4個字中的平仄是否相同
        if len(self.char2down_tone[cleantext[6]]) > 0 and len(self.char2down_tone[cleantext[11]]) > 0:
          sametone = 1 # 第二句跟第三句的第2個字是否都是仄聲
        elif len(self.char2down_tone[cleantext[6]]) == 0 and len(self.char2down_tone[cleantext[11]]) == 0:
          sametone = 1 # 第二句跟第三句的第2個字是否都是平聲
        else: difftone = 2
        if len(self.char2down_tone[cleantext[8]]) > 0 and len(self.char2down_tone[cleantext[13]]) > 0 and sametone == 1:
          sametone = 1 # 第二句跟第三句的第4個字是否都是仄聲
        elif len(self.char2down_tone[cleantext[8]]) == 0 and len(self.char2down_tone[cleantext[13]]) == 0 and sametone == 1:
          sametone = 1 # 第二句跟第三句的第4個字是否都是平聲
        else: difftone = 3
        # 以下根據前面判斷結果作輸出
        if samevowel == 1 and diffvowel == 1 and sametone == 1 and difftone == 1: 
          print "檔案:",f,"，原文如下:\n",text,"\n這是五言絕句\n"
        else: 
          print "檔案:",f,"，原文如下:\n",text,"\n這不是五言絕句，因為:"
        if samevowel == 0:
          print cleantext[9],'和',cleantext[19],'的押韻不同'
        if diffvowel == 0:
          print cleantext[14],'和',cleantext[19],'或',cleantext[9],'的押韻相同\n'
        if sametone == 2:
          print cleantext[1],'和',cleantext[6],'的平仄相同\n'
        if sametone == 3:
          print cleantext[3],'和',cleantext[8],'的平仄相同\n'
        if sametone == 4:
          print cleantext[11],'和',cleantext[16],'的平仄相同\n'
        if sametone == 5:
          print cleantext[13],'和',cleantext[18],'的平仄相同\n'
        if difftone == 2:
          print cleantext[6],'和',cleantext[11],'的平仄相反\n'
        if difftone == 3:
          print cleantext[8],'和',cleantext[13],'的平仄相反\n'
      elif len(cleantext) < 20:
        print "檔案:",f,"，原文如下:\n",text,'文字格式不一樣，五言絕句每句五字，四句共20個字\n'
      else:
        print "檔案:",f,'，文字過長不列出原文:\n文字格式不一樣，五言絕句每句五字，四句共20個字\n'
  #    print cleantext[13], len(c2a.char2down_tone[cleantext[13]])


if __name__ == '__main__':
  c2a = Char2Any()
  words = []; words_tagged = []; MoreMenu = ''; corpus = ''
  print '? :',c2a.char2stroke('?')
  print u'我 :',c2a.char2stroke(u'我')
  print u'一 :',c2a.char2stroke(u'一')
  print c2a.phonetic_symbols(u'我')
  print c2a.phonetic_symbols(u'一')
  print c2a.phonetic_symbols(u'了')
  print c2a.phones(u'了')
  print c2a.phones(u'刀')
  print c2a.phones(u'二')
  print c2a.phones(u'十')
  print c2a.tones(u'了')
  print c2a.tones(u'刀')
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
    	
## 也許 cs 才是正確的詞轉字
## 求：十全十美、一字一句、三心二意、顛三倒四、不三不四等詞出來
#idiom = [(c1, c2, c3, c4) for (c1, c2, c3, c4) in chars \
#if (re.match(u'一-十', c1) and re.match(u'一-十', c3)) or \
#(re.match(u'一-十', c2) and re.match(u'一-十', c4))]
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

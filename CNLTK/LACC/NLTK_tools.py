# -*- coding: big5 -*-
# LACC version 0.1: Load and Analyze Chinese Corpus (LACC)
# This program allowS all text analyses provided NLTK
# Writen by samtseng@ntnu.edu.tw on 2011/11/07
# To execute under DOS command, run: python LACC_win.py
#
import re, codecs, sys, os
if sys.getdefaultencoding() != 'utf-8':
  reload(sys)
  sys.setdefaultencoding('utf-8') 
#IDENTIFIER = re.compile(u'^\d+\.\s+[。：，？！]\s+')
IDENTIFIER = re.compile(u'^\d+\.[　\s]+[。．：；，？﹖！](\([A-Z]+\))?')
#IDENTIFIER = re.compile(u'^\d+\.[　\s]+[。．：；，？﹖！](\([A-Z]+\))?|[－「」【】、。．：；，？﹖！\s]')
DummyLine = re.compile('^[\*%]+|^\s*$')
TAGWORD = re.compile(u'([^()　\s]+)\(([A-Za-z_\d]+)\)')
MyWORD = re.compile(r'(\S+)')
#MyWORD = re.compile(r'(\W|\d|\w)')

import nltk
from nltk.corpus.reader import *

class SyntaxCorpusReader_LACC(SyntaxCorpusReader):
    """
    Reader inherited from SyntaxCorpusReader.
    """
    def _read_block(self, stream):
      sent = '';
      for line in stream:
        if DummyLine.match(line): continue
        line = IDENTIFIER.sub('', line)
        sent += line
        if re.search(u'[。？！]', line) : break
      return [sent]

    def _word(self, sent):
      return MyWORD.findall(sent) # to know the changes, see the examples below
#        LoT = MyWORD.findall(sent) # LoT : ListOfTuple
#        return [x+y for x,y in LoT] # convert LoT into a List
# python -c "import re; WORD = re.compile(r'(?:(?::[^:()|]+:([^:()|]+))|(?:#(.+)\([A-Z]+CATEGORY\)))'); print WORD.findall('NP(Head:DM:有一天)#，(COMMACATEGORY)')"
#[('\xe6\x9c\x89\xe4\xb8\x80\xe5\xa4\xa9', ''), ('', '\xef\xbc\x8c')]
# python -c "import re; WORD = re.compile(r'(?:(?::[^:()|]+:([^:()|]+))|(?:#(.+)\([A-Z]+CATEGORY\)))'); lot= WORD.findall('NP(Head:DM:有一天)#，(COMMACATEGORY)'); print [ x+y for x,y in lot]"
#['\xe6\x9c\x89\xe4\xb8\x80\xe5\xa4\xa9', '\xef\xbc\x8c']

    def _parse(self, sent):
        return nltk.tree.sinica_parse(sent)

    def _tag(self, sent, simplify_tags=None):
        tagged_sent = [(w,t) for (w,t) in TAGWORD.findall(sent)]
        if simplify_tags:
            tagged_sent = [(w, self._tag_mapping_function(t))
                           for (w,t) in tagged_sent]
        return tagged_sent


class MyText(object):
    """
    >>> moby = Text(nltk.corpus.gutenberg.words('melville-moby_dick.txt'))
    """
    # This defeats lazy loading, but makes things faster.  This
    # *shouldnt* be necessary because the corpus view *should* be
    # doing intelligent caching, but without this it's running slow.
    # Look into whether the caching is working correctly.
    _COPY_TOKENS = True
    
    def __init__(self, tokens, name=None):
        """
        Create a Text object.
        
        @param tokens: The source text.
        @type tokens: C{sequence} of C{str}
        """
        if self._COPY_TOKENS:
            tokens = list(tokens)
        self.tokens = tokens
    #////////////////////////////////////////////////////////////
    # Support item & slice access
    #////////////////////////////////////////////////////////////
    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.tokens[i.start:i.stop]
        else:
            return self.tokens[i]

    def __len__(self):
        return len(self.tokens)


def demo_concordance(self, word, width=50, lines=25):
        """
        Print a concordance for C{word} with the specified context window.
        Word matching is not case-sensitive.
        @seealso: L{ConcordanceIndex}
        """
        if '_concordance_index' not in self.__dict__:
            print "Building index..."
            self._concordance_index = nltk.text.ConcordanceIndex(self.tokens,
                                                       key=lambda s:s.lower())
        while 1:
          word = raw_input('Enter a Chinese word such as "開心"(type 0 to exit):'); 
          print "word='"+ word + "'"
          if word == '0': break
          word = word.decode('utf-8')
          self._concordance_index.print_concordance(word, width, lines)

from nltk.util import tokenwrap, LazyConcatenation
from nltk.probability import FreqDist, LidstoneProbDist

def demo_collocations(self, num=40, window_size=2):
        """
        Print collocations derived from the text, ignoring stopwords.

        @seealso: L{find_collocations}
        @param num: The maximum number of collocations to print.
        @type num: C{int}
        @param window_size: The number of tokens spanned by a collocation (default=2)
        @type window_size: C{int}
        """
        if not ('_collocations' in self.__dict__ and self._num == num and self._window_size == window_size):
            self._num = num
            self._window_size = window_size
            print "Building collocations list"
            from nltk.corpus import stopwords
            ignored_words = stopwords.words('english')
            from nltk.collocations import BigramCollocationFinder
            finder = BigramCollocationFinder.from_words(self.tokens, window_size) 
            finder.apply_freq_filter(2)
            finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)
            from nltk.metrics import f_measure, BigramAssocMeasures
            bigram_measures = BigramAssocMeasures()
            self._collocations = finder.nbest(bigram_measures.likelihood_ratio, num)
        colloc_strings = [w1+u' '+w2 for w1, w2 in self._collocations]
        print "List {0} collocations".format(num)
        print tokenwrap(colloc_strings, separator=u'; ')



def generate_model(cfdist, word, num=20): 
    for i in range(num):
      print word,
      word = cfdist[word].max()

def demo_generate(text):
  print "len of tokens=", len(text)
  while True:
    N = raw_input("Select a number N for the N-gram model (2, 3, or 4 only):")
    N = int(N)
    if N in [2, 3, 4]: break
  if N == 2:
    bi = nltk.bigrams(text)
    cfd = nltk.ConditionalFreqDist(bi)
  else:
    from nltk.model import NgramModel
    from nltk.probability import LidstoneProbDist, WittenBellProbDist
    estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
    lm = NgramModel(N, text, estimator)
#    for w in lm.generate(20, context=('I')): print w,
  while 1:
    inp = raw_input('Enter a Chinese word such as "目前"(type 0 to exit):'); 
    print "inp='"+ inp + "'"
    if inp == '0': break
    inp = inp.decode('big5')
    if N == 2:
      generate_model(cfd, inp)
    else:
      for w in lm.generate(20, context=(inp)): print w,
      print "\n"
      for w in lm.generate(20, context=(inp)): print w,
    print "\n"



def demo_similar(self, word, num=20):
        """
        Distributional similarity: find other words which appear in the
        same contexts as the specified word; list most similar words first.
        
        @param word: The word used to seed the similarity search
        @type word: C{str} 
        @param num: The number of words to generate (default=20)
        @type num: C{int}
        @seealso: L{ContextIndex.similar_words()}
        """
        if '_word_context_index' not in self.__dict__:
            print 'Building word-context index...'
            self._word_context_index = nltk.text.ContextIndex(self.tokens,
                                                    filter=lambda x:x.isalpha(),
                                                    key=lambda s:s.lower())

#        words = self._word_context_index.similar_words(word, num)

        while 1:
          word = raw_input('Enter a Chinese word such as "開心"(type 0 to exit):'); 
          print "word='"+ word + "'"
          if word == '0': break
          word = word.decode('utf-8')
          wci = self._word_context_index._word_to_contexts
          if word in wci.conditions():
            contexts = set(wci[word])
            fd = FreqDist(w for w in wci.conditions() for c in wci[w]
                          if c in contexts and not w == word)
            words = fd.keys()[:num]
            print tokenwrap(words)
          else:
            print "No matches"

def demo_common_context(self, num=20):
        """
        Find contexts where the specified words appear; list
        most frequent common contexts first.
        @seealso: L{ContextIndex.common_contexts()}
        """
        if '_word_context_index' not in self.__dict__:
            print 'Building word-context index...'
            self._word_context_index = nltk.text.ContextIndex(self.tokens,
                                                    key=lambda s:s.lower())
        while 1:
          inp = raw_input('Enter two Chinese words such as "我 你"(type 0 to exit):'); 
          print "inp='"+ inp+"'"
          if inp == '0': break
          inp = inp.decode('utf-8')
          words = inp.split(u' ')
          try:
            fd = self._word_context_index.common_contexts(words, True)
            if not fd:
                print "No common contexts were found"
            else:
                ranked_contexts = fd.keys()[:num]
                print tokenwrap(w1+"_"+w2 for w1,w2 in ranked_contexts)
          except ValueError, e:
            print e

def demo_findall(text):
  while 1:
    inp = raw_input('Enter two Chinese words such as "我:2 手:4"(type 0 to exit):'); 
    print "inp='"+ inp+"'"
    if inp == '0': break
    inp = inp.decode('big5')
    reg = "<1> <2> <3> <4> <5>"
    if len(inp) == 0:
      print 'no input words'
    else:
      for wp in inp.split(' '):	
        (w, p) = wp.split(':')
  #        reg = re.sub(p, w, reg)
        reg = re.sub(p, ''.join(['.*', w, '.*']), reg)
    reg = re.sub('\d', '.*', reg)
    print "reg=", reg
#    text.findall(reg)
    if "_token_searcher" not in text.__dict__:
      text._token_searcher = nltk.text.TokenSearcher(text)
    hits = text._token_searcher.findall(reg)
    hits = [' '.join(h) for h in hits]
    print tokenwrap(hits, u"; ") 

def demo_vocab(text):
  text.vocab()

from collections import defaultdict
from operator import itemgetter

def my_itemgetter(*items): # revised from http://docs.python.org/library/operator.html
    if len(items) == 1:
        item = items[0]
        def g(obj):
            return len(obj[item])
    else:
        def g(obj):
            return tuple(len(obj[item]) for item in items)
    return g

def myi():
  def g(obj): return len(obj[1])
  return g

def myig(): return lambda(obj): obj[1]

def demo_RLgrams(word, corpus, num=20):
  uL = defaultdict(list)
  uR = defaultdict(list)
  uniL = defaultdict(list)
  uniR = defaultdict(list)
  for w in word:
    if len(w) < 2: continue
    uL[w[0]].append(w[1:])
    uR[w[-1]].append(w[:-1])

  print "Reduce Unigram uL (List of list) into uniL (List of tuples) ..."; 
  for k,lst in uL.iteritems():
    dic = defaultdict(int)
    for u in lst: dic[u] += 1
    for kd, vd in sorted(dic.items(), key=myig(), reverse=True):
      uniL[k].append((kd, vd))
    
  print "Reduce Unigram uR (List of list) into uniR (List of tuples) ..."; 
  for k,lst in uR.iteritems():
    dic = defaultdict(int)
    for u in lst: dic[u] += 1
    for kd, vd in sorted(dic.items(), key=myig(), reverse=True):
      uniR[k].append((kd, vd))

  while 1:
    inp = raw_input('Enter a Chinese character such as "花" or "花園" (type 0 to exit):'); 
    print "inp='"+ inp+"'"
    if inp == '0': break
    if len(inp) == 1:
      inp = inp.decode('big5')
      print "The right sub-terms have ", len(uniL[inp]), " items. List {0} of them:".format(min( num, len(uniL[inp])) )
      for (t, df) in uniL[inp][:num]:
        print t, df
      print "The left sub-terms have ", len(uniR[inp]),  " items. List {0} of them:".format(min( num, len(uniR[inp])) )
      for (t, df) in uniR[inp][:num]:
        print t, df
    else:
      RWcount = 0; LWcount = 0; RDcount = 0; LDcount = 0
      inp = inp.decode('utf-8')
      if min( num, len(uniL[inp[0]]), len(uniR[inp[0]])) == num:
        print "The right sub-terms of ", inp[0], " have ", len(uniL[inp[0]]), " items. List {0} of them:".format(min( num, len(uniL[inp[0]])) )
        for (t, df) in uniL[inp[0]][:num]:
          RWcount += df
          print t, df
        print "The left sub-terms of ", inp[1], " have ", len(uniR[inp[1]]),  " items. List {0} of them:".format(min( num, len(uniR[inp[1]])) )
        for (t, df) in uniR[inp[1]][:num]:
          LWcount += df
          print t, df
        #RWcount -= uniL[inp[0]][0][1] # delete duplicated term and df
        if os.name == 'nt':
          print 'too many to show, save to file :\nall_RLgrams_for'+inp+'.txt(in '+os.getcwd()+'\\result\\'+corpus+')'
          print 'file in progress...'
          if not os.path.exists('result/'+corpus): os.makedirs('result/'+corpus)
          result = codecs.open('result\\'+corpus+'\\all_RLgrams_for'+inp+'.txt', 'w')
        elif os.name == 'posix':
          print 'too many to show, save to file :\nall_RLgrams_for'+inp+'.txt(in '+os.getcwd()+'/result/'+corpus+')'
          print 'file in progress...'
          if not os.path.exists('result/'+corpus): os.makedirs('result/'+corpus)
          result = codecs.open('result//'+corpus+'//all_RLgrams_for'+inp+'.txt', 'w')
        result.write("\nThe right sub-terms of "+inp[0]+" have "+str(len(uniL[inp[0]]))+" items.\n")
        for (t, df) in uniL[inp[0]]:
          if len(t) == 1: result.write(inp[0]+str(t)+','+str(df)+'\n'); RWcount += df; RDcount += 1
        result.write("and have "+str(RDcount)+" items in doubleword.\n")
        result.write("The left sub-terms of "+inp[1]+" have "+str(len(uniR[inp[1]]))+" items.\n")
        for (t, df) in uniR[inp[1]]:
          if len(t) == 1: result.write(str(t)+inp[1]+','+str(df)+'\n'); LWcount += df; LDcount += 1
        result.write("and have "+str(LDcount)+" items in doubleword.\n")
        RWcount -= uniL[inp[0]][0][1] # delete duplicated term and df
        result.write("Total right and left sub-terms frequency of "+inp+" is "+str(RWcount+LWcount)+"\n")
        result.write("and have "+str(RDcount+LDcount)+" items in doubleword.\n") 
      else:
        print "The right sub-terms of ", inp[0], " have ", len(uniL[inp[0]]), " items. List {0} of them:".format(min( num, len(uniL[inp[0]])) )
        for (t, df) in uniL[inp[0]][:num]:
          RWcount += df
          print t, df
        print "The left sub-terms of ", inp[1], " have ", len(uniR[inp[1]]),  " items. List {0} of them:".format(min( num, len(uniR[inp[1]])) )
        for (t, df) in uniR[inp[1]][:num]:
          LWcount += df
          print t, df
          #RWcount -= uniL[inp[0]][0][1] # delete duplicated term and df
        print "Total right and left sub-terms of ", inp, " have ", RWcount+LWcount, " items" 

def RLgramsALL(word, result, inp):
  uL = defaultdict(list)
  uR = defaultdict(list)
  uniL = defaultdict(list)
  uniR = defaultdict(list)
  for w in word:
    if len(w) < 2: continue
    uL[w[0]].append(w[1:])
    uR[w[-1]].append(w[:-1])

  for k,lst in uL.iteritems():
    dic = defaultdict(int)
    for u in lst: dic[u] += 1
    for kd, vd in sorted(dic.items(), key=myig(), reverse=True):
      uniL[k].append((kd, vd))
    
  for k,lst in uR.iteritems():
    dic = defaultdict(int)
    for u in lst: dic[u] += 1
    for kd, vd in sorted(dic.items(), key=myig(), reverse=True):
      uniR[k].append((kd, vd))

#  print 'word=',type(word),'inp=',type(inp)
  RWcount = 0; LWcount = 0; RDcount = 0; LDcount = 0
  result.write("\nThe right sub-terms of "+inp[0]+" have "+str(len(uniL[inp[0]]))+" items.\n")
  for (t, df) in uniL[inp[0]]:
    if len(t) == 1: result.write(inp[0]+str(t)+","+str(df)+"\n"); RWcount += df; RDcount += 1
  result.write("and have "+str(RDcount)+" items in doubleword.\n")
  result.write("The left sub-terms of "+inp[1]+" have "+str(len(uniR[inp[1]]))+" items.\n")
  for (t, df) in uniR[inp[1]]:
    if len(t) == 1: result.write(str(t)+inp[1]+","+str(df)+"\n"); LWcount += df; LDcount += 1
  result.write("and have "+str(LDcount)+" items in doubleword.\n")
  RWcount -= uniL[inp[0]][0][1] # delete duplicated term and df
  result.write("Total right and left sub-terms frequency of "+inp+" is "+str(RWcount+LWcount)+"\n")
  result.write("and have "+str(RDcount+LDcount)+" items in doubleword.\n")

def demo_findPOSpattern(words_tagged, num=20):
  print "List the most {0} ambiguous words ...".format(num)
  i = 0
  data = nltk.ConditionalFreqDist(words_tagged)
  for word in data.conditions(): 
    if len(data[word]) > 3:
      i += 1
      tags = data[word].keys()
      print word.encode('big5'), "=>", ', '.join(tags)
      if i >= num: break
  while True:
    inp = raw_input("Enter a 3-frame pattern (example:'把 N V', 0 to exit): ")
    if inp == '0': break
    inp = inp.decode('big5')
    P = inp.split(' ')
    for (w1,t1), (w2,t2), (w3,t3) in nltk.trigrams(words_tagged):
      W = (w1, w2, w3); T = (t1, t2, t3); 
      flag = 0
      for i in range(len(W)):
      	if len(P[i]) == 0: break # if no input pattern then show dialog again
        if ord(P[i]) < 128: # an English tag name 
          if T[i].startswith(P[i]): flag += 1
        elif W[i] == P[i]: flag += 1
      if flag == len(W):
        print ', '.join(W)



def LoadCC(root, regex, enc):
  print "Loading corpus:", root, "..."
#  stbp = SyntaxCorpusReader_LACC(
#  '/Users/sam/nltk_data/corpora/sinica_treebank', 
#  'parsed', encoding='utf-8')
  stbp = SyntaxCorpusReader_LACC(root, regex, encoding=enc)
#  word = stbp.words()
#  sent = stbp.sents()
  if re.search('(ASBC|test|ChineseTextBook)', root):
#    return stbp.tagged_words(simplify_tags=True)
    return stbp.tagged_words()
  else: 
    return stbp.words()



if __name__ == '__main__':

  words = []; words_tagged = []
  while True:
    print '''
    Corpora for text analysis:
      1. Standard Segmented Corpus from Academia Sinica (partial version) 
      2. Standard Segmented Corpus from Academia Sinica
      3. Academia Sinica Balaced Corpus with tagged texts (partial version) 
      4. Academia Sinica Balaced Corpus with tagged texts
      5. Chinese Text Book
      6. Get all RLterms in Chinese Text Book 
    '''
    inp = raw_input("Select a corpus for analysis (enter one of the above number 1-6):")
    if inp == '1': words = LoadCC('SSC2-3_u', '.*.seg', 'utf8')
    if inp == '2': words = LoadCC('SSC_u', '.*.seg', 'utf8')
    if inp == '3': 
      words_tagged = LoadCC('ASBC2-3_u', '.*', 'utf8')
#nltk.corpus.reader.util.concat() 
# def words(self, fileids=None):
#...     return concat([[w for w in open(fileid).read().split('\n') if w]
#...                    for fileid in self.abspaths(fileids)])
#      words = nltk.corpus.reader.util.concat([[w for (w, t) in words_tagged]])
      words = [w for (w, t) in words_tagged]
    if inp == '4': 
      words_tagged = LoadCC('ASBC_u', '.*', 'utf8')
#      words = nltk.corpus.reader.util.concat([[w for (w, t) in words_tagged]])
      words = [w for (w, t) in words_tagged]
    if inp == '5': words = LoadCC('ChineseTextBook', '.*.txt', 'utf8')
    if inp == '6': 
      words_tagged = LoadCC('ChineseTextBook', '.*.txt', 'big5')
      words = [w for (w, t) in words_tagged]
      result = codecs.open('result_all.txt', 'w', 'big5')
      for w in words:
        if len(w) == 2: RLgrams(words, w)
#      SingleWords = []
#      for w in words:
#        for t in w: SingleWords.append(t)
#      for i in range(len(SingleWords)-1):
#        print SingleWords[i]+SingleWords[i+1]
#      	 tt = ''; tt = SingleWords[i]+SingleWords[i+1]
#        RLgrams(words, tt)
      result.close()
    if inp in '123456': break
  print "type(words)=", type(words), "\ntype(words_tagged)=", type(words_tagged)
  text = MyText(words)
  #print "The first 20 words of words:", ','.join(w for w in words[:20])
  #print "The first 20 words of text:", ','.join(w for w in text[:20])
  print "The first 20 tuples of words_tagged:", ','.join('/'.join([w,t]) for (w,t) in words_tagged[:20])
  MoreMenu = ''
  if inp in '34': MoreMenu = '8. Find text patterns with POS tags'
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
    print "Number of words:", len(words), ", len(text)=", len(text)
    print "Number of tagged words:", len(words_tagged)
    inp = raw_input('Select a number from the above for analysis (0 to exit):'); 
    print "inp='" + inp + "'"
    if inp == '0': exit(0)
    if inp == '1': demo_concordance(text, "")
    if inp == '2': demo_collocations(text)
    if inp == '3': demo_similar(text, "")
    if inp == '4': demo_common_context(text)
    if inp == '5': demo_findall(text)
    if inp == '6': RLgrams(words, inp)
    if inp == '7': demo_generate(text)
    if inp == '8' and MoreMenu: demo_findPOSpattern(words_tagged)
#    if inp == '9': demo_vocab(text)
  


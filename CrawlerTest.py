#-------------------------------------------------------------------------------
# coding:        utf-8
# Version:      python3.2
# Purpose:抓取测试 pageCrawl,抓取osc的最新推荐博客列表
#分析出博客链接、标题、内容简介、作者和发布时间
#
#声明：本例只供技术交流和练习使用，如侵害了您的权利，请发邮件给daokun66@163.com通知删除
# Author:      zdk
# Created:     07/03/2013
#-------------------------------------------------------------------------------
import httplib2
from html.parser import HTMLParser


def getPageContent(url):
    '''
    使用httplib2用编程的方式根据url获取网页内容
    将bytes形式的内容转换成utf-8的字符串
    '''
    #使用ie9的user-agent，如果不设置user-agent将会得到403禁止访问
    headers={'user-agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'}
    if url:
         response,content = httplib2.Http().request(url,headers=headers)
         if response.status == 200 :
            return str(content,'utf-8')


class MyHtmlParser(HTMLParser):
    '''
    根据html内容解析出相应的标签，获取标签的属性或相应的数据并输出
    '''
    def __init__(self):
        HTMLParser.__init__(self)
        self.href = []      #存放博客链接
        self.title = []     #存放博客标题
        self.summary = []   #存放博客内容简介
        self.author = []    #存放作者和发布时间

        self.ul = None          #是否进入到了ul标签
        self.ul_li = None       #是否进入到了ul里的li标签
        self.ul_li_h3 = None    #是否进入到了ul里的li里的h3标签
        self.ul_li_h3_a = None  #是否进入到了ul里的li里的h3里的a标签
        self.ul_li_p = None     #是否进入到了ul里的li里的p标签
        self.ul_li_div = None   #是否进入到了ul里的li里的div标签

    def handle_starttag(self, tag, attrs):
        if tag == 'ul' :
            for name,value in attrs:
                if name == 'class' and value =='BlogList':
                    self.ul = 1   #进入到了ul标签
                    break
        elif self.ul and tag == 'li':
            self.ul_li = 1        #进入到了ul里的li标签
        elif self.ul and self.ul_li and tag == 'h3':
            self.ul_li_h3 = 1     #进入到了ul里的li里的h3标签
        elif self.ul and self.ul_li and self.ul_li_h3 and  tag== 'a':
            self.ul_li_h3_a = 1   #进入到了ul里的li里的h3里的a标签
            for name,value in attrs:
                if name == 'href':
                    self.href.append(value)    #取博客链接
                    print("博客链接:"+value)   #输出博客链接
        elif self.ul and self.ul_li and tag == 'p':
            self.ul_li_p = 1    #进入到了ul里的li里的p标签
        elif self.ul and self.ul_li and tag == 'div':
            for name,value in attrs:
                if name == 'class' and value =='date':
                    self.ul_li_div = 1 #进入到了ul里的li里的class='date'的div标签
                    break

    def handle_data(self, text):
        if self.ul and self.ul_li and self.ul_li_h3 and self.ul_li_h3_a :
             self.title.append(text) #链接里面的数据即为标题
             print("博客标题:"+text)
        elif self.ul and self.ul_li and self.ul_li_p :
             self.summary.append(text) #ul里的li里的p标签的内容为博客内容简介
             print("博客简介:"+text)

        elif self.ul and self.ul_li and self.ul_li_div :
             self.author.append(text)   #ul里的li里的div标签的内容为作者和更新时间
             print("博客作者和更新时间:"+text)

    def handle_endtag(self, tag):
        if tag == 'a' and self.ul and self.ul_li and self.ul_li_h3 and self.ul_li_h3_a :
            #退出了ul里的li里的h3里的a标签
            #重置h3和a的标识数据
            self.ul_li_h3 = None
            self.ul_li_h3_a = None
        elif tag == 'p' and self.ul and self.ul_li and self.ul_li_p:
            #退出了ul里的li里的p标签
            self.ul_li_p = None
        elif tag == 'div' and self.ul and self.ul_li and self.ul_li_div:
            #退出了ul里的li里的div标签
            self.ul_li_div = None
        elif tag == 'li' and self.ul and self.ul_li :
            #退出了ul里的li标签
            self.ul_li = None
        elif tag == 'ul' and self.ul :
            #退出了ul标签
            self.ul = None



if __name__ == '__main__':
    pageC = getPageContent('http://www.oschina.net/blog/more?p=1')
    my = MyHtmlParser()
    my.feed(pageC)

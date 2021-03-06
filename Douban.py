# coding:utf-8
""" 一个简单的Python爬虫,用于抓取豆瓣电影TOP100的电影名称
Anthor: Max Kwok
Version: 0.0.1
Date: 2016-01-18
Language: Python 2.7.10
Editor: pycharm 5
"""
import string
import re
import urllib2


class DouBanSpider(object):
    """page:用于标示当前所处的抓取页面
       cur_url:用于标示当前争取抓取页面的url
       dates:存储处理好的抓取到的电影名称
       _top_num:用于记录当前的top号码
       cur_page:标示当前所抓取的网站页码
       Returns:返回抓取到整个页码的HTML(unicode 编码)
       URLError: url引发的异常
       my_page: 传入页面的HTML文本用于正则匹配
    """
    def __init__(self):
        self.page = 1
        self.cur_url = "http://movie.douban.com/top250?start={page}&filter=&type="#豆瓣排名前250的网页
        self.dates = []#存取处理好的抓取到的电影名称
        self._top_num = 1
        print "豆瓣电影爬虫准备就绪,准备爬取数据..."

    def get_page(self,cur_page):#根据当前页码爬取网页HTML
        url = self.cur_url
        try:
            my_page = urllib2.urlopen(url.format(page=(cur_page - 1)* 25)).read().decode("utf-8")
        except urllib2.URLError, e:
            if hasattr(e,"code"):
                print "The server couldn't fulfill the request."
                print "Error code : %s" % e.code
            elif hasattr(e,"reason"):
                print "We failed to reach a server. Please check your url and read the Reason."
                print "Reason: %s" % e.reason
        return my_page

    def find_title(self,my_page):#通过返回的整个网页HTML,正则匹配前100的电影名称
        temp_date = []
        movie_items = re.findall(r'<span.*?class="title">(.*?)</span>', my_page,re.S)
        for index, item in enumerate(movie_items):
            if item.find("&nbsp") == -1:
                temp_date.append("Top"+str(self._top_num)+" "+item)
                self._top_num += 1
        self.dates.extend(temp_date)

    def start_spider(self):#爬虫入口,并控制爬虫抓取页面的范围
        while self.page <=4:
            my_page = self.get_page(self.page)
            self.find_title(my_page)
            self.page +=1

def main():
    print """
        ########################
        一个简单的豆瓣电影前100爬虫
        Author: Max Kwok
        Version: 0.0.1
        Date: 2016-01-18
        ########################
        """
    my_spider = DouBanSpider()
    my_spider.start_spider()
    for item in my_spider.dates:
        print item
    print "豆瓣爬虫爬取结束..."

if __name__=='__main__':
    main()



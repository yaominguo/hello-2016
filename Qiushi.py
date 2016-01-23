# _*_ coding:utf-8 _*_
import urllib
import urllib2
import re
import thread
import time

class QSBK:#糗事百科爬虫类

    def __init__(self):#初始化,定义变量
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0(compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}#初始化headers
        self.stories = []#存放段子的变量,每个元素是每一页的段子们
        self.enable = False#存放程序是否继续运行的变量

    def getPage(self,pageIndex):#传入某一页的索引获得页面代码
        try:
            url = 'http://www.qiushibaike.com/hot/page' + str(pageIndex)
            request = urllib2.Request(url,headers = self.headers)#构建请求的request
            response = urllib2.urlopen(request)#利用urlopen获取页面代码
            pageCode = response.read().decode('utf-8')#将页码转化编码
            return  pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print "连接糗事百科失败,错误原因:",e.reason
                return  None

    def getPageItems(self,pageIndex):#传入某页代码,返回本页不带图片的段子列表
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页码加载失败...."
            return None
        pattern = re.compile('<div.*?author clearfix">.*?<img.*?<a.*?<h2>(.*?)</h2>.*?<div.*?content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)
        items = re.findall(pattern,pageCode)
        pageStories = []#用了存储每页的段子们
        for item in items:
            haveImg = re.search("img",item[3])#是否含有图片
            if not haveImg:#如果不含图片,加入list中
                replaceBR = re.compile('<br/')
                text = re.sub(replaceBR,'\n',item[1])
                #item[0]是发布者,item[1]是内容,item[2]是发布时间,item[4]是点赞数
                pageStories.append([item[0].strip(),text.strip(),item[2].strip(),item[4].strip()])
        return pageStories

    def loadPage(self):#加载并提取页面内容,加到列表中
        if self.enable == True:
            if len(self.stories)<2:#如果当前未看的页数少于2,则加载新一页
                pageStories = self.getPageItems(self.pageIndex)#获取新一页
                if pageStories:#将该页的段子放到全局list中
                    self.stories.append(pageStories)
                    self.pageIndex += 1 #获取完后页码加一,表示读取下一页

    def getOneStory(self,pageStories,page):#调用该方法,每次回车打印一个段子
        for story in pageStories:#遍历一页的段子
            input = raw_input()#等待用户输入
            self.loadPage()#每当输入一次回车,判断是否需要加载新页面
            if input == "Q":#输入Q则结束程序
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t发布时间:%s\t赞:%s\n%s" %(page,story[0],story[2],story[3],story[1])

    def start(self):#开始方法
        print u"正在读取糗事百科,按回车查看新段子,Q键退出."
        self.enable = True#使变量为true,程序可以正常运行
        self.loadPage()#先加载一页内容
        nowPage = 0#局部变量,控制当前都到第几页
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]#从全局list中获取一页段子
                nowPage += 1#当前页码加一
                del self.stories[0]#将全局list中第一个元素删除,因为已经退出
                self.getOneStory(pageStories,nowPage)#输出该页段子

spider = QSBK()
spider.start()





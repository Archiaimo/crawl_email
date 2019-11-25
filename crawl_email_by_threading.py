import urllib.request
import urllib
import threading
import re
import time
from collections import deque
import queue
#广度挖掘所有链接中的邮箱

def geteveryurl(data):
    alllist=[]
    mylist1=[]
    mylist2=[]
    mylist1=getallhttp(data)
    if len(mylist1)>0:
        mylist2=getabsurl(mylist1[0],data)
    alllist.extend(mylist1)
    alllist.extend(mylist2)
    return alllist

def getabsurl(url,data):
    try:
        urlregex=re.compile('href=\'(.*?)\"',re.IGNORECASE)
        httplist= urlregex.findall(data)
        newhttplist=httplist.copy()#深拷贝
        for data in newhttplist:
            if data.find('http://')!=-1:
                httplist.remove(data)
            if data.find('javascript')!=-1:
                httplist.remove(data)
        hostname=gethostname(url)
        if hostname != None:
            for i in range(len(httplist)):
                httplist[i]=hostname + httplist[i]

        return httplist
    except:
        return []

def gethostname(httpstr):
    try:
        hostregex = re.compile(r'(http://\S*?)/',re.IGNORECASE)
        mylist = hostregex.findall(httpstr)
        if len(mylist)==0:
            return None
        else:
            return mylist[0]
    except:
        return None



def getallhttp(data):
    try:
        httpregex = re.compile(r'(http://\S*?)[\"|>|)]',re.IGNORECASE)
        mylist = httpregex.findall(data)
        return mylist
    except:
        return ''


def getallemail(data):
    try:
        mailregex = re.compile(r'([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})',re.IGNORECASE)
        mylist = mailregex.findall(data)
        return mylist
    except:
        return ''

def getdata(url):
    try:
        data=urllib.request.urlopen(url).read().decode('utf-8')
        return data
    except:
        return ''#发生异常返回空

def BFS(urlstr):
    global emailqueue
    urlqueue=deque([])#创建url队列
    urlqueue.append(urlstr)#插入url队列
    while len(urlqueue)!=0:
        url =urlqueue.popleft()#弹出一个url
        print(url)#打印url链接
        pagedata=getdata(url)#获取网页源代码
        emaillist=getallemail(pagedata)#提取邮箱列表
        if len(emaillist)!=0:#邮箱不为空
            for email in emaillist:#打印所有邮箱
                print(email)
                emailqueue.put(email)
        newurllist=geteveryurl(pagedata)#抓取所有url
        if len(newurllist)!=0:#判断长度
            for urlstr in newurllist:#循环处理每一个url
                if urlstr not in urlqueue:#判断在不在队列中
                    urlqueue.append(urlstr)#插入

def savemail():
    global emailqueue
    mailfile = open('mail.txt','ab')
    while True:
        time.sleep(3)
        while not emailqueue.empty():
            data=emailqueue.get()
            mailfile.write(data + '\r\n')
            mailfile.flush()
    mailfile.close()


emailqueue=queue.Queue()
urlqueue=queue.Queue()
sem=threading.Semaphore(10)
timethread=threading.Timer(5,savemail)  #5秒以后开启一个线程来保存
timethread.start()


BFS('http://bbs.tianya.cn/post-140-393974-2.shtml')
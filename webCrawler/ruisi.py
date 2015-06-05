# coding=utf-8
import urllib2, re, sys, threading, time


def getInfo(myurl, seWord):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    req = urllib2.Request(
        url=myurl,
        headers=headers
    )
    time.sleep(0.3)
    response = urllib2.urlopen(req)
    html = response.read()
    html = unicode(html, 'utf-8')
    timeMatch = seWord.search(html)
    if timeMatch:
        s = timeMatch.groups()
        return s[0]
    else:
        return None

def safeGet(myid, myurl, seWord):
    try:
        return getInfo(myurl, seWord)
    except:
        try:
            return getInfo(myurl, seWord)
        except:
            httperrorfile = open(file5, 'a')
            info = '%d %s\n' % (myid, 'httperror')
            httperrorfile.write(info)
            httperrorfile.close()
            return 'httperror'


def searchWeb(idArr):
    for id in idArr:
        sexUrl = url1 % (id)
        timeUrl = url2 % (id)
        sex = safeGet(id,sexUrl, sexRe)
        if not sex:
            sex = safeGet(id,timeUrl, sexRe)
        time = safeGet(id,timeUrl, timeRe)

        if (sex is 'httperror') or (time is 'httperror') :
            pass
        else:
            if sex:
                info = '%d %s' % (id, sex)
                if time:
                    info = '%s %s\n' % (info, time)
                    wfile = open(file1, 'a')
                    wfile.write(info)
                    wfile.close()
                else:
                    info = '%s %s\n' % (info, 'notime')
                    errtimefile = open(file2, 'a')
                    errtimefile.write(info)
                    errtimefile.close()
            else:
                notexist = safeGet(id,sexUrl, notexistRe)
                if notexist is 'httperror':
                    pass
                else:
                    if notexist:
                        notexistfile = open(file3, 'a')
                        info = '%d %s\n' % (id, 'notexist')
                        notexistfile.write(info)
                        notexistfile.close()
                    else:
                        unkownsexfile = open(file4, 'a')
                        info = '%d %s\n' % (id, 'unkownsex')
                        unkownsexfile.write(info)
                        unkownsexfile.close()

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if len(sys.argv) != 3:
        print 'usage: python ruisi.py <startNum> <endNum>'
        sys.exit(-1)
    global sexRe,timeRe,notexistRe,url1,url2,file1,file2,file3,file4,startNum,endNum,file5
    startNum=int(sys.argv[1])
    endNum=int(sys.argv[2])
    sexRe = re.compile(u'em>\u6027\u522b</em>(.*?)</li')
    timeRe = re.compile(u'em>\u4e0a\u6b21\u6d3b\u52a8\u65f6\u95f4</em>(.*?)</li')
    notexistRe = re.compile(u'(p>)\u62b1\u6b49\uff0c\u60a8\u6307\u5b9a\u7684\u7528\u6237\u7a7a\u95f4\u4e0d\u5b58\u5728<')
    url1 = 'http://rs.xidian.edu.cn/home.php?mod=space&uid=%s'
    url2 = 'http://rs.xidian.edu.cn/home.php?mod=space&uid=%s&do=profile'
    file1 = 'ruisi\\correct%s-%s.txt' % (startNum, endNum)
    file2 = 'ruisi\\errTime%s-%s.txt' % (startNum, endNum)
    file3 = 'ruisi\\notexist%s-%s.txt' % (startNum, endNum)
    file4 = 'ruisi\\unkownsex%s-%s.txt' % (startNum, endNum)
    file5 = 'ruisi\\httperror%s-%s.txt' % (startNum, endNum)
    searchWeb(xrange(startNum,endNum))
    # numThread = 10
    # searchWeb(xrange(endNum))
    # total = 0
    # for i in xrange(numThread):
    # data = xrange(1+i,endNum,numThread)
    #     total  =+ len(data)
    #     t=threading.Thread(target=searchWeb,args=(data,))
    #     t.start()
    # print total


main()


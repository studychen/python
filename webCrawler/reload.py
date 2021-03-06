# coding=utf-8
#这儿是针对httperror的id进行重新爬虫
#代码和ruisi.py很像
import urllib2, re, sys, time,os


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
    global sexRe,timeRe,notexistRe,url1,url2,file1,file2,file3,file4,startNum,endNum,file5
    sexRe = re.compile(u'em>\u6027\u522b</em>(.*?)</li')
    timeRe = re.compile(u'em>\u4e0a\u6b21\u6d3b\u52a8\u65f6\u95f4</em>(.*?)</li')
    notexistRe = re.compile(u'(p>)\u62b1\u6b49\uff0c\u60a8\u6307\u5b9a\u7684\u7528\u6237\u7a7a\u95f4\u4e0d\u5b58\u5728<')
    url1 = 'http://rs.xidian.edu.cn/home.php?mod=space&uid=%s'
    url2 = 'http://rs.xidian.edu.cn/home.php?mod=space&uid=%s&do=profile'
    file1 = '..\\newnew\\correct_re.txt'
    file2 = '..\\newnew\\errTime_re.txt'
    file3 = '..\\newnew\\notexist_re.txt'
    file4 = '..\\newnew\\unkownsex_re.txt'
    file5 = '..\\newnew\\httperror_re.txt'

    for filename in os.listdir(r'E:\pythonProject\ruisi'):
        if filename.startswith('httperror'):
            count = 0
            newName = 'E:\\pythonProject\\ruisi\\%s' % (filename)
            readFile = open(newName,'r')
            oldLine = '0'
            for line in readFile:
                newLine =  line
                if (newLine != oldLine):
                    nu = newLine.split()[0]
                    oldLine = newLine
                    count += 1
                    searchWeb((int(nu),))
            print "%s deal %s lines" %(filename, count)

    # searchWeb(xrange(startNum,endNum))
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


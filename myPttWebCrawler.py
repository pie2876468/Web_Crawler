import requests
import time
import json
from bs4 import BeautifulSoup


PTT_URL = 'https://www.ptt.cc'
global nextWebPath
nextWebPath = '/bbs/Gossiping/index.html'

def getWebPage(WebPath):
    try:
        response = requests.get(
            url= PTT_URL+WebPath,
            cookies={'over18': '1'}
        )
        if response.status_code == 200:
            return response.text
        else:
            print("Error: Cannot get web page for", WebPath)
            return None
    except Exception as e:
        return None

def getWebArticals(response,todayDate):
    soup = BeautifulSoup(response, 'html5lib')
    nextWebDiv = soup.find("div", "btn-group btn-group-paging")
    global nextWebPath
    nextWebPath = nextWebDiv.find_all('a')[1]['href']
    pageinfo = []
    posts = soup.find_all("div", "r-ent")
    for post in posts:
        tmpDate = post.find("div","date").text.strip()
        if tmpDate == todayDate:
            tmpPushNumber = post.find("div","nrec").text
            if tmpPushNumber=="爆":
                tmpPushNumber = 100
            elif tmpPushNumber.startswith('X'):
                tmpPushNumber = -1
            elif tmpPushNumber=="":
                tmpPushNumber = 0
            else:
                tmpPushNumber = int(tmpPushNumber)
            if post.find("a"):
                tmpTitle = post.find("div","title").text.strip()
                tmpHref = PTT_URL + post.find("div","title").find_all('a')[0]['href']
                tmpAuthor = ""
                if post.find('div', 'author'):
                    tmpAuthor = post.find('div', 'author').text
                tmp_post = {
                    "title": tmpTitle,
                    "number": tmpPushNumber,
                    "author": tmpAuthor,
                    "href": tmpHref,
                    "date": tmpDate
                }
                pageinfo.append(tmp_post)
    return pageinfo

if __name__ == '__main__':
    todayDate = time.strftime("%m/%d").lstrip('0')
    newPageInfo = getWebArticals(getWebPage(nextWebPath),todayDate)
    totalPost = [];
    cnt = 0;
    while newPageInfo:
        print("Reading Page %d" % (cnt))
        cnt+=1
        totalPost += newPageInfo
        newPageInfo = getWebArticals(getWebPage(nextWebPath),todayDate)
        if cnt>1000:
            break;

    print('今天有', len(totalPost), '篇文章')
    threshold = 99
    print('熱門文章(> %d 推):' % (threshold))
    #print post with tmpPushNumber>100
    for post in totalPost:
        if int(post["number"])>=threshold:
            print(post)
    print("Done!!!!!!!!!!!!!!!!!!!")

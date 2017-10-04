import urllib
import urllib.request
import urllib.parse
import bs4
import re
import os
from concurrent.futures import ThreadPoolExecutor


def deleteTag(x):
    return re.sub("<[^>]*>", "", x)


def getComments(lang='all'):
    def innerHTML(s, sl=0):
        ret = ''
        for i in s.contents[sl:]:
            if i is str:
                ret += i.strip()
            else:
                ret += str(i)
        return ret

    def fText(s):
        if len(s): return innerHTML(s[0]).strip()
        return ''

    def replace(l, X, Y):
        for i, v in enumerate(l):
            if (str(v).index(X) > -1):
                l.pop(i)
                l.insert(i, str(v).replace(X,Y))
        return l

    retList = []
    colSet = set()

    page = 1
    while 1:
        try:
            f = urllib.request.urlopen("http://store.steampowered.com/search/?tags=1742&page="+str(page))
            data = f.read().decode('utf-8')
            #print(data)
        except:
            print("URL ERROR or Not Data")
            break

        soup = bs4.BeautifulSoup(data, "html.parser")
        srlists = soup.find_all('span', {'class': 'title'})


        if (len(srlists) < 1) : break

        list(set(srlists))  # 중복제거
        srlists = replace(srlists, '<span class="title">','')
        srlists = replace(srlists, '</span>', '')

        #print(srlists)
        print(page, len(srlists), srlists)
        for x in srlists:
            retList.append(x)

        page += 1
    return retList

def fetch():
    outname = 'SteamGameList.txt'
    # english 대신에 korean을 넣으면 한국어를 긁어옵니다.
    rs = getComments('english')
    if not len(rs): return
    f = open(outname, 'w', encoding='utf-8')
    for r in rs:
        f.write(r+"\n")
    f.close()

with ThreadPoolExecutor(max_workers=5) as executor:
	executor.submit(fetch)

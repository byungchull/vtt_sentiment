import urllib
import urllib.request
import urllib.parse
import bs4
import re
import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode, quote_plus

def deleteTag(x):
    return re.sub("<[^>]*>", "", x)

def getPlots(lang='all'):
    #retList = []

    inname = 'SteamGameList.txt'
    in_file = open(inname, "r", encoding='utf-8')

    i=1

    # HTML Parsing 을 위해서 임시 주석처리
    logf = open("wikiLogSearch.txt", 'w', encoding='utf-8')
    plotf = open("wikiPlotText.txt","w", encoding='utf-8')
    while True:
        gameTitle = in_file.readline().replace("\n", "")
        if not gameTitle:
            break

        # 특수문자제거 (일본어, 중국어도 제거됨)
        #gameTitle = re.sub('[^가-힣0-9a-zA-Z:\-\\s]', '', gameTitle)

        # 공백을 _로 변경, : 문자 이후로 제거해야 검색되는 경우도 있고, 소문자로 검색해야 검색되는 경우도 있음 (게임명 필터링 강화 필요)
        # 공백을 _로 바꾸면 485개, 공백으로 하면 459개
        #gameTitle = gameTitle.replace(" ","_")

        #gameTitle = gameTitle.replace(" ", "_")

        # 일부 특수문자 제거
        gameTitle = gameTitle.replace("™", "")
        gameTitle = gameTitle.replace("®", "")

        payload = {'search': gameTitle, 'title': 'Special:Search', 'fulltext':'','go':'Go'}
        result = urlencode(payload, quote_via=quote_plus)

        print("["+str(i)+"] GameTitle : ", gameTitle)
        print("URL : https://en.wikipedia.org/w/index.php?" + result)
        logf.write("\n\nGameTitle : "+gameTitle)
        logf.write("\nURL : https://en.wikipedia.org/w/index.php?" + result +"\n")

        try:
            f = urllib.request.urlopen("https://en.wikipedia.org/w/index.php?"+result)
            data = f.read().decode('utf-8')
            logf.write(data)

            startNum = data.find('<h3><span class="mw-headline" id="Plot">Plot</span>')
            endNum = data.find('<span class="mw-headline"', startNum+10)

            if (startNum < 0):
                startNum = data.find('<h3><span class="mw-headline" id="Synopsis">Synopsis</span>')
                endNum = data.find('<span class="mw-headline"', startNum + 10)

            if (startNum < 0):
                startNum = data.find('<h2><span class="mw-headline" id="Plot">Plot</span>')
                endNum = data.find('<h2><span class="mw-headline"', startNum + 10)

            if (startNum > 0 and startNum < endNum) :
                startPlot = data.find("<p>", startNum)
                strPlot = data[startPlot:endNum]

                print(deleteTag(strPlot))
                plotf.write("\n\n["+str(i)+"] GameTitle : " + gameTitle + "\n")
                plotf.write(deleteTag(strPlot))
            i+=1
        except Exception as ex:
            print(ex)
            logf.write(str(ex))
            logf.write("\n")

        # HTML Parsing을 위해서 단 1회만 실행

    logf.close()
    plotf.close()

'''
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
'''


'''
def fetch():
    outname = 'WikiPlot.txt'

    # english 대신에 korean을 넣으면 한국어를 긁어옵니다.
    rs = getPlots('english')
    if not len(rs): return
    f = open(outname, 'w', encoding='utf-8')
    for r in rs:
        f.write(r+"\n")
    f.close()
'''

# english 대신에 korean을 넣으면 한국어를 긁어옵니다.
getPlots('english')

'''
with ThreadPoolExecutor(max_workers=5) as executor:
	executor.submit(fetch)
'''

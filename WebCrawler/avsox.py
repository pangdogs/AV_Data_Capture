import sys
sys.path.append('..')
import re
from lxml import etree
import json
from bs4 import BeautifulSoup
from ADC_function import *
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors = 'replace', line_buffering = True)

def getActorPhoto(htmlcode): #//*[@id="star_qdt"]/li/a/img
    soup = BeautifulSoup(htmlcode, 'lxml')
    a = soup.find_all(attrs={'class': 'avatar-box'})
    d = {}
    for i in a:
        l = i.img['src']
        t = i.span.get_text()
        p2 = {t: l}
        d.update(p2)
    return d
def getTitle(a):
    try:
        html = etree.fromstring(a, etree.HTMLParser())
        result = str(html.xpath('/html/body/div[2]/h3/text()')).strip(" ['']") #[0]
        return result.replace('/', '')
    except:
        return ''
def getActor(a): #//*[@id="center_column"]/div[2]/div[1]/div/table/tbody/tr[1]/td/text()
    soup = BeautifulSoup(a, 'lxml')
    a = soup.find_all(attrs={'class': 'avatar-box'})
    d = []
    for i in a:
        d.append(i.span.get_text())
    return d
def getStudio(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//p[contains(text(),"制作商: ")]/following-sibling::p[1]/a/text()')).strip(" ['']").replace("', '",' ')
    return result1
def getRuntime(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//span[contains(text(),"长度:")]/../text()')).strip(" ['分钟']")
    return result1
def getLabel(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//p[contains(text(),"系列:")]/following-sibling::p[1]/a/text()')).strip(" ['']")
    return result1
def getNum(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//span[contains(text(),"识别码:")]/../span[2]/text()')).strip(" ['']")
    return result1
def getYear(release):
    try:
        result = str(re.search('\d{4}',release).group())
        return result
    except:
        return release
def getRelease(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//span[contains(text(),"发行时间:")]/../text()')).strip(" ['']")
    return result1
def getCover(htmlcode):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[2]/div[1]/div[1]/a/img/@src')).strip(" ['']")
    return result
def getCover_small(htmlcode):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('//*[@id="waterfall"]/div/a/div[1]/img/@src')).strip(" ['']")
    return result
def getTag(a):  # 获取演员
    soup = BeautifulSoup(a, 'lxml')
    a = soup.find_all(attrs={'class': 'genre'})
    d = []
    for i in a:
        try:
            d.append(translateTag_to_sc(i.get_text()))
        except:
            pass
    d.append('无马赛克')
    return d
def getSeries(htmlcode):
    try:
        html = etree.fromstring(htmlcode, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
        result1 = str(html.xpath('//span[contains(text(),"系列:")]/../span[2]/text()')).strip(" ['']")
        return result1
    except:
        return ''

def main(number):
    number = number.upper()

    html = get_html('https://tellme.pw/avsox')
    site = etree.HTML(html).xpath('//div[@class="container"]/div/a/@href')[0]
    a = get_html(site + '/cn/search/' + number)
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()


    links = html.xpath('//*[@id="waterfall"]/div/a/@href')
    titles = html.xpath('//*[@id="waterfall"]/div/a/div[@class="photo-info"]/span/text()[1]')
    ids = html.xpath('//*[@id="waterfall"]/div/a/div[@class="photo-info"]/span/date[1]/text()[1]')

    movieList = []
    for i, e in enumerate(links):
        if str(ids[i]).upper().replace('_', '-') == number.replace('_', '-'):
            movie = {'link':str(links[i]), 'title':str(titles[i]), 'id':str(ids[i])}
            movieList.append(movie)

    index = 0

    if len(movieList) <= 0:
        raise ValueError("no movie")
    elif len(movieList) >= 2:
        for i, link in enumerate(movieList):
            print(str(i+1)+": "+movieList[i]['title'])
            print(movieList[i]['link'])

        index = int(input("input index: "))-1

    if index < 0 or index >= len(movieList):
        raise ValueError("out of range")

    link = movieList[index]['link']

    if link == '':
        raise ValueError("no match")

    web = get_html(link)
    soup = BeautifulSoup(web, 'lxml')
    info = str(soup.find(attrs={'class': 'row movie'}))
    dic = {
        'actor': getActor(web),
        'title': getTitle(web).replace(getNum(web),'').strip(),
        'studio': getStudio(info),
        'outline': '',#
        'runtime': getRuntime(info),
        'director': '', #
        'release': getRelease(info),
        'number': getNum(info),
        'cover': getCover(web),
        'imagecut': 1,
        'tag': getTag(web),
        'label': getLabel(info),
        'year': getYear(getRelease(info)),  # str(re.search('\d{4}',getRelease(a)).group()),
        'actor_photo': getActorPhoto(web),
        'website': link,
        'source': 'avsox.py',
        'series': getSeries(info),
    }
    js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'), )  # .encode('UTF-8')
    return js

if __name__ == "__main__":
    print(main('012717_472'))

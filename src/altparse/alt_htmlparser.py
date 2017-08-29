from urllib.error import HTTPError
from urllib.error import URLError
import urllib.request as url
import lxml.html


def get_links(html_page):
    dom = lxml.html.fromstring(html_page.read())
    outlinks=[]
    for link in dom.xpath('//a/@href'):
        outlinks.append(link)
    return outlinks


def parse(urlToParse):
    html_page=[]
    t=True
    try:
        html_page = url.urlopen(urlToParse)
    except HTTPError as e:
        print("Not a valid url")
        t=False
    except URLError as e:
        print("Not a valid url")
        t=False
    
    return t, html_page


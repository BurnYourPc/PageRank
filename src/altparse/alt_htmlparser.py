from urllib.error import HTTPError
from urllib.error import URLError
import urllib.request as url
import lxml.html

def get_links(link):
    #connection = url.urlopen(link)
    html_page=parse(link)

    dom =  lxml.html.fromstring(html_page.read())
    outlinks=[]
    for link in dom.xpath('//a/@href'):
        outlinks.append(link)
    return outlinks

def parse(urlToParse):
    html_page=[]
    try:
        html_page = url.urlopen(urlToParse)
    except HTTPError as e:
        print("Not a valid url")
    except URLError as e:
        print("Not a valid url")
    
    return html_page

#Sprint(get_links('http://www.sport24.gr/'))

from urllib.error import HTTPError
from urllib.error import URLError

from bs4 import BeautifulSoup
import urllib.request as url


def parse(urlToParse):
    html_page=[]
    t=True
    try:
        html_page = url.urlopen(urlToParse)
    except HTTPError as e:
        print("Not a valid url")
        t=False
    except URLError as e:
        print("Not a valid url")#, e.code)
        t=False
    return t, html_page


def isParsable(link):
    try:
        html_page = url.urlopen(link)
    except HTTPError as e:
        print("Not a valid url")#, e.code)
        return False
    except URLError as e:
        print("Not a valid url")
        return False
    return True


def make_soup(html_page):
    soup = BeautifulSoup(html_page, "html.parser")
    return soup


def get_links(soup):
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links


# print(get_links(make_soup(parse('http://www.sport24.gr/'))))

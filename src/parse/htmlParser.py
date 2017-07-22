from urllib.error import HTTPError
from urllib.error import URLError

from bs4 import BeautifulSoup
import urllib.request as url


def parse(urlToParse):
    try:
        html_page = url.urlopen(urlToParse)
    except HTTPError as e:
        print("Not a valid url", e.code)
    except URLError as e:
        print("Not a valid url", e.code)
    return html_page


def make_soup(html_page):
    soup = BeautifulSoup(html_page, "html.parser")
    return soup


def get_links(soup):
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links


# print(get_links(make_soup(parse('http://www.sport24.gr/'))))

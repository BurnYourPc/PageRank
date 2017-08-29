from src.parse import htmlParser
from src.uniq_purifier import *
from src.purifier import purifier as pu
from collections import Counter


def findSites(urlList):
    outlinks = []
    # outlinks1 = []
    for url in urlList:
        chu, outlinks1 = pu.find_outlinks2(url, False, "String", 1)
        for outlink in outlinks1:
            outlinks.append(outlink)
    return outlinks


def countOutlinks(oulinkList):
    sites = findSites(oulinkList)
    print(sites)
    link_dict = dict((x, sites.count(x)) for x in set(sites))
    # link_dict = Counter(sites)
    return link_dict
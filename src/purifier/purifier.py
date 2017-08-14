from src.parse import htmlParser as parse
from src.altparse import alt_htmlparser as altparse
from urllib.parse import urlsplit, urlunsplit


def split_links(link, parser):
    outlinks=[]
    inlinks=[]
    if parser==1:
        html_page = parse.parse(link)
        soup = parse.make_soup(html_page=html_page)
        links = parse.get_links(soup)
    else:
        links=altparse.get_links(link)
    
    check = "{0.netloc}".format(urlsplit(link))
    #print(check)
    #print(check.count("."))
    if (check.count(".")==2):
        www, link2check, dom = check.split(".")
    else:
        #print("hello")
        link2check, dom = check.split(".")
    for index in links:
        index=str(index)
        if ( (link2check in index) and (index[0:4]=='http') ):
            inlinks.append(index)
        else:
            outlinks.append(index)
    outlinks=clean_links(outlinks,link)
    return inlinks, outlinks


def clean_links(outlinks, linkToCheck):
    clear_outlinks = []
    for link in outlinks:
        splited = urlsplit(link)
        base = "{0.scheme}://{0.netloc}/".format(splited)
        check = "{0.netloc}".format(urlsplit(linkToCheck))
        if (check.count(".")==2):
            www, link, dom = check.split(".")
        else:
            link, dom = check.split(".")
        checkIt = link + "." + dom
        if base[:4] == 'http' and checkIt not in base:
            clear_outlinks.append(base)
    return clear_outlinks


def find_outlinks(link, n):
    inlinks = link
    inlinks2 = []
    # outlink = []
    inlinks, outlinks = split_links(link,2)
    # print(len(inlinks))
    #print(outlinks)
    if n == 2:
        return outlinks
    for i in inlinks:
        # find_outlinks()
        ch, outlink = find_outlinks(i, n+1)
        for j in outlink:
            #if j not in outlinks:
            # inlinks.append(j)
            outlinks.append(j)
    return outlinks



#print(find_outlinks('http://www.sport24.gr/', len('http://www.sport24.gr/'), 1))
#link='http://www.sport24.gr/'
#print(clean_links(split_links('http://www.sport24.gr/', len('http://www.sport24.gr/'))[1],link))
#inlinks=split_links('http://www.sport24.gr/')[0]
#print(inlinks)
#in1=split_links('http://www.sport24.gr/',2)[1]
#print(in1)
#print(" ")
#print(out1)
#in2, out2= find_outlinks('http://www.sport24.gr/',1)
#print(in2)
#print(" ")
#print(out2)
#print(split_links('http://www.sport24.gr/')[0])
#splited = urlsplit(link)
#print(splited)
#base = "{0.scheme}://{0.netloc}/".format(splited)
#print(base)
#check = "{0.netloc}".format(urlsplit(link))
#print(check)
#www, link, dom = check.split(".")
#print(www,link,dom)

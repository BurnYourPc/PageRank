from src.parse import htmlParser as parse
from src.altparse import alt_htmlparser as altparse
from urllib.parse import urlsplit, urlunsplit


def split_links(link, basetocheck, parser):   #take your url, its base and the chosen parser and find all inlinks and outlinks
    inlinks = []
    outlinks = []
    link=str(link)
    print(link)
    if ( " " in link ):      #otherwise is not parsable    |||keep this -->("–")
       return inlinks, outlinks
    if ( is_ascii(link) ):              #otherwise is not parsable
        return inlinks, outlinks
    
    if (parser==1):
        t, html_page = parse.parse(link)
        if (not t):       #checks if the url is parsable
            return inlinks, outlinks
        soup = parse.make_soup(html_page=html_page)
        links = parse.get_links(soup)     #take inlinks and outlinks together in the same list
    else:
        t, html_page=altparse.parse(link)
        if (not t):     #checks if the url is parsable
            return inlinks, outlinks
        links=altparse.get_links(html_page)
        
    
    for index in links:
        index=str(index)
        if ( (basetocheck in index) and (index[0:4]=='http') ):     #check if it is inlink
            inlinks.append(index)
        elif(index[0:4]=='http'):     #check if it is outlink
            splited = urlsplit(index)
            base = "{0.scheme}://{0.netloc}/".format(splited)       #clean the link
            outlinks.append(base)
        
    outlinks=set(outlinks)       #from list change it to set in order to keep uniqe urls
    outlinks=list(outlinks)     #make it list again (unique urls too)
    print(outlinks)
    inlinks=set(inlinks)     #from list change it to set in order to keep uniqe urls
    inlinks=list(inlinks)     #make it list again (unique urls too)
    return inlinks, outlinks


def clean_links(outlinks, linkToCheck):   #merged in split_link
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


def find_outlinks(link, checkin, basetocheck, n):
    inlinks = link
    inlinks2 = []
    
    if (n==1):
        basetocheck=getBaseToCheck(link)      #take the base of your url
        
    inlinks, outlinks = split_links(link, basetocheck, 2)
    if n==1:
        print(len(inlinks))
        
    if (n==1):      #check is only for the initial url and not its inlinks
        if (len(inlinks)==0):         #check if there are no inlinks
            checkin=False
        else:
            checkin=True
    if n == 2:   #only in the second recursive call (if you want to go deaper in inlinks increase the limit
        return checkin, outlinks      #return the outlinks of the inlinks
    count=0
    for i in inlinks:
        count=count+1
        print(count)
        ch, outlink = find_outlinks(i, checkin, basetocheck, n+1)
        for j in outlink:
            if j not in outlinks:    #check if this inlink's outlink belongs to the initial url outlink list
                outlinks.append(j)        #add to the outlink list the outlink from an inlink
    return checkin, outlinks      #this return statement occurs only if n==1 (initial url)


def getBaseToCheck(link):   #find base urls (for example: 'http://www.rt.com/ base is 'rt'
    check = "{0.netloc}".format(urlsplit(link))

    if (check.count(".")==2):
        www, link2check, dom = check.split(".")
    elif (check.count(".")==1):
        link2check, dom = check.split(".")
    elif (check.count(".")==3):
        www, link2check, blog, dom = check.split(".")   #http://www.yourblog.blogspot.com/ base is 'yourblog'
    else:
        www, link2check, blog, bla, dom = check.split(".")
    return link2check




def is_ascii(s):   # check if url have encoded a unicode string in ascii to be produced (non english characters for example or "–" (not "-") character)
    isascii = len(s) != len(s.encode())
    return isascii


#d="http://.www.sport –24.gr/"

#print(is_ascii(d))



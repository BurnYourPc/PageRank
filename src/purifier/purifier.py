from src.parse import htmlParser as parse


def split_links(link, n):
    inlinks = []
    outlinks = []
    html_page = parse.parse(link)
    soup = parse.make_soup(html_page=html_page)
    links = parse.get_links(soup)
    for index in links:
        if type(index) == type('str'):
            if index[0:n] == link[0:n]:
                inlinks.append(index)
            else:
                outlinks.append(index)
    return inlinks, outlinks


def find_outlinks(link, length, n):
    inlinks = link
    inlinks2 = []
    # outlink = []
    inlinks, outlinks = split_links(link, length)
    # print(len(inlinks))
    print(outlinks)
    if n == 3:
        return inlinks, outlinks
    for i in inlinks:
        # find_outlinks()
        inlinks2, outlink = find_outlinks(i,length, n+1)
        for j in outlink:
            if j not in outlinks:
                # inlinks.append(j)
                outlinks.append(j)
    return inlinks2, outlinks



print(find_outlinks('http://www.sport24.gr/', len('http://www.sport24.gr/'), 1))

from src.parse import htmlParser as parse
from src.purifier import purifier as pure
from src.uniq_purifier import unqpurifier as unqpure
from src.createPdf import pdfcreator as PdfC
import os
import numpy as np
from numpy import linalg as LA
from copy import deepcopy
from tkinter import *
import tkinter.messagebox


def sitesGui(numSites):
    mw = Tk()
    mw.title("Pagerank Implementation")       #window's title
    rows = []
    for i in range(numSites):
        cols = []
        for j in range(1):
            e = Entry(relief=RIDGE,bd=5)
            e.grid(row=i+1, column=j+1, sticky=NSEW) #create window's widgets
            e.insert(END, '%s' % 'http://www.')
            cols.append(e)
        rows.append(cols)
    
    def getSites():
        urls=[]
        n=0
        for row in rows:
            for col in row:
                urls.append(col.get())  #get widgets' input as string
                n=n+1
        print(urls)
        mw.destroy()  #destroy window
        A=np.zeros((n,n), dtype=float)  #create A-matrix as a zero matrix
        urls2=urls
        col=0
        for link in urls:
            basetocheck=unqpure.getBaseToCheck(link)    #find base urls (for example: 'http://www.rt.com/ base is 'rt'
            checkin, outlinks=unqpure.find_outlinks(link, False, basetocheck, 1)     #find all outlinks with first parser ((link, False, basetocheck, 2) for second parser
            print(outlinks)
            if (checkin):    #if there is at least one inlink
                A[col,col]=1
            counter=0
            for otherLink in urls2:   #check which urls belong to link's outlink list
                if otherLink!=link:
                    counter=counter+1
                    if otherLink in outlinks:
                        A[counter,col]=1         #if this url belong to link's outlink mark 1 in the corresponding collumn and row
            col=col+1
        print(A)
        A=getAready(A,n)     #we make our matrix collumn stohastic by dividing every collumn's elements with the total number of non-zero elemnts in that collumn
        print(A)
        A=removeSpiderTraps(A,n)     #We gurantee that our graph is connected
        ranking=getRank(A,n)     #get the sites' ranking
        path=os.path.dirname(os.path.abspath("."))   #that's the path to .../PageRankImplementation/src
        print("The ranking of the sites' is:")
        print(ranking)
        source=path+'/main'    #that's the path to .../PageRankImplementation/src/main
        destination=path[0:len(path)-3]+'getRanking'   #that's the path to .../PageRankImplementation/getRanking
        PdfC.CreateRankPdf(ranking,urls,source,destination)    #call function to create pdf with your sites' ranking
        
    
        
    
    Button(text='give Sites', command=getSites).grid()
    mainloop()
    
    
def getAready(A,n):
    for j in range(n):
        nz=np.count_nonzero(A[:,j])
        for i in range(n):
            if (A[i,j]!=0):
                A[i,j]=A[i,j]/nz
    return A


def removeSpiderTraps(A,n):
    A=0.8*A
    A2=np.zeros((n,n), dtype=float)
    A2=(1/n)+A2
    A2=0.2*A2
    A=A+A2
    return A


def getRank(A,n):
    r=np.zeros((n,1), dtype=float)
    for i in range(n):
        r[i]=1/n
    rnew=np.dot(A,r)
    while (LA.norm(rnew-r,2)>0.000001):
        r=rnew
        rnew=np.dot(A,rnew)
    return rnew


def rankUrls(urls,n):     #we do the same as in siteGui function
    A=np.zeros((n,n), dtype=float)
    urls2=urls
    col=0
    for link in urls:
        basetocheck=unqpure.getBaseToCheck(link)
        checkin, outlinks=unqpure.find_outlinks(link, False, basetocheck, 1)
        print(outlinks)
        if (checkin):
            A[col,col]=1
        counter=0
        for otherLink in urls2:
            if otherLink!=link:
                counter=counter+1
                if otherLink in outlinks:
                    A[counter,col]=1
        col=col+1
    print(A)
    A=getAready(A,n)
    print(A)
    A=removeSpiderTraps(A,n)
    r=getRank(A,n)
    print("The ranking of the sites' is:")
    print(r)
    return r


#---------------------------------------------------------------------------#

print("Welcome to BurnYourPc project of PageRank implementation..!")
print(" ")
answer=input("Sites in txt[1] or input-window[2]\n")
answer=int(answer)
path=os.path.dirname(os.path.abspath("."))   #that's the path to .../PageRankImplementation/src
print(path)
if (answer==1):
    input("Edit the 'sites.txt' in getRanking folder and press enter\n")
    path2txt=path[0:len(path)-3]+'getRanking/sites.txt'   #the path to the sites' txt
    myfile = open(path2txt, 'r') 
    urls=[]
    counter=0
    for line in myfile: 
        counter=counter+1
        site=line
        site=site[0:(len(site)-1)]
        urls.append(site)             #append sites from txt in url list
    print(urls)
    ranking= rankUrls(urls,counter)     #call function to compute the sites' ranking
    print(ranking)
    source=path+'/main'      #that's the path to .../PageRankImplementation/src/main
    destination=path[0:len(path)-3]+'getRanking'     #that's the path to .../PageRankImplementation/getRanking
    PdfC.CreateRankPdf(ranking,urls,source,destination)    #call function to create pdf with your sites' ranking
elif (answer==2):
    num=input("How many sites do you want to rank?\n")    #give number of sites you want to rank
    num=int(num)
    sitesGui(num)      #create a window for input urls
else:
    print(" ")
    print("Wrong inputs! Try again..")



from src.parse import htmlParser as parse
from src.purifier import purifier as pure
from src.uniq_purifier import unqpurifier as unqpure
import numpy as np
from copy import deepcopy
from tkinter import *
import tkinter.messagebox


def sitesGui(numSites):
    mw = Tk()
    mw.title("Pagerank Implementation")
    rows = []
    for i in range(numSites):
        cols = []
        for j in range(1):
            e = Entry(relief=RIDGE,bd=5)
            e.grid(row=i+1, column=j+1, sticky=NSEW)
            e.insert(END, '%s' % 'http://www.')
            cols.append(e)
        rows.append(cols)
    
    def getSites():
        urls=[]
        n=0
        for row in rows:
            for col in row:
                urls.append(col.get())
                n=n+1
            #i=i+1
        print(urls)
        mw.destroy()
        A=np.zeros((n,n), dtype=int)
        #print(A)
        urls2=urls
        col=0
        for link in urls:
            checkin, outlinks=unqpure.find_outlinks(link, False, 1)
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
    
        
    
    Button(text='give Sites', command=getSites).grid()
    mainloop()
    
    
def getAready(A,n):
    for j in range(n):
        nz=np.count_nonzero(A[:,j])
        for i in range(n):
            if (A[i,j]!=0):
                A[i,j]=A[i,j]/nz
    
    return A


sitesGui(3)

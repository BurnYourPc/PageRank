import os
import numpy as np
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import shutil


def CreateRankPdf(ranking,urls,source,destination):        #takes the ranking vector, the urls, the main's file path and the destination for your pdf and creates a pdf with your ranking results
    
    urls2pdf=[]
    rank2pdf=[]
    allurls=len(urls)
    counter=0
    count_pages=0
    rsort=getSort(ranking,allurls)    #take sorting positions in order to write the rankings in deacrising order
    print(rsort)
    for i in range(allurls):
        rank2pdf.append(ranking[rsort[allurls-i-1]])
        urls2pdf.append(urls[rsort[allurls-i-1]])
        counter=counter+1
        if (counter%60==0 or counter==allurls):    #check if we add 60 urls or we add the last url. 60 is the limit for a pdf page to be created
            count_pages=count_pages+1       #add one page
            BurnRanksOnPdf(rank2pdf,urls2pdf,count_pages)     #create a new page for our pdf
            rank2pdf=[]        #empty vectors for the new pdf page
            urls2pdf=[]
    
    output = PdfFileWriter()
    for i in range(count_pages):     #merge all pdf pages that have been created
        append_pdf(PdfFileReader(open("output"+str(i+1)+".pdf","rb")),output)
    
    file_list = os.listdir(destination)
    file_count = len(file_list)+1
    name="RankSites"+str(file_count-1)+".pdf"     #name our final, merged pdf file
    output.write(open(name,"wb"))
    
    for i in range(count_pages):
        os.remove(os.path.join(source, "output"+str(i+1)+".pdf"))      #remove all pdfs that are merged (they are uselless now)
    
    shutil.move(source+"/"+name, destination)       #cut and paste our final pdf file to the diserable folder


def BurnRanksOnPdf(ranking,urls,numpage):    #take ranking, urls and the corresponding page of the pdf file and create that page
 
    pdf = PdfFileWriter()

    # create canvas to edit pdf
    imgTemp = BytesIO()
    imgDoc = canvas.Canvas(imgTemp, pagesize=A4)
    
    # set the initial position for the first url with its ranking to be writed
    x=45
    if (numpage==1):    #check if it is the first page of our pdf
        yarx=730
    else:
        yarx=750    #if it isn't write the first pdf closest to the top of the page
    
    # set fonts
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    #pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
    
    y=yarx
    counter=1
    allurls=len(urls)
    for site in urls:
        if (counter==31):     #if we write 30 urls we have to change collumn in the page
            x=x+280
            y=yarx
        imgDoc.setFont('Vera', 13)
        if (counter+(numpage-1)*60<10):
            gapenum=15
        elif(counter+(numpage-1)*60<100):
            gapenum=20
        else:
            gapenum=27
        imgDoc.drawString(x-gapenum,y,str(counter+(numpage-1)*60)+".")  #write the position of the url (for example "1. bestsite.com [rank]"
        imgDoc.setFont('VeraBd', 13)
        imgDoc.drawString(x,y,site[11:(len(site)-1)]) #write site name without "http:www."
        imgDoc.setFont('Vera', 13)
        rnk=ranking[counter-1]
        rnk[0]=100*rnk[0]
        imgDoc.drawString(x+190,y,str(np.round(rnk[0],decimals=2)))     #write rank with two decimals digits
        counter=counter+1
        print(counter)
        y=y-20    #go down for the next site position to be writen
    
    
    imgDoc.setFont('Vera', 13)
    imgDoc.drawString(30,820,"BurnYourPc Organization/")
    imgDoc.setFont('VeraBd', 9)
    imgDoc.drawString(40,818,"_____________________________________________________________________________")
    imgDoc.drawString(197,820,"PageRankImplementation")
    if (numpage==1):
        imgDoc.setFont('Vera', 16)
        imgDoc.drawString(230,780,"Web sites Ranking")
    imgDoc.setFont('VeraIt', 8)
    imgDoc.drawString(430,20,"By PantelisPanka, nikfot, TolisChal")
    imgDoc.setFont('Vera', 8)
    imgDoc.drawString(550,820,str(numpage))
    
    imgDoc.save()
    
    # Use PyPDF to merge the image-PDF into the template
    pdf.addPage(PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0))

    pdf.write(open("output"+ str(numpage)+".pdf","wb"))      #save this page pdf to the source (see previous function) path


def append_pdf(input,output):        #function to merge pdf pages
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]


def getSort(r,n):
    rsort=np.array([])
    for i in range(n):
        rsort=np.append(rsort,r[i])
    return np.argsort(rsort)



import os
import numpy as np
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import shutil


def CreateSudoPdf(ranking,urls,source,destination):

    urls2pdf=[]
    rank2pdf=[]
    allurls=len(urls)
    counter=0
    count_pages=0
    rsort=getSort(ranking,allurls)
    print(rsort)
    for i in range(allurls):
        rank2pdf.append(ranking[rsort[allurls-i-1]])
        urls2pdf.append(urls[rsort[allurls-i-1]])
        counter=counter+1
        if (counter%60==0 or counter==allurls):
            count_pages=count_pages+1
            BurnRanksOnPdf(rank2pdf,urls2pdf,count_pages)
            rank2pdf=[]
            urls2pdf=[]
    
    output = PdfFileWriter()
    for i in range(count_pages):
        append_pdf(PdfFileReader(open("output"+str(i+1)+".pdf","rb")),output)
    
    file_list = os.listdir(destination)
    file_count = len(file_list)+1
    name="RankSites"+str(file_count-1)+".pdf"
    output.write(open(name,"wb"))
    
    for i in range(count_pages):
        os.remove(os.path.join(source, "output"+str(i+1)+".pdf"))
    
    shutil.move(source+"/"+name, destination)


def BurnRanksOnPdf(ranking,urls,numpage):
 
    pdf = PdfFileWriter()

    # Using ReportLab Canvas to insert image into PDF
    imgTemp = BytesIO()
    imgDoc = canvas.Canvas(imgTemp, pagesize=A4)
    
    # Draw image on Canvas and save PDF in buffer
    x=45
    if (numpage==1):
        yarx=730
    else:
        yarx=750
    
    #pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    #pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
    
    y=yarx
    counter=1
    allurls=len(urls)
    for site in urls:
        if (counter==31):
            x=x+280
            y=yarx
        imgDoc.setFont('Vera', 13)
        if (counter+(numpage-1)*60<10):
            gapenum=15
        elif(counter+(numpage-1)*60<100):
            gapenum=20
        else:
            gapenum=27
        imgDoc.drawString(x-gapenum,y,str(counter+(numpage-1)*60)+".")
        imgDoc.setFont('VeraBd', 13)
        imgDoc.drawString(x,y,site[11:(len(site)-1)])
        imgDoc.setFont('Vera', 13)
        rnk=ranking[counter-1]
        rnk[0]=100*rnk[0]
        imgDoc.drawString(x+190,y,str(np.round(rnk[0],decimals=2)))
        counter=counter+1
        print(counter)
        y=y-20
    
    
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

    pdf.write(open("output"+ str(numpage)+".pdf","wb"))


def append_pdf(input,output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]


def getSort(r,n):
    rsort=np.array([])
    for i in range(n):
        rsort=np.append(rsort,r[i])
    return np.argsort(rsort)



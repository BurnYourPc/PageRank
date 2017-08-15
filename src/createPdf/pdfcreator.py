import os
import numpy as np
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import shutil


#def CreateSudoPdf(ranking,urls,source,destination):

    
    
   # for i in range(5):
   #     pathTemp=pathConst+getStrPathDiff(i+1)
   #     file_list = os.listdir(pathTemp)
   #     file_count = len(file_list)
   #     allmax.append(file_count)
    
    
    #counter=0

    #for i in range(num):
        
    #    diff=getNumDiff(i,nums)
    #    diffpath=getStrPathDiff(diff)
    #    path=pathConst+diffpath
    #    file_list = os.listdir(path)
    #    file_count = len(file_list)
        
        
        
     
     #   if ((counter)%6==1):
     #       count_pages=count_pages+1
     #   
     #   if (pick<10):
     #       prob=probConst+str(0)+str(pick)+".png"
     #   else:
     #       prob=probConst+str(pick)+".png"
     #   path=path+prob
     #   patharray.append(path)
     #   if (len(patharray)==6 or i==num-1):
     #       BurnSudoOnPdf(patharray,count_pages,diffarray)
     #       patharray=[]
     #       diffarray=[]
      
    #output = PdfFileWriter()
    #for i in range(count_pages):
    #    append_pdf(PdfFileReader(open("output"+str(i+1)+".pdf","rb")),output)
    
    #file_list = os.listdir(destination)
    #file_count = len(file_list)+1
    #name="RankSites"+str(file_count)+".pdf"
    #output.write(open(name,"wb"))
    
    #for i in range(count_pages):
    #    os.remove(os.path.join(source, "output"+str(i+1)+".pdf"))
    
    #shutil.move(source+"/"+name, destination)


def BurnSudoOnPdf(ranking,urls,numpage,numcol):
 
    pdf = PdfFileWriter()

    # Using ReportLab Canvas to insert image into PDF
    imgTemp = BytesIO()
    imgDoc = canvas.Canvas(imgTemp, pagesize=A4)
    
    # Draw image on Canvas and save PDF in buffer
    
    if (numcol==1):
        x=55
    else:
        x=345
    y=750
    
    #pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    #pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
    
    counter=0
    for site in urls:
        imgDoc.setFont('VeraBd', 13)
        imgDoc.drawString(x,y,site)
        imgDoc.setFont('Vera', 13)
        imgDoc.drawString(x+100,y,str(ranking[counter]))
        counter=counter+1
        print(counter)
        y=y-20
    
    
    imgDoc.setFont('Vera', 13)
    imgDoc.drawString(30,820,"BurnYourPc Organization/")
    imgDoc.setFont('VeraBd', 9)
    imgDoc.drawString(197,820,"PageRankImplementation")
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


r=np.array([1.2,3.4,0.2345,1.345,6.98,456.123,1.234,0.45])
d=['hello','hello','hello','hello','hello','hello','hello','hello']
BurnSudoOnPdf(r,d,1,1)

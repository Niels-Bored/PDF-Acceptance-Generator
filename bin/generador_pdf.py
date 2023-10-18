import os
import io
import xlrd
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

current_folder = os.path.dirname (__file__)
parent_folder = os.path.dirname (current_folder)
files_folder = os.path.join (parent_folder, "files")
data = os.path.join (files_folder, f"Data.xlsx")
original_pdf = os.path.join (current_folder, f"aceptacion.pdf")

def generatePDF(no_solicitud, name, dni, motivo, fecha_solicitud, email, poblacion, ciudad, cp, telefono, situacion, prerrequisito, basica, automatizacion, redes, riesgo, quirofano, lampara, generadora, observaciones, aceptado, requisitoSI, requisitoNO, iebt, iite):
    packet = io.BytesIO()
    # Fonts with epecific path
    pdfmetrics.registerFont(TTFont('times','times.ttf'))
    pdfmetrics.registerFont(TTFont('timesbd', 'timesbd.ttf'))
    pdfmetrics.registerFont(TTFont('arial', 'arial.ttf'))

    c = canvas.Canvas(packet, letter)

    #Página 1

    c.setFont('arial', 10)
    c.drawString(100, 733, str(int(no_solicitud)))
    c.drawString(330, 733, fecha_solicitud)
    c.drawString(510, 733, aceptado)
    c.drawString(150, 715, name)
    c.drawString(520, 715, dni)

    c.setFont('timesbd', 12)

    if(motivo=="inicial"):
        c.drawString(151, 645, "X")
    if(motivo=="renovacion"):
        c.drawString(325, 645, "X")

    if(basica):
        c.drawString(530, 517, "X")
    if(automatizacion):
        c.drawString(530, 492, "X")
    if(redes):
        c.drawString(530, 467, "X")
    if(riesgo):
        c.drawString(530, 442, "X")
    if(quirofano):
        c.drawString(530, 417, "X")
    if(lampara):
        c.drawString(530, 392, "X")
    if(generadora):
        c.drawString(530, 367, "X")
    
    if(requisitoSI=="x"):
        c.drawString(23, 338, "X")
    if(requisitoNO=="x"):
        c.drawString(23, 277, "X")

    if(iebt):
        c.drawString(23, 608, "X")
    if(iite):
        c.drawString(23, 332, "X")
    if(aceptado=="SI"):
        c.drawString(23, 298, "X")

    c.showPage()
    c.save()

    packet.seek(0)

    new_pdf = PdfFileReader(packet)
    
    existing_pdf = PdfFileReader(open(original_pdf, "rb"))
    output = PdfFileWriter()
    
    #Creación página
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    new_pdf = os.path.join (files_folder, f"Aceptación de Solicitud_{int(no_solicitud)}.pdf")
    output_stream = open(new_pdf, "wb")
    output.write(output_stream)
    output_stream.close()


  
wb = xlrd.open_workbook(data) 

hoja = wb.sheet_by_index(0) 
for i in range (2, hoja.nrows):
    print(hoja.cell_value(i, 0))
    print(hoja.cell_value(i, 1))
    print(hoja.cell_value(i, 9))
    print(hoja.cell_value(i, 10))
    print(hoja.cell_value(i, 11))
    print(hoja.cell_value(i, 12))
    print(hoja.cell_value(i, 13))
    print(hoja.cell_value(i, 14))
    print(hoja.cell_value(i, 15))
    print(hoja.cell_value(i, 16))
    print(hoja.cell_value(i, 24))
    print(hoja.cell_value(i, 25)) 
    print(hoja.cell_value(i, 26)) 

    fecha_segementada=hoja.cell_value(i, 1).split(" del ")
    fecha_solicitud=fecha_segementada[0]+"/"+fecha_segementada[1]+"/"+fecha_segementada[2]
    print(fecha_solicitud)
    no_solicitud=hoja.cell_value(i, 0)
    name=hoja.cell_value(i, 9)
    dni=hoja.cell_value(i, 10)
    email=hoja.cell_value(i, 11)
    poblacion=hoja.cell_value(i, 13)
    ciudad=hoja.cell_value(i, 14)
    cp=hoja.cell_value(i, 15)
    telefono=hoja.cell_value(i, 16)
    observaciones=hoja.cell_value(i, 24)
    aceptado=hoja.cell_value(i, 27)
    requisitoSI=hoja.cell_value(i, 26)
    requisitoNO=hoja.cell_value(i, 27)

    if(hoja.cell_value(i, 2)=="SI"):
        print("Inicial")
        motivo="inicial"
    if(hoja.cell_value(i, 3)=="SI"):
        print("Renovacion")
        motivo="renovacion"
    if(hoja.cell_value(i, 4)=="SI"):
        print("Experiencia")
        prerrequisito="experiencia"
    if(hoja.cell_value(i, 5)=="SI"):
        print("Formacion")         
        prerrequisito="formacion"
    if(hoja.cell_value(i, 6)=="SI"):
        print("Autonomo")
        situacion="autonomo"
    if(hoja.cell_value(i, 7)=="SI"):
        print("Ajena")
        situacion="ajena"
    if(hoja.cell_value(i, 8)=="SI"):
        print("No trabaja")         
        situacion="no trabaja" 
    if(hoja.cell_value(i, 17)=="X"):
        print("IEBT")
        iebt=True
    else:
        print("No IEBT")
        iebt=False 
    if(hoja.cell_value(i, 25)=="X"):
        print("IITE")
        iite=True
    else:
        print("No IITE")
        iite=False  
    if(hoja.cell_value(i, 18)=="SI"):
        print("Basica")
        basica=True
    else:
        print("No Basica")
        basica=False    
    if(hoja.cell_value(i, 19)=="SI"):
        print("Automatizacion")
        automatizacion=True
    else:
        print("No Automatizacion")
        automatizacion=False 
    if(hoja.cell_value(i, 20)=="SI"):
        print("Redes")
        redes=True
    else:
        print("No Redes")
        redes=False 
    if(hoja.cell_value(i, 21)=="SI"):
        print("Riesgo")
        riesgo=True
    else:
        print("No Riesgo")
        riesgo=False 
    if(hoja.cell_value(i, 22)=="SI"):
        print("Quirofano")
        quirofano=True
    else:
        print("No Quirofano")
        quirofano=False
    if(hoja.cell_value(i, 23)=="SI"):
        print("Generadora")
        generadora=True
    else:
        print("No Generadora")
        generadora=False   
    if(hoja.cell_value(i, 24)=="SI"):
        print("Lampara")
        lampara=True
    else:
        print("No Lampara")
        lampara=False   
    print("_______________________________")
    generatePDF(no_solicitud, name, dni, motivo, fecha_solicitud, email, poblacion, ciudad, cp, telefono, situacion, prerrequisito, basica, automatizacion, redes, riesgo, quirofano, lampara, generadora, observaciones, aceptado, requisitoSI, requisitoNO, iebt, iite)
print("Documentos generados correctamente")    
input()
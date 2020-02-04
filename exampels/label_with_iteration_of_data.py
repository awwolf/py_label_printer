#compatibility github-pycharm
import sys; sys.path.append("..")
#import library
from src.label_lib2 import LabelPage
#from reportlab.lib.units import mm
#import for barcodes
from reportlab.graphics.barcode import code39, qr, code93, code128
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
#import else
from datetime import datetime
mm = 1
L = LabelPage(size=(70,50), cnt=(2,4), space=(20 ,20), filename=__file__[:-2]+"pdf", rotate=True)
L.setFrame(0.2, round=8)
L.setMarksOuter(1, spacing=10)
L.setMarksInner(0.5, spacing=5)
c = L.get_canvas_object()

# Generate some data
data = []
for i in range(32):
    data.append([{"color": "red", "rgb":(255, 0, 0), "id":i}, {"color": "green", "rgb":(0, 255, 0), "id":i}, {"color": "blue", "rgb":(0, 0, 255), "id":i}][i % 3])

c.setFont("Helvetica-Bold", size=3)
c.drawString(20,20, "inner marks")
c.drawString(20,14, "outer marks")
c.setFont("Helvetica-Bold", size=6)
c.setFillColorRGB(1,0,0)
c.drawCentredString(L.pagesize[0]/2,200, "This is only on the first page! Iteration DEMO with Data and Barcodes")

#iterate with function 'iter_label' through the data

for i in L.iter_label(data):
# draw text
    if L.new_page:
        c.setFillColorRGB(1,0,0)
        c.setFont("Helvetica-Bold", size=6)
        c.drawString(-10,L.LeftBottom[1]*-1+6, "This text is on every page. Attention, this position is relativ to the first label." + " "*27 + "Page " + str(int(i["id"]/8+1)))
    c.setFillColorRGB(*i["rgb"])
    c.setFont("Helvetica-Bold", size=8)
    c.drawCentredString(L.sizeX / 2 , 27, i["color"])
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Courier", size=7)
    c.drawCentredString(L.sizeX/2, 7, "ID: " + str(i["id"]))
# draw barcodes
    #bc = code39.Extended39("ID%.6i" % i["id"], barWidth=0.30, barHeight=10)
    #bc = code128.Code128("ID%.6i" % i["id"], barWidth=0.45, barHeight=10
    bc = code93.Standard93("ID%.6i" % i["id"], barWidth=0.33, barHeight=8)
    bc.drawOn(c, -10, 14 )
# draw QR-code
    qr_code = qr.QrCodeWidget("WEB:www.example.com\nACCESS:%s\nID%.6i\nTS:%s" % (i["color"],i["id"],datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
    bounds = qr_code.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    dr = Drawing(0, 0, transform=[25. / width, 0, 0, 25. / height, 0, 0])
    dr.add(qr_code)
    renderPDF.draw(dr, c, L.sizeX/2-12, 35*mm)
# draw hole
    c.circle(7, L.sizeY-7, 2.5)
# draw image
    c.drawImage("star.jpg",5.0*mm,27.0*mm,width=6*mm,height=6*mm, preserveAspectRatio=True, anchor='c')

L.save()
L.show()




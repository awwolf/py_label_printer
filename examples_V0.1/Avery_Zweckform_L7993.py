#awwolf 11.10.2019 V1.0
import sys; sys.path.append("..") #compatibility github-pycharm
from src.label_lib import LabelPage

L = LabelPage(size=(99.1,67.7), cnt=(2,4), space=(2.5 , 0), LeftBottom=[None, None], frame=1, filename=__file__[:-2]+"pdf", rotate=True)
#L = LabelPage(size=(67.7, 99.1), cnt=(4,2), space=(0, 2.5), LeftBottom=[None, None], frame=1, filename=__file__[:-2]+"pdf", rotate=False)
c = L.get_canvas_object()


L.setFillColorRGB(0, 0, 255, 1)
L.drawRect(5,78,56.9,10.9, fill=True)

L.setFillColorRGB(255, 255, 255, 1)
c.setFont("Helvetica-Bold", size=25)
L.drawString(12, 80, "AIR INLET")

L.setFillColorRGB(0, 0, 0, 1)
c.setFont("Helvetica-Bold", size=14)
L.drawString(11, 68, "6-9 Bar, > 150 L/Min")

L.drawString(15, 59, "ISO 8573-1:2010")
L.drawString(26, 53, "[1:3:1]")

L.drawCircle(x=33.85, y=25.85,radius=9)

L.save()
L.run()




#awwolf 11.10.2019 V1.0
import sys; sys.path.append("..") #compatibility github-pycharm
from src.label_lib2 import LabelPage
from src import templates

L = LabelPage(**templates.Avery_Zweckform_L7993, filename=__file__[:-2]+"pdf", rotate=True)
L.setFrame()
c = L.get_canvas_object()

for i in L.iter_label():
    L.setFillColorRGB(0, 0, 255, 1)
    c.roundRect(5, 78, 56.9, 10.9, radius=5, fill=True)
    L.setFillColorRGB(255, 255, 255, 1)
    c.setFont("Helvetica-Bold", size=8.8)
    c.drawString(12, 80, "AIR INLET")
    L.setFillColorRGB(0, 0, 0, 1)
    c.setFont("Helvetica-Bold", size=4.9)
    c.drawString(11, 68, "6-9 Bar, > 150 L/Min")
    c.drawString(15, 59, "ISO 8573-1:2010")
    c.drawString(26, 53, "[1:3:1]")
    c.circle(33.85, 25.85, 9)

L.save()
L.show()




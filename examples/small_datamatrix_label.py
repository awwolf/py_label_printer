import sys; sys.path.append("..") #compatibility github-pycharm
from src.label_lib2 import LabelPage
from src import templates

L = LabelPage(**templates.Avery_Zweckform_3667, filename=__file__[:-2]+"pdf", rotate=False)
L.setFrame()
c = L.get_canvas_object()

for i in L.iter_label():
    id = "ID%.8i" % i
    L.draw_datamatrix(id, 35, L.sizeY/2, 8)
    c.setFont("Times-BoldItalic", size=3.8)
    c.setFillColorRGB(0,0,0)
    c.drawString(3, 9.3, "Demo Label")

    c.setFont("Courier-Bold", size=4)
    c.setFillColorRGB(0,0,1)
    c.drawString(2.8, 4.3, id)
    c.rotate(90)
    c.setFont("Courier-Bold", size=3.5)
    c.drawString(4, -45, "%.4i" % i)
    c.rotate(-90)

L.save()
L.show()

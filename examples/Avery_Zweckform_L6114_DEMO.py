import sys; sys.path.append("..") #compatibility github-pycharm
from src.label_lib2 import LabelPage
from src import templates

L = LabelPage(**templates.Avery_Zweckform_L6114, filename=__file__[:-2]+"pdf")
L.setFrame()
c = L.get_canvas_object()

# add watermark
str = "Achtung • Attention •"* 32
c.rotate(-10)
c.setFont("Helvetica-BoldOblique", size=4)

space = 0.65
for i in range(80):
    st = str[i%(len(str))*4:]
    c.setFillColorRGB(*[0.8]*3, 1)
    c.drawString(-250+ (i*space),0 + 7*(i*space), st)
c.rotate(10)

# generate text
c.setFillColorRGB(1,0,0,1)

for i in L.iter_label():
    c.setFont("Helvetica-Bold", size=6.4)
    c.drawCentredString(L.sizeX/2,22, "Lieferschein")
    c.setFont("Helvetica-Bold", size=4)
    c.drawCentredString(L.sizeX/2,17, "innenliegend!")
    c.setFont("Helvetica-Bold", size=6.4)
    c.drawCentredString(L.sizeX / 2, 8, "Packing List")
    c.setFont("Helvetica-Bold", size=4)
    c.drawCentredString(L.sizeX / 2, 3, "inside")

L.save()
L.show()




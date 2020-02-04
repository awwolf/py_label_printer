import sys; sys.path.append("..") #compatibility github-pycharm
from src.label_lib2 import LabelPage
from src import templates

L = LabelPage(**templates.Avery_Zweckform_L6114, filename=__file__[:-2]+"pdf")
L.setFrame()
c = L.get_canvas_object()

# add watermark
str = "DEMO • "* 32
c.rotate(-30)
c.setFont("Helvetica-BoldOblique", size=5)

diff = 0.7
for i in range(80):
    c.setFillColorRGB(220 / 255, 220 / 255, 150 / 255, 1)
    c.drawString((-250+diff)+ i, (0-diff) + 7*i, str)
    c.setFillColorRGB(180/255, 200/255, 255/255,1)
    c.drawString(-250+ i,0 + 7*i, str)
c.rotate(30)

# generate text
c.setFillColorRGB(1,0,0,1)

#c.setFont("Helvetica-Bold", size=6.4)
#c.drawString(10,20,"DEMO DEVICE")
for i in L.iter_label():
    c.setFont("Helvetica-Bold", size=6.4)
    c.drawString(10,20,"DEMO DEVICE")
    c.setFont("Helvetica-Bold", size=3.6)
    c.drawString(5,10," Garantieverlust beim Entfernen")
    c.drawString(5,5,"     Warranty Void if Removed")

L.save()
L.show()




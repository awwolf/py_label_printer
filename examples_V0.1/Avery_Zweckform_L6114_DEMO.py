import sys; sys.path.append("..") #compatibility github-pycharm
from src.label_lib import LabelPage
from reportlab.lib.units import mm,cm,inch

L = LabelPage(size=(63.5,29.6), cnt=(3,9), space=(2.5,0), LeftBottom=[None, None], frame=1, filename=__file__[:-2]+"pdf")
c = L.get_canvas_object()

str = "DEMO • "*32
c.rotate(-30)
L.setFont("Helvetica-BoldOblique", size=10)
L.setFillColorRGB(220,220,150,1)
diff = 0.5
for i in range(80):
    c.drawString((-250+diff)*mm+ i, (0-diff)*mm + 14*i, str)
L.setFillColorRGB(180, 200, 255,1)
for i in range(80):
    c.drawString(-250*mm+ i,0*mm + 14*i, str)

c.rotate(30)
c.setFillColorRGB(255,0,0,1)
c.setFont("Helvetica-Bold", size=18)
L.drawString(10,20,"DEMO DEVICE")
c.setFont("Helvetica-Bold", size=10)
L.drawString(5,10," Garantieverlust beim Entfernen")
L.drawString(5,5,"     Warranty Void if Removed")

L.save()
L.run()




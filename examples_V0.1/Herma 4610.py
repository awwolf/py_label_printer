#compatibility github-pycharm
import sys; sys.path.append("..")
from src.label_lib import LabelPage
from src import templates

L = LabelPage(**templates.Herma_4610, frame=False, filename=__file__[:-2]+"pdf")
c = L.get_canvas_object()

c.setFont("Helvetica-Bold", size=10)
L.drawString(4,22,"Your Company Name")

c.setFont("Helvetica", size=10)

rows= [('Description:', 'Part A'),
       ('P/O:', '123456'),
       ('Quantity:', "5"),
       ('Lot:', None),
       ('Expiry Date:', None)]

start_x = 18
for row in rows:
    L.drawString(4,start_x,row[0])
    if row[1] is None:
        L.drawString(25, start_x, "___________")
    else:
        L.drawString(25, start_x, row[1])
    start_x -= 4

L.save()
L.run()




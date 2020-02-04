import sys; sys.path.append("..")   #compatibility github-pycharm
from src.label_lib2 import LabelPage
from src import templates

L = LabelPage(**templates.Herma_4610, filename=__file__[:-2]+"pdf")
L.setFrame(thickness=0.5)
c = L.get_canvas_object()

#Data
rows= [('Description:', 'Part A'),
       ('P/O:', '123456'),
       ('Quantity:', "5"),
       ('Lot:', None),
       ('Expiry Date:', None)]

for i in L.iter_label():
    c.setFont("Helvetica-Bold", size=4)
    c.drawString(4, 24, "Your Company Name")
    c.setFont("Helvetica", size=3.7)
    start_x = 19
    for row in rows:
        c.drawString(4, start_x, row[0])
        if row[1] is None:
            c.drawString(25, start_x, "___________")
        else:
            c.drawString(25, start_x, row[1])
        start_x -= (4)

L.save()
L.show()




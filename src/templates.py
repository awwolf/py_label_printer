''' Put here your Label Templates

    size  - single label size (X, Y) in Millimeters
    cnt   - number of labels in (X, Y)
    space - spacing between the labels (X, Y) in Millimeters
    LeftBottom - (X, Y) position of the left-bottom corner of the first label from the left-bottom side of the page
                 leave blank if centered
'''

from reportlab.lib.pagesizes import A4

Avery_Zweckform_L6114 = {"size":(63.5,29.6), "cnt":(3,9), "space":(2.5, 0), "pagesize":A4}
Avery_Zweckform_L7993 = {"size":(99.1,67.7), "cnt":(2,4), "space":(2.5, 0), "pagesize":A4}


Herma_4610 = {"size":(52.5,29.7), "cnt":(4,10), "space":(0,0), "pagesize":A4}

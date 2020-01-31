#awwolf 11.10.2019 V1.0
from reportlab.lib.pagesizes import A4,landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm,cm,inch
import subprocess

X, Y = 0, 1
frame_none, frame_label = 0, 1

'''Posible Fonts

Times-Roman           Courier                    Helvetica                 
Times-Bold            Courier-Bold               Helvetica-Bold            
Times-Italic          Courier-Oblique            Helvetica-Oblique         
Times-BoldItalic      Courier-BoldOblique        Helvetica-BoldOblique    '''

class LabelPage:
    def __init__(self, size, cnt, space=(0,0), LeftBottom=[None, None], pagesize=A4, rotate=False, frame=frame_none, filename="Label_Lib.pdf"):
        if rotate: pagesize=landscape(pagesize)
        if LeftBottom is None or LeftBottom is (None, None): LeftBottom = [None, None]

        self.c = canvas.Canvas(filename=filename, pagesize=pagesize)
        #self.c.translate(mm, mm)
        self.size, self.cnt, self.space, self.frame, self.filename = size, cnt, space, frame, filename

        self.pagesize = pagesize[0]/mm, pagesize[1]/mm
        o_size_x = (size[0] * cnt[0]) + ((cnt[0] - 1) * space[0])
        o_size_y = (size[1] * cnt[1]) + ((cnt[1] - 1) * space[1])
        if LeftBottom == [None, None]:
            LeftBottom[X] = (self.pagesize[X] - o_size_x) / 2
            LeftBottom[Y] = (self.pagesize[Y] - o_size_y) / 2
        self.LeftBottom = LeftBottom

        #Äußerer Rahmen
        #self.c.rect(RightBottom[X] * mm, RightBottom[Y] * mm, o_size_x * mm, o_size_y * mm)

        self.positions = []
        self.setLineWidth(0.1)
        for idx_x in range(self.cnt[X]):
            x = self.LeftBottom[X] + (idx_x * (self.size[X] + self.space[X]))
            for idx_y in range(self.cnt[Y]):
                y = self.LeftBottom[Y] + (idx_y * (self.size[Y] + self.space[Y]))
                if self.frame == 1:
                    self.c.rect(x * mm, y * mm, self.size[X] * mm, self.size[Y] * mm)
                self.positions.append([x,y])

    def get_canvas_object(self):
        return self.c
    def drawString(self, x, y, str):
        for idx in self.positions:
            self.c.drawString( (idx[X] + x) * mm, (idx[Y] + y) * mm, str)
    def drawRect(self, x, y , width, height, radius=0, fill=False, positions=None):
        for id, idx in enumerate(self.positions):
            if positions is None or id in positions:
                self.c.roundRect(x=(idx[X] + x) * mm, y=(idx[Y] + y) * mm, width=width*mm, height=height*mm, radius=3,fill=fill)

    def drawCircle(self,x,y, radius, fill=False):
        for idx in self.positions:
            self.c.circle((idx[X] + x) * mm, (idx[Y] + y) * mm, r=radius*mm, fill=fill)

    def drawLine(self, x, y , x2, y2):
        for idx in self.positions:
            self.c.line((idx[X] + x) * mm, (idx[Y] + y) * mm, (idx[X] + x2) * mm, (idx[Y] + y2) * mm)
    def setStrokeColorRGB(self, r, g, b, alpha=None):
        self.c.setStrokeColorRGB(r/255, g/255, b/255, alpha)
    def setFillColorRGB(self, r, g, b, alpha=None):
        self.c.setFillColorRGB(r/255, g/255, b/255, alpha)
    def setLineWidth(self, width):
        self.c.setLineWidth(width)
    def setFont(self, font= "Helvetica", size= 14):
        self.c.setFont(font, size)

    def draw(self):
        self.c.setFont("Helvetica", 14)
        # choose some colors
        self. c.setStrokeColorRGB(0.2, 0.5, 0.3)
        self.c.setFillColorRGB(1, 0, 1)
        self.c.line(0, 0, 0, 1.7 * inch)
        self.c.line(0, 0, 1 * inch, 0)

    def save(self):
        self.c.save()

    def run(self):
        subprocess.Popen(self.filename, shell=True)








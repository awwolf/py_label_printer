#awwolf 11.10.2019 V1.0
from reportlab.lib.pagesizes import A4,landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm,cm,inch

import subprocess

from reportlab.platypus import PageBreak

X, Y, X2, Y2 = 0, 1, 2, 3
frame_none, frame_label = 0, 1

'''Posible Fonts

Times-Roman           Courier                    Helvetica                 
Times-Bold            Courier-Bold               Helvetica-Bold            
Times-Italic          Courier-Oblique            Helvetica-Oblique         
Times-BoldItalic      Courier-BoldOblique        Helvetica-BoldOblique    '''

class LabelPage():
    def __init__(self, size, cnt, space=(0,0), LeftBottom=[None, None], pagesize=A4, rotate=False, frame=frame_none, filename="Label_Lib.pdf"):
        #default parameters
        self.frame_spacing = 0
        self.marks_outer_spacing, self.marks_outer_length, self.marks_outer = -10, 30, 0
        self.marks_inner_spacing, self.marks_inner_length, self.marks_inner = -20, 5, 0

        if rotate:
            pagesize=landscape(pagesize)
            size = list(size); size.reverse(); size=tuple(size)
            cnt = list(cnt); cnt.reverse()
            space = list(space); space.reverse()
            LeftBottom = list(LeftBottom); LeftBottom.reverse()
        self.sizeX, self.sizeY = size[X], size[Y]


        if LeftBottom is None or LeftBottom is (None, None): LeftBottom = [None, None]

        self.c = canvas.Canvas(filename=filename, pagesize=pagesize)
        self.size, self.cnt, self.space, self.frame, self.filename = size, cnt, space, frame, filename

        self.pagesize = pagesize[0]/mm, pagesize[1]/mm
        o_size_x = (size[0] * cnt[0]) + ((cnt[0] - 1) * space[0])
        o_size_y = (size[1] * cnt[1]) + ((cnt[1] - 1) * space[1])
        if LeftBottom == [None, None]:
            LeftBottom[X] = (self.pagesize[X] - o_size_x) / 2
            LeftBottom[Y] = (self.pagesize[Y] - o_size_y) / 2
        self.LeftBottom = LeftBottom


        self.positions = []
        self.setLineWidth(0.1)

        for idx_x in range(self.cnt[X]):
            x = self.LeftBottom[X] + (idx_x * (self.size[X] + self.space[X]))
            for idx_y in range(self.cnt[Y]):
                y = self.LeftBottom[Y] + (idx_y * (self.size[Y] + self.space[Y]))
                #if self.frame == 1 or True:
                    #self.c.rect(x * mm, y * mm, self.size[X] * mm, self.size[Y] * mm)
                self.positions.append([x,y])
        self.__page_begin()

    def setFrame(self, thickness = 0.5, spacing=0):
        self.frame, self.frame_spacing = thickness,spacing
    def setMarksOuter(self, thickness = 0.5, size = 5):
        self.marks_outer_spacing, self.marks_outer_length, self.marks_outer = size * mm, size * mm, thickness * mm
    def setMarksInner(self, thickness = 0.5, size = 5):
        self.marks_inner_spacing, self.marks_inner_length, self.marks_inner = size * mm, size * mm, thickness * mm

    def __page_begin(self):
        if self.frame or True:
            self.c.setStrokeColorRGB(0,0,0)
            ptr = 0
            for ix in range(self.cnt[X]):
                for iy in range(self.cnt[Y]):
                    idx = self.positions[ptr][X]*mm, self.positions[ptr][Y]*mm
                    ptr += 1
                    if self.frame:
                        self.c.setLineWidth(self.frame * mm)
                        self.c.rect(idx[X] - self.frame_spacing*mm, idx[Y] - self.frame_spacing*mm, (self.size[X] * mm) + (self.frame_spacing * 2*mm), (self.size[Y] * mm) + (self.frame_spacing * 2*mm))
                    if self.marks_inner: # inner Marks
                        self.__draw_corner("LB", idx[X], idx[Y], self.marks_inner_length * mm, space=self.marks_inner_spacing * mm, thickness=self.marks_inner * mm)
                        self.__draw_corner("RT", self.size[X] * mm + idx[X], self.size[Y] * mm + idx[Y], self.marks_inner_length * mm, space=self.marks_inner_spacing * mm, thickness=self.marks_inner * mm)
                        self.__draw_corner("RB", idx[X] + self.size[X] * mm, idx[Y], self.marks_inner_length * mm, space=self.marks_inner_spacing * mm, thickness=self.marks_inner * mm)  #RightBottom
                        self.__draw_corner("LT", idx[X], idx[Y] + self.size[Y] * mm, self.marks_inner_length * mm, space=self.marks_inner_spacing * mm, thickness=self.marks_inner * mm) #LeftTop
                    if self.marks_outer:
                        self.c.setLineWidth(self.marks_outer * mm)
                        if ix == 0 and iy == 0:
                            self.__draw_corner("LB", idx[X], idx[Y], self.marks_outer_length * mm, space=self.marks_outer_spacing * mm, thickness=self.marks_outer * mm)
                        if ix == self.cnt[X]-1 and iy == 0:
                            self.__draw_corner("RB", idx[X] + self.sizeX * mm, idx[Y], self.marks_outer_length * mm, space=self.marks_outer_spacing * mm, thickness=self.marks_outer * mm)
                        if ix == 0 and iy == self.cnt[Y]-1: #left top
                            self.__draw_corner("LT", idx[X], idx[Y] + self.sizeY * mm, self.marks_outer_length * mm, space=self.marks_outer_spacing * mm, thickness=self.marks_outer * mm)
                        if ix == self.cnt[X]-1 and iy == self.cnt[Y]-1:
                            self.__draw_corner("RT", idx[X] + self.sizeX * mm, idx[Y] + self.sizeY * mm, self.marks_outer_length * mm, space=self.marks_outer_spacing * mm, thickness=self.marks_outer * mm)

            self.c.setLineWidth(0.1)



    def __draw_corner(self, pos ,x ,y , length, space = 0, thickness = 0.1):
        self.c.setLineWidth(thickness)
        th = thickness / 2
        if pos == "LT":
            x, y = x - space, y + space
            self.c.line(x-th, y, x + length, y)
            self.c.line(x, y, x, y - length)
        if pos == "RB":
            x, y = x + space, y - space
            self.c.line(x+th, y, x - length, y)
            self.c.line(x, y, x, y + length)
        if pos == "LB":
            x, y = x - space, y - space
            self.c.line(x-th, y, x + length, y)
            self.c.line(x, y, x, y + length)
        if pos == "RT":
            x, y = x + space, y + space
            self.c.line(x+th, y, x - length, y)
            self.c.line(x, y, x, y - length)


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

    def iter_label(self, data):
        try:
            idx = 0
            for d in (data):
                if idx == 0:
                    self.c.translate(self.positions[0][X]*mm, self.positions[0][Y]*mm)
                if idx >0:
                    dx = (self.positions[idx - 1][X] * mm* - 1) + self.positions[idx][X] * mm
                    dy = (self.positions[idx - 1][Y] * mm * -1) + self.positions[idx][Y] * mm
                    self.c.translate(dx,dy)
                yield d
                idx +=1
                if idx > self.cnt[X]*self.cnt[Y] -1:
                    idx = 0
                    self.c.showPage()
                    self.__page_begin()
        except:
            print("IndexError: list index out of range. The data is longer than the number of labels.")




    def save(self):
        self.c.save()

    def run(self):
        subprocess.Popen(self.filename, shell=True)

    def print(self):
        pass
        import os
        os.startfile(self.filename, "print")

        #Parameters adobe
        # /p <filename> - Open and go straight to the print dialog





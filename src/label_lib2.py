#awwolf 11.10.2019 V1.0
from reportlab.lib.pagesizes import A4,landscape    # pip install reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm,cm,inch
#for Datamatrix generation
from pystrich.datamatrix import DataMatrixEncoder # pip install pystrich==0.8
from reportlab.lib.utils import ImageReader
import io

import subprocess, os

X, Y, X2, Y2 = 0, 1, 2, 3

'''Posible Fonts
Times-Roman           Courier                    Helvetica                 
Times-Bold            Courier-Bold               Helvetica-Bold            
Times-Italic          Courier-Oblique            Helvetica-Oblique         
Times-BoldItalic      Courier-BoldOblique        Helvetica-BoldOblique    '''

class LabelPage():
    def __init__(self, size, cnt, space=(0,0), LeftBottom=(None, None), pagesize=None, rotate=False, filename="Label_Lib.pdf"):
        #default parameters
        pagesize = A4
        self.frame_spacing, self.frame, self.frame_round = 0, 0, None
        self.marks_outer_spacing, self.marks_outer_length, self.marks_outer = -10, 30, 0
        self.marks_inner_spacing, self.marks_inner_length, self.marks_inner = -20, 5, 0

        #change rotation
        if rotate:
            pagesize=landscape(pagesize)
            size = list(size); size.reverse(); size=tuple(size)
            cnt = list(cnt); cnt.reverse()
            space = list(space); space.reverse()
            LeftBottom = list(LeftBottom); LeftBottom.reverse()
        self.sizeX, self.sizeY = size[X], size[Y]
        if LeftBottom is None:
            LeftBottom = [None, None]
        LeftBottom = list(LeftBottom)

        self.c = canvas.Canvas(filename=filename, pagesize=pagesize)
        #self.c.scale(mm, mm)
        self.size, self.cnt, self.space, self.filename, self.new_page = size, cnt, space,  filename, False

        self.pagesize = pagesize[0]/mm, pagesize[1]/mm

        o_size_x = (size[0] * cnt[0]) + ((cnt[0] - 1) * space[0])
        o_size_y = (size[1] * cnt[1]) + ((cnt[1] - 1) * space[1])
        if LeftBottom == [None, None]:
            LeftBottom[X] = (self.pagesize[X] - o_size_x) / 2
            LeftBottom[Y] = (self.pagesize[Y] - o_size_y) / 2
        self.LeftBottom = LeftBottom
        self.c.scale(mm, mm)
        #calculation positions
        self.positions = []
        for idx_y in range(self.cnt[Y]).__reversed__():
            y = self.LeftBottom[Y] + (idx_y * (self.size[Y] + self.space[Y]))
            for idx_x in range(self.cnt[X]):
                x = self.LeftBottom[X] + (idx_x * (self.size[X] + self.space[X]))
                self.positions.append([x,y])

    def setFrame(self, thickness = 0.5, spacing=0, round=False):
        self.frame, self.frame_spacing, self.frame_round = thickness,spacing, round
    def setMarksOuter(self, thickness = 0.5, spacing = 5):
        self.marks_outer_spacing, self.marks_outer_length, self.marks_outer = spacing, spacing, thickness
    def setMarksInner(self, thickness = 0.5, spacing = 5):
        self.marks_inner_spacing, self.marks_inner_length, self.marks_inner = spacing, spacing, thickness

    def __page_begin(self):
        self.new_page = True
        if self.frame or True:
            self.c.setStrokeColorRGB(0,0,0)
            ptr = 0
            for iy in range(self.cnt[Y]):
                for ix in range(self.cnt[X]):
                    idx = self.positions[ptr][X], self.positions[ptr][Y]
                    ptr += 1
                    if self.frame:
                        self.c.setLineWidth(self.frame)
                        if self.frame_round == False:    #draws a rect over each label
                            self.c.rect(idx[X] - self.frame_spacing, idx[Y] - self.frame_spacing, (self.size[X]) + (self.frame_spacing * 2), (self.size[Y]) + (self.frame_spacing * 2))
                        if self.frame_round == True:  # draws a circle in the middle of each label
                            self.c.circle(idx[X] + self.size[X] / 2, idx[Y] + self.size[Y] / 2, self.size[X] / 2 + self.frame_spacing)
                            self.c.circle(idx[X] + self.size[X] / 2, idx[Y] + self.size[Y] / 2, self.size[Y] / 2 + self.frame_spacing)
                        else:
                            self.c.roundRect(idx[X] - self.frame_spacing, idx[Y] - self.frame_spacing, (self.size[X]) + (self.frame_spacing * 2), (self.size[Y]) + (self.frame_spacing * 2), self.frame_round)
                    if self.marks_inner: # inner Marks
                        self.__draw_corner("LB", idx[X], idx[Y], self.marks_inner_length, space=self.marks_inner_spacing, thickness=self.marks_inner)
                        self.__draw_corner("RT", self.size[X] + idx[X], self.size[Y] + idx[Y], self.marks_inner_length, space=self.marks_inner_spacing, thickness=self.marks_inner)
                        self.__draw_corner("RB", idx[X] + self.size[X], idx[Y], self.marks_inner_length, space=self.marks_inner_spacing, thickness=self.marks_inner)  #RightBottom
                        self.__draw_corner("LT", idx[X], idx[Y] + self.size[Y], self.marks_inner_length, space=self.marks_inner_spacing, thickness=self.marks_inner) #LeftTop
                    if self.marks_outer:
                        self.c.setLineWidth(self.marks_outer)
                        if ix == 0 and iy == 0:
                            self.__draw_corner("LT", idx[X], idx[Y] + self.sizeY, self.marks_outer_length, space=self.marks_outer_spacing, thickness=self.marks_outer)
                        if ix == self.cnt[X]-1 and iy == 0:
                            self.__draw_corner("RT", idx[X] + self.sizeX, idx[Y] + self.sizeY, self.marks_outer_length, space=self.marks_outer_spacing, thickness=self.marks_outer)
                        if ix == 0 and iy == self.cnt[Y]-1: #left top
                            self.__draw_corner("LB", idx[X], idx[Y], self.marks_outer_length, space=self.marks_outer_spacing, thickness=self.marks_outer)
                        if ix == self.cnt[X]-1 and iy == self.cnt[Y]-1:
                            self.__draw_corner("RB", idx[X] + self.sizeX, idx[Y], self.marks_outer_length, space=self.marks_outer_spacing, thickness=self.marks_outer)

            self.c.setLineWidth(0.1)


    def __draw_corner(self, direction, x, y, length, space = 0, thickness = 0.1):
        #draws a corner on the x,y position for cutting
        self.c.setLineWidth(thickness)
        th = thickness / 2
        if direction == "LT":
            x, y = x - space, y + space
            self.c.line(x-th, y, x + length, y)
            self.c.line(x, y, x, y - length)
        if direction == "RB":
            x, y = x + space, y - space
            self.c.line(x+th, y, x - length, y)
            self.c.line(x, y, x, y + length)
        if direction == "LB":
            x, y = x - space, y - space
            self.c.line(x-th, y, x + length, y)
            self.c.line(x, y, x, y + length)
        if direction == "RT":
            x, y = x + space, y + space
            self.c.line(x+th, y, x - length, y)
            self.c.line(x, y, x, y - length)

    def get_canvas_object(self):
        return self.c

    def setStrokeColorRGB(self, r, g, b, alpha=None):
        self.c.setStrokeColorRGB(r/255, g/255, b/255, alpha)
    def setFillColorRGB(self, r, g, b, alpha=None):
        self.c.setFillColorRGB(r/255, g/255, b/255, alpha)

    def iter_label(self, data = None):
        if data == None:
            data = range(self.cnt[X] * self.cnt[Y])
        try:
            idx = 0
            for i, d in enumerate(data):
                if idx == 0:
                    self.__page_begin()
                    self.c.translate(self.positions[0][X], self.positions[0][Y])
                    self.new_page = True
                if idx >0:
                    dx = (self.positions[idx - 1][X] * - 1) + self.positions[idx][X]
                    dy = (self.positions[idx - 1][Y] * -1) + self.positions[idx][Y]
                    self.c.translate(dx,dy)
                    self.new_page = False
                yield d
                idx +=1
                if idx > self.cnt[X]*self.cnt[Y] -1:
                    idx = 0
                    if i < len(data) - 1:
                        self.c.showPage()
                        self.c.scale(mm, mm)
                        self.__page_begin()
        except:
            print("IndexError: list index out of range. The data is longer than the number of labels.")

    def draw_datamatrix(self, text, x, y, size, anchor="C"):
        e_datamatrix = DataMatrixEncoder(text)
        img = ImageReader(io.BytesIO(e_datamatrix.get_imagedata()))
        _x, _y = x - size / 2,  y - size / 2
        if "N" in str(anchor).upper(): _y = y - size
        if "S" in str(anchor).upper(): _y = y
        if "E" in str(anchor).upper(): _x = x - size
        if "W" in str(anchor).upper(): _x = x
        self.c.drawImage(img, _x, _y, *[size] * 2)


    def save(self):
        self.c.save()

    def show(self):
        subprocess.Popen(self.filename, shell=True)

    def print(self):
        os.startfile(self.filename, "print")
        #Parameters adobe
        # /p <filename> - Open and go straight to the print dialog





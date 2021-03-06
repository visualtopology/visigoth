# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#   and associated documentation files (the "Software"), to deal in the Software without 
#   restriction, including without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all copies or 
#   substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from visigoth.common.diagram_element import DiagramElement
from visigoth.svg.line import line

class Sequence(DiagramElement):

    class Separator(object):

        def __init__(self,parent,stroke,stroke_width,fraction):
            self.parent = parent
            self.stroke = stroke
            self.stroke_width = stroke_width
            self.fraction = fraction

        def build(self,format):
            pass

        def getWidth(self):
            if self.parent.layout == "vertical":
                return 0
            else:
                return self.stroke_width

        def getHeight(self):
            if self.parent.layout == "vertical":
                return self.stroke_width
            else:
                return 0

        def draw(self,doc,cx,cy):
            if self.parent.layout == "vertical":
                x1 = cx-self.fraction*self.parent.getWidth()/2
                x2 = cx+self.fraction*self.parent.getWidth()/2
                y1 = cy
                y2 = cy
            else:
                y1 = cy - self.fraction * self.parent.getHeight() / 2
                x2 = cy + self.fraction * self.parent.getHeight() / 2
                x1 = cx
                x2 = cx
            l = line(x1,y1,x2,y2,stroke=self.stroke,stroke_width=self.stroke_width)
            doc.add(l)

        def getLeftJustified(self):
            return False

        def getRightJustified(self):
            return False

        def getTopJustified(self):
            return False

        def getBottomJustified(self):
            return False

    """
    Construct a container holding multiple elements in a sequence layout

    Keyword Arguments:
        spacing(int): spacing between elements in pixels
        orientation(str): vertical|horizontal whether to layout the sequence top-to-bottom or left-to-right

    The way you might use me is:

    >>> d = Diagram()
    >>> s = Sequence()
    >>> s.add(Text("Here is some text"))
    >>> s.add(Text("Here is some more text"))
    >>> d.add(s)
    """

    def __init__(self,spacing=20,orientation="vertical"):
        DiagramElement.__init__(self)
        self.elements = []
        self.spacing = spacing
        self.layout = orientation

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def build(self,fmt):
        for idx in range(len(self.elements)):
            element = self.elements[idx]
            element.build(fmt)

        total_spacing = 0
        if len(self.elements):
            total_spacing = self.spacing*(len(self.elements)-1)

        if self.layout == "vertical":
            self.width = max([element.getWidth() for element in self.elements])
            self.height = total_spacing+sum([element.getHeight() for element in self.elements])
        else:
            self.width = total_spacing+sum([element.getWidth() for element in self.elements])
            self.height = max([element.getHeight() for element in self.elements])

    def add(self,element):
        """
        Add an element to the sequence to appear after previously added elements

        Arguments:
            element(DiagramElement): the element to append to the sequence
        """
        self.elements.append(element)
        return self

    def remove(self, element):
        self.elements.remove(element)

    def addSeparator(self,stroke="black",stroke_width=2,fraction=1.0):
        self.elements.append(Sequence.Separator(self,stroke,stroke_width,fraction))

    def draw(self,doc,cx,cy):
        off_y = cy-self.height/2
        off_x = cx-self.width/2

        if self.layout == "vertical":
            for e in self.elements:

                ecx = cx
                if e.getLeftJustified():
                    ecx = off_x + e.getWidth()/2
                elif e.getRightJustified():
                    ecx = cx + self.width/2 - e.getWidth()/2
                e.draw(doc, ecx, off_y+e.getHeight()/2)
                off_y += self.spacing + e.getHeight()
        else:
            for e in self.elements:
                e.draw(doc, off_x+e.getWidth()/2, cy)
                off_x += self.spacing + e.getWidth()


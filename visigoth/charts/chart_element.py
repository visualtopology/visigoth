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

import os.path

from visigoth.common import DiagramElement
from visigoth.svg import line
from visigoth.utils.js import Js

class ChartElement(DiagramElement):

    def __init__(self):
        super(ChartElement,self).__init__()
        self.setTooltipFunction()
        self.setGridStyle()
        self.colour_manager = None
        self.marker_manager = None
        self.xAxis = None
        self.yAxis = None
        self.draw_grid = False

        self.marginx = 0
        self.marginy = 0

    def setDrawGrid(self,draw_grid):
        self.draw_grid = draw_grid

    def setPalette(self,colour_manager):
        self.colour_manager = colour_manager

    def getPalette(self):
        return self.colour_manager

    def setMargins(self,marginx,marginy):
        self.marginx = marginx
        self.marginy = marginy

    def setMarkerManager(self,marker_manager):
        self.marker_manager = marker_manager

    def getMarkerManager(self):
        return self.marker_manager

    def setAxes(self,xAxis,yAxis):
        self.xAxis = xAxis
        self.yAxis = yAxis

    def getAxes(self):
        return (self.xAxis,self.yAxis)

    def setGridStyle(self,stroke="grey",stroke_width=1):
        self.grid_stroke = stroke
        self.grid_stroke_width = stroke_width

    def setTooltipFunction(self,fn = lambda cat,val: "%s: %0.2f"%(cat,val)):
        self.tooltip_fn = fn

    def getTooltip(self,cat,val):
        return self.tooltip_fn(cat,val)

    def configureXRange(self,axis_min,axis_max):
        self.x_axis_min = axis_min
        self.x_axis_max = axis_max

    def configureYRange(self,axis_min,axis_max):
        self.y_axis_min = axis_min
        self.y_axis_max = axis_max

    def getXRange(self):
        return (self.x_axis_min,self.x_axis_max)

    def getYRange(self):
        return (self.y_axis_min,self.y_axis_max)

    def configureChartArea(self,ox,oy,width,height):
        self.chart_ox = ox
        self.chart_oy = oy
        self.chart_width = width
        self.chart_height = height

    def computeX(self,value):
        return self.xAxis.getPointPosition(self.chart_ox,value)

    def computeY(self,value):
        return self.yAxis.getPointPosition(self.chart_oy,value)

    def build(self,fmt):
        if self.colour_manager:
            self.colour_manager.build()

        x_axis_height = 0
        y_axis_width = 0

        if self.xAxis:
            self.xAxis.build(fmt)
            x_axis_height = self.xAxis.getHeight()
        if self.yAxis:
            self.yAxis.build(fmt)
            y_axis_width = self.yAxis.getWidth()
        
        if self.xAxis:
            self.xAxis.setLength(self.getWidth()-y_axis_width-2*self.marginx)
        if self.yAxis:
            self.yAxis.setLength(self.getHeight()-x_axis_height-2*self.marginy)
        
        if self.xAxis:
            self.xAxis.build(fmt)
            x_axis_height = self.xAxis.getHeight()
        if self.yAxis:
            self.yAxis.build(fmt)
            y_axis_width = self.yAxis.getWidth()
        
        self.chart_width = self.getWidth() - y_axis_width
        self.chart_height = self.getHeight() - x_axis_height

    def drawGrid(self,doc):

        if self.yAxis and not self.yAxis.isDiscrete():
            y_ticks = self.yAxis.getTickPositions(self.chart_oy)
            x1 = self.chart_ox
            x2 = self.chart_ox + self.chart_width
            for y in y_ticks:
                l = line(x1,y,x2,y,self.grid_stroke,self.grid_stroke_width)
                doc.add(l)

        if self.xAxis and not self.xAxis.isDiscrete:
            x_ticks = self.xAxis.getTickPositions(self.chart_ox)
            y1 = self.chart_oy
            y2 = self.chart_oy + self.chart_height
            for x in x_ticks:
                l = line(x,y1,x,y2,self.grid_stroke,self.grid_stroke_width)
                doc.add(l)

    def getSlices(self):
        # Override in charts which support slices
        return None

    def draw(self,doc,cx,cy):
        # self.openClip(doc,cx,cy)
        ox = cx - self.getWidth()/2
        oy = cy - self.getHeight()/2

        chart_height = self.getHeight()
        chart_width = self.getWidth()

        x_axis_height = 0
        if self.xAxis:
            x_axis_min = self.xAxis.getMinValue()
            x_axis_max = self.xAxis.getMaxValue()
            self.configureXRange(x_axis_min,x_axis_max)
            x_axis_height = self.xAxis.getHeight()
            chart_height -= x_axis_height
        chart_height -= 2*self.marginy

        y_axis_width = 0
        if self.yAxis:
            y_axis_min = self.yAxis.getMinValue()
            y_axis_max = self.yAxis.getMaxValue()
            self.configureYRange(y_axis_min,y_axis_max)
            y_axis_width = self.yAxis.getWidth()
            chart_width -= y_axis_width

        chart_width -= 2*self.marginx

        self.configureChartArea(ox+y_axis_width+self.marginx,oy+self.marginy,chart_width,chart_height)

        if self.xAxis:
            self.xAxis.draw(doc,self.chart_ox+self.chart_width/2,oy+self.marginy+self.chart_height+x_axis_height/2)
        if self.yAxis:
            self.yAxis.draw(doc,ox+self.marginx+y_axis_width/2,self.chart_oy+self.chart_height/2)

        if self.draw_grid:
            self.drawGrid(doc)

        # compute the centre of the chart drawing area
        chart_cx = self.chart_ox + self.chart_width/2
        chart_cy = self.chart_oy + self.chart_height/2
        config = self.drawChart(doc,chart_cx,chart_cy,self.chart_width,self.chart_height)

        # self.closeClip(doc)

        with open(os.path.join(os.path.split(__file__)[0],"chart_element.js"),"r") as jsfile:
            jscode = jsfile.read()
        Js.registerJs(doc,self,jscode,"chart_element",cx,cy,config)
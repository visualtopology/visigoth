# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from visigoth.svg.svgstyled import svgstyled

class image(svgstyled):

    def __init__(self,x,y,width,height,uri,tooltip=""):
        svgstyled.__init__(self,"image",tooltip)
        self.x = x
        self.y = y
        self.uri = uri
        self.width = width
        self.height = height
        self.addAttr("x",self.x)
        self.addAttr("y",self.y)
        self.addAttr("href",self.uri)
        self.addAttr("width",self.width)
        self.addAttr("height",self.height)
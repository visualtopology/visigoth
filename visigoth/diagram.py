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

import os.path
import os

import visigoth
from visigoth.svg import svgdoc,rectangle
from visigoth.utils.js import Js
from visigoth.svg import javascript_snippet, css_snippet
from visigoth.common.text import Text, Span
from visigoth.utils.fonts import FontManager
from visigoth.containers.sequence import Sequence


class Diagram:

        
    """
    Represent a diagram contining one or more maps and other elements

    Keyword Arguments:
        title(str) : title string to add to the output document
        description(str) : description to place in the output document
        fill(str): background colour for the diagram
        margin_top(int): margin around the top of the diagram
        margin_bottom(int): margin around the bottom of the diagram
        margin_left(int): margin around the left of the diagram
        margin_right(int): margin around the right of the diagram
        spacing(int): spacing between elements in pixels

    A way you might use me is:

    >>> d = Diagram(fill="white")
    >>> from visigoth.common.text import Text
    >>> d.add(Text("Hello World!")
    >>> print(d.draw()) # print the svg to the console
    """

    def __init__(self,title="",description="",fill=None,margin_left=50,margin_right=50,margin_top=50,margin_bottom=50,spacing=20):
        self.title = title
        self.description = description

        self.fill = fill
        self.margin_top = margin_top
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.spacing = spacing
        self.content = Sequence()
        self.snippets = []
        self.connections = []
        self.styles = [Diagram.default_style]
        self.default_text_attributes = {}
        
        with open(os.path.join(os.path.split(__file__)[0],"diagram.js"),"r") as jsfile:
            jscode = jsfile.read()
        self.snippets.append(jscode)
        self.font_embedding = False
        FontManager.registerFonts()

        self.setDefaultTextAttributes({"font-family":"Roboto"})

    def setFontEmbedding(self,embed):
        """
        Enable or disable font embedding

        Arguments:
            embed(bool): whether to embed fonts or link to them

        Notes:
            By default fonts are not embedded into the output SVG but are linked from google's servers.
            Fonts should be embedded if you want content to render correctly when offline or when the SVG file
            is to be rendered as an image.  If enabled, only fonts that were used will be embedded.
        """
        self.font_embedding = True

    default_style = """
        .geopath:hover { filter: url(#glow); }
        .geopolygon:hover path { fill: #00f; }
        .geopoint:hover { filter: url(#glow); }
        :focus { outline: 5px solid orange; }
        .highlight { filter: url(#glow); }
        """
    
    def getTitle(self):
        return self.title

    def getDescription(self):
        return self.description

    def generateFooter(self):
        return Text(
            [Span("Generated by: "),
             Span(" visigoth v"+visigoth.version, url=visigoth.home_url),
             Span(" ( "),
             Span(" source code", url=visigoth.repo_url),
             Span(" ) ")],font_height=14)

    def search(self,element_id):
        return self.content.search(element_id)

    def removeElement(self,element_id):
        ele = self.search(element_id)
        container = ele.getContainer()
        container.remove(ele)

    def addStyle(self,style):
        """
        Add CSS styles to the diagram

        Arguments:
            style(str) a string containing CSS text

        Returns:
            the Diagram object
        """
        self.styles.append(style)
        return self

    def add(self,element):
        """
        Add an element to the diagram

        Arguments:
            element(visigoth.common.DiagramElement): the element to add

        Returns:
            the Diagram object

        Notes:
        """
        self.content.add(element)
        return self

    def clear(self):
        self.connections = []

    def connect(self,source,source_channel,dest,dest_channel,adapter_function="function(event) { return event; }"):
        """
        Connect two elements in the diagram with a channel to allow one to receive events sent by the other

        Arguments:
            source(visigoth.common.DiagramElement): the element emitting events
            source_channel(str): the name of the channel sending events from the source
            dest(visigoth.common.DiagramElement): the element receiving events
            dest_channel(str): the name of the channel recieving events to the destination
            adapter_function(str): a definition for a javascript function which transforms the event as it is dispatched to the destination

        Returns:
            the Diagram object
        """
        if (source,source_channel,dest,dest_channel,adapter_function) not in self.connections:
            self.connections.append((source,source_channel,dest,dest_channel,adapter_function))
        return self
        
    def addJavascript(self,snippet):
        """
        Add javascript code to the Diagram

        Returns:
            the Diagram object
        """
        self.snippets.append(snippet)
        return self

    def setDefaultTextAttributes(self,text_attributes):
        """
        Define default attributes for text displayed in the diagram

        Arguments:
            text_attributes(dict): dict containing SVG name,value attributes to apply to text by default

        Returns:
            the Diagram object

        Notes:
            default attributes are overridden by those defined on diagram elements
        """
        for key in text_attributes:
            self.default_text_attributes[key] = text_attributes[key]
            
        FontManager.setFontDefaults(
            self.default_text_attributes.get("font-family","Roboto"),
            self.default_text_attributes.get("font-weight","normal"), 
            self.default_text_attributes.get("font-style","normal"), 
        )
        return self

    def getDefaultTextAttributes(self):
        return self.default_text_attributes

    def __repr_svg__(self):
        return self.draw()

    def draw(self,format="svg",html_title="",include_footer=True):
        """
        Draw the diagram to create an SVG document

        Keyword Arguments:
            format(str): the format of the output file, either "svg" or "html"
            html_title(str): the title for the document valid for format="html"
            include_footer(bool): whether to include a footer with project/github repo links

        Returns:
            a string containing the document in the requested format
        """

        if include_footer:
            footer = self.generateFooter()
            self.content.add(footer)

        target = self.content

        target.build()

        w = target.getWidth()
        h = target.getHeight()

        w += self.margin_left + self.margin_right
        h += self.margin_top + self.margin_bottom

        d = svgdoc(self, w, h, format, html_title=html_title)
        d.setMetadata(visigoth.version,visigoth.home_url,visigoth.repo_url)
        d.setEmbedFonts(self.font_embedding)

        for style in self.styles:
            d.addStyle(css_snippet(style))

        if self.fill:
            d.add(rectangle(0,0,w,h,fill=self.fill))

        off_x = self.margin_left
        off_y = self.margin_top

        for snippet in self.snippets:
            d.add(javascript_snippet(snippet,False))

        target.draw(d, off_x+target.getWidth()/2, off_y+target.getHeight()/2)

        for (source,source_channel,dest,dest_channel,adapter_function) in self.connections:
            Js.connect(d,source,source_channel,dest,dest_channel,adapter_function)

        if include_footer:
            self.content.remove(footer)
        return d.render()

# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

import unittest

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.containers.box import Box
from visigoth.containers.map import Map
from visigoth.containers.sequence import Sequence

from visigoth.map_layers.gridsquares import GridSquares
from visigoth.map_layers.wms import WMS
from visigoth.utils.mapping import Geocoder
from visigoth.utils.mapping import Projections,Mapping


class TestMap(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        gc = Geocoder()
        center = gc.fetchCenter("Berlin")
        bounds = Mapping.computeBoundaries(center,4000,projection=Projections.ESPG_3857)
        m1 = Map(768, boundaries=bounds, projection=Projections.ESPG_3857)
        
        wms1 = WMS(type="osm")
        wms1.setInfo("Map")

        grid1 = GridSquares()
        grid1.setInfo("Grid")

        m1.addLayer(wms1)
        m1.addLayer(grid1)

        s1 = Sequence()
        s1.add(m1)

        d.add(Box(s1))

        bounds = Mapping.computeBoundaries(center,4000,projection=Projections.ESPG_3857)
        m2 = Map(768,boundaries=bounds,projection=Projections.ESPG_3857)

        wms2 = WMS(type="osm")
        wms2.setInfo("Map")

        grid2 = GridSquares()
        grid2.setInfo("Grid")

        m2.addLayer(wms2)
        m2.addLayer(grid2)
        grid2.setOpacity(0.5)

        s2 = Sequence()
        s2.add(m2)

        d.add(Box(s2))

        svg = d.draw()
        TestUtils.output(svg,"test_map.svg")

if __name__ == "__main__":
    unittest.main()
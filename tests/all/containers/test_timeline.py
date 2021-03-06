# -*- coding: utf-8 -*-
# Copyright 2017-2018 Niall McCarroll
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import datetime

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.containers import TimeLine, Box
from visigoth.charts import Bar
from visigoth.common import Legend, Text
from visigoth.utils.colour import DiscreteColourManager

class TestSequence(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        timeline1 = TimeLine(orientation="vertical")
        timeline2 = TimeLine(orientation="horizontal")

        colour_manager = DiscreteColourManager()
        colour_manager.addColour("A","#E7FFAC").addColour("B","#FFC9DE")
        colour_manager.addColour("C","#B28DFF").addColour("D","#ACE7FF")

        data1 = [("A",10),("B",5),("C",-4),("D",3)]
        data2 = [("A",8),("B",2),("C",-1),("D",6)]
        data3 = [("A",3),("B",5),("C",2),("D",-3)]

        bar1 = Bar(data1, x=0, y=1, colour=0, width=400, height=400, colour_manager=colour_manager)
        bar2 = Bar(data2, x=0, y=1, colour=0, width=200, height=200, colour_manager=colour_manager)
        bar3 = Bar(data3, x=0, y=1, colour=0, width=300, height=300, colour_manager=colour_manager)

        timeline1.add(datetime.datetime(2016,1,1,0,0,0),None,"2016")
        timeline1.add(datetime.datetime(2017,1,1,0,0,0),Box(bar1),"2017",offset=100)
        timeline1.add(datetime.datetime(2017,1,1,0,0,0), Box(Text("Event")), None, offset=100)
        timeline1.add(None,Box(Text("Inserted text with no date")),None,offset=100)
        timeline1.add(datetime.datetime(2018,1,1,0,0,0),Box(bar2),"2018",offset=150)
        timeline1.add(datetime.datetime(2019,1,1,0,0,0),Box(bar3),"2019",offset=120)
        timeline1.add(datetime.datetime(2020,1,1,0,0,0),None,"2020")

        timeline2.add(datetime.datetime(2016,1,1,0,0,0),None,"2016")
        timeline2.add(datetime.datetime(2017,1,1,0,0,0),Box(bar1),"2017",offset=50)
        timeline2.add(datetime.datetime(2018,1,1,0,0,0),Box(bar2),"2018",offset=120)
        timeline2.add(datetime.datetime(2019,1,1,0,0,0),Box(bar3),"2019",offset=90)
        timeline2.add(datetime.datetime(2020,1,1,0,0,0),None,"2020")

        d.add(timeline1).add(timeline2)
        legend = Legend(colour_manager=colour_manager,legend_columns=4,width=768)
        d.add(legend)

        TestUtils.draw_output(d, "test_timeline")

    def test_text(self):
        d = Diagram(fill="white")

        timeline1 = TimeLine(orientation="vertical")
        timeline2 = TimeLine(orientation="horizontal")

        timeline1.add(datetime.datetime(2016, 1, 1, 0, 0, 0), None, "2016 !!!!!!")
        timeline1.add(datetime.datetime(2017, 1, 1, 0, 0, 0), Box(Text("Event 1234 1234",font_height=40)), None, offset=100)
        timeline1.add(datetime.datetime(2020, 1, 1, 0, 0, 0), None, "2020 !!!!!!")

        timeline2.add(datetime.datetime(2016, 1, 1, 0, 0, 0), None, "2016 !!!!!!")
        timeline2.add(datetime.datetime(2017, 1, 1, 0, 0, 0), Box(Text("Event 1234 1234", font_height=40)), None,
                      offset=100)
        timeline2.add(datetime.datetime(2020, 1, 1, 0, 0, 0), None, "2020 !!!!!!")

        d.add(Box(timeline1))
        d.add(Box(timeline2))

        TestUtils.draw_output(d, "test_timeline_text")

if __name__ == "__main__":
    unittest.main()
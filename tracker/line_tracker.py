# -*- coding: utf-8 -*-
#**************************************************************************
#*                                                                     *
#* Copyright (c) 2019 Joel Graff <monograff76@gmail.com>               *
#*                                                                     *
#* This program is free software; you can redistribute it and/or modify*
#* it under the terms of the GNU Lesser General Public License (LGPL)  *
#* as published by the Free Software Foundation; either version 2 of   *
#* the License, or (at your option) any later version.                 *
#* for detail see the LICENCE text file.                               *
#*                                                                     *
#* This program is distributed in the hope that it will be useful,     *
#* but WITHOUT ANY WARRANTY; without even the implied warranty of      *
#* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the       *
#* GNU Library General Public License for more details.                *
#*                                                                     *
#* You should have received a copy of the GNU Library General Public   *
#* License along with this program; if not, write to the Free Software *
#* Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307*
#* USA                                                                 *
#*                                                                     *
#***********************************************************************
"""
Line tracker class for tracker objects
"""

from ..support.smart_tuple import SmartTuple

from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.coin_styles import CoinStyles

from .geometry_tracker import GeometryTracker

class LineTracker(GeometryTracker):
    """
    Tracker object for SoLineSet
    """

    def __init__(self, name, points, parent, view=None):
        """
        Constructor
        """

        super().__init__(name=name, parent=parent, view=view)

        #build node structure for the node tracker
        self.line = self.geometry.add_node(Nodes.LINE_SET, name)

        self.add_node_events(self.line)
        self.set_style()
        self.set_visibility(True)
        self.drag_style = self.DragStyle.CURSOR

        self.points = points

        self.update(points)

    def update(self, points):
        """
        Override of Geometry method
        """

        self.points = points
        super().update(points)

    def update_drag_center(self):
        """
        Override of Drag method
        """

        #default to the current cursor position
        _pt = self.mouse_state.world_position

        #average the coordinates to calculate the centerpoint
        if self.drag_style == self.DragStyle.AVERAGE:

            _pt = (0.0, 0.0, 0.0)

            for _p in self.points:
                _pt = SmartTuple._add(_pt, _p)

            _pt = SmartTuple._mul(_pt, 0.5)

        #use Manhattan distance to find nearest endpoint
        elif self.drag_style == self.DragStyle.ENDPOINT:

            _dist = -1
            _cursor = self.mouse_state.world_position
            _pt = _cursor

            _fn = lambda p1, p2: abs(_pt[0] - _p[0])\
                        + abs(_pt[1] - _p[1])\
                        + abs(_pt[2 - _p[2]])

            for _p in self.points:

                if _dist == -1:
                    _dist = _fn(_cursor, _p)
                    continue

                _new_dist = _fn(_cursor, _p)

                if _new_dist < _dist:
                    _dist = _new_dist
                    _pt = _p

        return _pt

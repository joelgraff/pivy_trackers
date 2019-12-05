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

from .geometry_tracker import GeometryTracker

class LineTracker(GeometryTracker):
    """
    Tracker object for SoLineSet
    """

    def __init__(self, name, points, parent, view=None, selectable=True):
        """
        Constructor
        """

        super().__init__(name=name, parent=parent, view=view)

        #build node structure for the node tracker
        self.line = self.geometry.add_node(Nodes.LINE_SET, name)
        self.add_node_events(self.line)
        self.groups = []

        self.set_style()
        self.set_visibility(True)
        self.set_selectability(selectable)
        self.drag_style = self.DragStyle.CURSOR

        self.linked_markers = {}

        self.update(points, notify=False)

    def set_selectability(self, selectable):
        """
        Set the mouse / button event nodes based on passed flag
        """

        if (selectable):
            self.event.root.whichChild = 0

        else:
            self.event.root.whichChild = -1

    def update(self, points, groups=None, notify=True):
        """
        Override of Geometry method
        """

        super().update(points, notify=notify)

        if groups is None:
            return

        self.groups = self.groups

        self.line.numVertices.setValues(0, len(groups), groups)

    def link_marker(self, marker, index):
        """
        Link a marker node to the line for automatic updates
        """

        #register the line and marker with each other
        self.register_geometry(marker, True)

        #save the index of the coordinate the marker updates
        if marker not in self.linked_markers:
            self.linked_markers[marker] = index

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

    def notify_geometry(self, event, message):
        """
        Geometry message notification override
        """
        super().notify_geometry(event, message)

        if not self.is_valid_notify:
            return

        #if this is an update from a marker, test to see if it is linked.
        if len (message.data) != len(self.points):

            if message.sender in self.linked_markers:

                self.points[self.linked_markers[message.sender]] \
                    = message.data[0]

        #Add sender to the excluded subscribers list, call update and
        #dispatch messages, then remove the sender
        self.excluded_subscribers.append(message.sender)
        self.update(self.points)
        del self.excluded_subscribers[-1]

    def notify_widget(self, event, message):
        """
        UI message notification override
        """
        super().notify_widget(event, message)

    def finish(self):
        """
        Cleanup
        """

        self.line = None
        self.drag_style = None
        self.points = None
        self.linked_markers = None

        super().finish()

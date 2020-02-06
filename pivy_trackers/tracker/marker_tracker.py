# -*- coding: utf-8 -*-
#***********************************************************************
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
Marker tracker class for tracker objects
"""

from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.coin_enums import MarkerStyles

from .geometry_tracker import GeometryTracker

class MarkerTracker(GeometryTracker):
    """
    Tracker object for nodes
    """

    def __init__(self, name, point, parent, view=None):
        """
        Constructor
        """

        super().__init__(name=name, parent=parent, view=view)

        self.point = None

        #build node structure for the node tracker
        self.marker = self.geometry.add_node(Nodes.MARKER_SET, name)

        self.add_node_events(self.marker)
        self.set_style()
        self.set_visibility(True)

        if not point:
            return

        self.point = tuple(point)
        self.update(notify=False)

    def update(self, coordinates=None, notify=True):
        """
        Update the coordinate position
        """

        _c = coordinates

        if not _c:
            _c = self.point

        elif isinstance(coordinates[0], tuple):
            self.point = coordinates[0]

        else:
            self.point = tuple(_c)

        super().update(_c, notify=notify)

    def update_drag_center(self):
        """
        Override of Drag base function
        """

        return self.point

    def set_style(self, style=None, draw=None, color=None):
        """
        Override style implementation
        """

        super().set_style(style, draw, color)

        if style is None:
            style = self.active_style

        self.marker.markerIndex = MarkerStyles.get(style.shape, style.size)

    def notify_geometry(self, event, message):
        """
        Geometry message notification override
        """

        super().notify_geometry(event, message)

        if not self.is_valid_notify:
            return

        _point = None

        if self.linked_geometry:

            _idx = message.sender.linked_geometry.get(self)

            if _idx is not None:
                _point = message.data[_idx[0]]

        if not _point:
            return

        if _point == self.point:
            return

        #Add sender to the excluded subscribers list, call update and
        #dispatch messages, then remove the sender
        self.excluded_subscribers.append(message.sender)

        self.update(_point)
        del self.excluded_subscribers[-1]

    def notify_widget(self, event, message):
        """
        Widget message notification override
        """

        if self.ignore_notify:
            return

        super().notify_widget(event, message)

    def finish(self):
        """
        Cleanup
        """

        self.point = None
        self.marker = None

        super().finish()

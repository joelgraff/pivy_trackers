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
Marker tracker class for tracker objects
"""

from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.coin_enums import MarkerStyles
from ..support.smart_tuple import SmartTuple

from .geometry_tracker import GeometryTracker
from .line_tracker import LineTracker

class MarkerTracker(GeometryTracker):
    """
    Tracker object for nodes
    """

    def __init__(self, name, point, parent, view=None):
        """
        Constructor
        """

        super().__init__(name=name, parent=parent, view=view)

        self.point = tuple(point)

        #build node structure for the node tracker
        self.marker = self.geometry.add_node(Nodes.MARKER_SET, name)

        self.add_node_events(self.marker)
        self.set_style()
        self.set_visibility(True)
        self.update(tuple(point), False)

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
            self.point = SmartTuple(_c)._tuple

        super().update(_c, notify)

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

        super().notify_geometry(message)

        if isinstance(message.sender, LineTracker):

            _idx = message.sender.linked_markers.get(self)

            if _idx is not None:
                self.point = message.data[_idx]

        #Add sender to the excluded subscribers list, call update and
        #dispatch messages, then remove the sender
        self.excluded_subscribers.append(message.sender)
        self.update(self.point)
        del self.excluded_subscribers[-1]

    def notify_user_interface(self, event, message):
        """
        UI message notification override
        """
        super().notify_ui(event, message)

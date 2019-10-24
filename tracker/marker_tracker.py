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
        self.update(tuple(point))

    def update(self, coordinates=None):
        """
        Update the coordinate position
        """

        _c = coordinates

        if not _c:
            _c = self.point
        else:
            self.point = SmartTuple(_c)._tuple

        super().update(_c)

        #if self.do_publish:
        #    self.dispatch(Events.NODE.UPDATED, (self.name, coordinates),
        #False)

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

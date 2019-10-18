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
Drag tracker for providing drag support to other trackers
"""

from ..support.smart_tuple import SmartTuple
from ..support.singleton import Singleton
from ..coin.coin_group import CoinGroup
from ..coin.coin_enums import NodeTypes as Nodes

from ..trait.base import Base
from ..trait.style import Style
from ..trait.event import Event
from ..trait.pick import Pick
from ..trait.geometry import Geometry

class DragTracker(Base, Style, Event, Pick, Geometry, metaclass=Singleton):
    """
    Drag tracker for providing drag support to other trackers
    """

    def __init__(self, parent):
        """
        Constructor
        """

        #Alter the geometry trait graph before initialization
        Geometry.init_graph(True, True)

        super().__init__('DragTracker', None, parent)

        self.drag = CoinGroup(is_switched=True, is_separated=True,
        parent=self.base, name='drag_tracker')

        self.drag.full = CoinGroup(is_switched=True, is_separated=True,
        parent=self.drag, name='drag_tracker_full')

        self.drag.full.transform = \
            self.drag.full.add_node(Nodes.TRANSFORM, 'transform')
        
        self.drag.full.group = self.drag.full.add_node(Nodes.GROUP, 'group')

        self.drag.part = CoinGroup(is_switched=True, is_separated=True,
        parent=self.drag, name='drag_tracker_part')

        self.drag.part.set_visibility()
        self.drag.full.set_visibility()
        self.drag.set_visibility()
        self.set_visibility()

        self.set_pick_style(False)
        self.partial_nodes = []
        self.partial_indices = []

        self.add_mouse_event(self.drag_mouse_event)
        self.add_button_event(self.drag_button_event)

        self.dragging = False

        #initialize the drag line
        self.show_drag_line = True

        self.geometry.line = \
            self.geometry.add_node(Nodes.LINE_SET, 'drag line')

        self.update([(0.0, 0.0, 0.0), (0.0, 0.0, 0.0)])

    def insert_full_drag(self, node):
        """
        Insert a graph to be fully transformed by dragging
        """

        self.drag.full.insert_node(node, self.drag.full.group)

    def insert_partial_drag(self, node, indices):
        """
        Insert a graph to be partially transformed by dragging
        """

        self.drag.part.insert_node(node)

        self.partial_nodes.append(node)
        self.partial_indices.append(indices)

    def drag_mouse_event(self, user_data, event_cb):
        """
        Drag mouse event callback
        """

        if self.mouse_state.button1.dragging and not self.dragging:
            if self.show_drag_line:
                self.geometry.set_visibility(True)

        self.dragging = self.mouse_state.button1.dragging

        if not self.dragging:
            return

        _coords = [
            self.mouse_state.button1.drag_start,
            self.mouse_state.world_position
        ]

        #update the transform
        self.translate(_coords[0], _coords[1])

        #update the drag line
        if self.show_drag_line:
            self.update(_coords)

    def drag_button_event(self, user_data, event_cb):
        """
        Drag button event callback
        """

        #end of drag state
        if not self.mouse_state.button1.dragging and self.dragging:

            self.drag.full.group.removeAllChildren()
            self.drag.part.remove_all_children()
            self.geometry.set_visibility(False)

##########################
## Transformation routines
##########################

    def translate(self, start_coord, end_coord):
        """
        Manage drag geometry translation
        """

        #accumulate the movement from the previous mouse position
        _delta = SmartTuple._sub(end_coord, start_coord)
        self.drag.full.transform.translation.setValue(_delta)

#    def rotate(self, coord):
#        """
#        Manage rotation during dragging
#        coord - coordinates for the rotation update
#        """

#        if not self.update_rotate:
#            return

#        _angle = 0.0

#        if self.rotation_center:
#            _angle = support.get_bearing(
#                SmartTuple._sub(coord, self.rotation_center))

#        else:

#            _dx_vec = SmartTuple._sub(
#                coord, self.drag.full.transform.translation.getValue())

#            self.drag.full.transform.center.setValue(coin.SbVec3f(_dx_vec))

#            self.rotation_center = coord
#            self.rotation = 0.0
#            self.angle = 0.0


#        _delta = self.angle - _angle

#        if _delta < -math.pi:
#            _delta += C.TWO_PI

#        elif _delta > math.pi:
#            _delta -= C.TWO_PI

#        self.rotation += _delta
#        self.angle = _angle

        #update the +z axis rotation for the transformation
#        self.drag.full.transform.rotation =\
#            coin.SbRotation(coin.SbVec3f(0.0, 0.0, 1.0), self.rotation)

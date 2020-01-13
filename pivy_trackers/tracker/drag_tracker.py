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
Drag tracker for providing drag support to other trackers
"""

from ..support.smart_tuple import SmartTuple
from support.tuple_math import TupleMath
from support.singleton import Singleton

from ..coin.coin_group import CoinGroup
from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.coin_enums import Axis
from ..coin.coin_styles import CoinStyles as Styles

from ..coin import coin_math

from ..trait.base import Base
from ..trait.style import Style
from ..trait.event import Event
from ..trait.pick import Pick
from ..trait.geometry import Geometry

from ..trait.enums import DragStyle

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

        #build the full drag group graph
        self.drag.full = CoinGroup(is_switched=True, is_separated=True,
        parent=self.drag, name='drag_tracker_full')

        self.drag.full.transform = \
            self.drag.full.add_node(Nodes.TRANSFORM, 'transform')
        
        self.drag.full.group = self.drag.full.add_node(Nodes.GROUP, 'group')

        #build the partial drag group graph
        self.drag.part = CoinGroup(is_switched=True, is_separated=True,
        parent=self.drag, name='drag_tracker_part')

        self.drag.part.coordinate =\
            self.drag.part.add_node(Nodes.COORDINATE, 'coordinate')

        self.drag.part.line = self.drag.part.add_node(Nodes.LINE, 'line')

        self.drag.part.set_visibility()
        self.drag.full.set_visibility()

        self.drag.set_visibility()
        self.set_visibility()

        self.set_pick_style(False)
        self.partial_nodes = []
        self.partial_indices = {}

        self.add_mouse_event(self.drag_mouse_event)
        self.add_button_event(self.drag_button_event)

        self.dragging = False

        self.update_center_fn = lambda: print('update_center_fn')

        #initialize the drag line
        self.show_drag_line = True

        self.geometry.line = \
            self.geometry.add_node(Nodes.LINE_SET, 'drag line')

        self.coin_style = Styles.Style(
            'drag_line', Styles.DASHED, color=Styles.Color.BLUE)

        self.set_style()
        self.geometry.set_visibility(False)

        self.rotation_enabled = True
        self.translation_enabled = True

        self.lock_axis = ()

        self.local_mouse_callbacks = {}
        self.local_button_callbacks = {}

        #------------------------
        #drag rotation attributes
        #------------------------

        #cumulative rotation value
        self.rotation = 0.0

        #current bearing of user rotation
        self.angle = 0.0

        #drag center point defined by inheriting class
        self.drag_center = (0.0, 0.0, 0.0)

        self.drag_style = DragStyle.CURSOR

        self.is_rotating = False

        self.update([(0.0, 0.0, 0.0), (0.0, 0.0, 0.0)])

    def insert_full_drag(self, node):
        """
        Insert a graph to be fully transformed by dragging

        node - a coin3d group-type node containing drag geometry
        """

        self.drag.full.insert_node(node, self.drag.full.group)

    def insert_partial_drag(self, node, coordinates, index):
        """
        Insert a graph to be partially transformed by dragging

        coordinates - an Iterable of line endpoints as tuples
        index - the line endpoint (0 or 1) to be updated
        """

        _len = len(self.drag.part.coordinate.getValues())

        #add new coordiantes to end of the point SbMFVec3f
        for _i, _v in enumerate(coordinates):
            self.drag.part.coordinate.setset1Value(_len + _i, _v)

        _len = len(self.drag.numVertices.getValues())

        #add new vertex number to the NumVertices SbMFInt32
        self.drag.line.numVertices.set1Value(_len, 2)

    def set_drag_axis(self, axis):
        """
        Set the lock axis, ensuring it's unit length.
        """

        if axis:
            aixs = TupleMath.unit(axis)

        self.lock_axis = axis

    def drag_mouse_event(self, user_data, event_cb):
        """
        Drag mouse event callback
        """

        if not self.dragging:
            return

        _coords = [
            self.drag_center,
            self.mouse_state.world_position
        ]

        #update the transform
        if self.mouse_state.alt_down:
            self.rotate(_coords[0], _coords[1], self.mouse_state.shift_down)

        else:
            self.translate(_coords[0], _coords[1], self.mouse_state.shift_down)

        if self.show_drag_line and not self.geometry.is_visible():

            #update to prevent incorrect coordinates
            self.update([
                self.mouse_state.world_position,
                self.mouse_state.world_position
            ])

            self.geometry.set_visibility(True)

        for _cb in self.local_mouse_callbacks.values():
            _cb(user_data, event_cb)

        event_cb.setHandled()

    def drag_button_event(self, user_data, event_cb):
        """
        Drag button event callback
        """

        if self.mouse_state.button1.dragging:
            return

        #end of drag operation
        if self.dragging:

            self.drag.full.group.removeAllChildren()
            self.drag.part.group.removeAllChildren()

            self.geometry.set_visibility(False)

            self.drag.full.set_translation((0.0, 0.0, 0.0))
            self.drag.full.set_rotation(0.0)
            self.drag.part.line.numVertices.setValues(0, 1, (0))
            self.dragging = False

        #start of drag operation
        else:
            self.update([self.drag_center, self.drag_center])

        for _cb in self.local_button_callbacks.values():
            _cb(user_data, event_cb)

##########################
## Transformation routines
##########################

    def translate(self, start_coord, end_coord, micro):
        """
        Manage drag geometry translation
        """

        if not self.translation_enabled:
            return

        if self.is_rotating:

            self.is_rotating = False

            _xlate = self.drag.full.get_translation()
            _world_pos = SmartTuple._add(_xlate, self.drag_center)

            self.mouse_state.set_mouse_position(self.view_state, _world_pos)

            return

        #accumulate the movement from the previous mouse position
        _delta = SmartTuple._sub(end_coord, start_coord)

        if self.lock_axis:

            if self.lock_axis[0] == 1.0:
                _delta = (_delta[0], 0.0, 0.0)

            elif self.lock_axis[1] == 1.0:
                _delta = (0.0, _delta[1], 0.0)

            elif self.lock_axis[2] == 1.0:
                _delta = (0.0, 0.0, _deltas[2])

            else:
                _delta =\
                    TupleMath.project(_delta[1], self.lock_axis, True)

        self.drag.full.set_translation(_delta)

        if self.show_drag_line:
            self.update([start_coord, end_coord])

    def rotate(self, center_coord, radius_coord, micro):
        """
        Manage rotation during dragging
        coords - pair of coordinates for the rotation update in tuple form
        """

        if not self.rotation_enabled:
            return

        #if already rotating get the updated bearing from the center
        if self.is_rotating:

            _center = self.drag.full.get_center()
            _offset = self.drag.full.get_translation()

            _start = SmartTuple._add(_center, _offset)
            _vec = SmartTuple._sub(radius_coord, _start)

            _angle = coin_math.get_bearing(_vec)
            _delta = self.angle - _angle

            self.rotation += _delta
            self.angle = _angle

            if self.show_drag_line:
                self.update([_start, radius_coord])

        #otherwise, initiate rotation.  Set centerpoint according to values
        #defined by inheriting class
        else:

            self.drag.full.set_center(self.drag_center)
            self.rotation = 0.0
            self.is_rotating = True

        #update the +z axis rotation for the transformation
        self.drag.full.set_rotation (self.rotation, Axis.Z)

    def finish(self):
        """
        Cleanup
        """

        Base.finish(self)
        Style.finish(self)
        Event.finish(self)
        Pick.finish(self)
        Geometry.finish(self)

        self.drag.part.finalize()
        self.drag.full.finalize()
        self.drag.finalize()

        self.partial_nodes = []
        self.partial_indices = {}

        self.update_center_fn = None
        self.coin_style = None
        self.drag_center = None

        Singleton.finish(DragTracker)

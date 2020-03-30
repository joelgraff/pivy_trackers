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
Geometry tracker base class
"""

from ..support.tuple_math import TupleMath

from ..coin import coin_utils

from ..coin.todo import todo
from ..trait.base import Base
from ..trait.message import Message
from ..trait.style import Style
from ..trait.event import Event
from ..trait.pick import Pick
from ..trait.select import Select
from ..trait.drag import Drag
from ..trait.geometry import Geometry
from ..trait.keyboard import Keyboard

from ..trait import enums

from ..coin.coin_styles import CoinStyles

class GeometryTracker(
    Base, Message, Style, Geometry, Event, Keyboard, Pick, Select, Drag):

    """
    Geometry tracker base class
    """

    #static alias for DragStyle class
    DragStyle = enums.DragStyle

    def __init__(self, name, parent, view=None):
        """
        Constructor
        """

        super().__init__(name=name, parent=parent, view=view)

        self.linked_geometry = {}
        self.coin_style = CoinStyles.DEFAULT

        self.last_matrix = None

    def link_geometry(self, target, source_idx, target_idx, target_only=False):
        """
        Link another geometry to the line for automatic updates

        target - reference to geometry to be linked
        source_idx - index updated by target geometry
        target_idx - index updated by this geometry
        target_only - if True, source is not updated by changes in target
        index values = 0 to max # of vertices in target line
        index value = -1 = all indices are updated
        """

        _target_key = (target, target_idx)
        _source_key = (self, source_idx)

        if  _target_key not in self.linked_geometry:

            #register the line and geometry with each other
            #self.register_geometry(target, True)
            self.linked_geometry[_target_key] = []

        self.linked_geometry[_target_key].append(source_idx)

        if _source_key not in target.linked_geometry:
            target.linked_geometry[_source_key] = []

        target.linked_geometry[_source_key].append(target_idx)

    def add_node_events(self, node=None, pathed=True):
        """
        Set up node events for the passed node
        """

        #events are added to the last-added event callback node
        self.add_select_events()
        self.add_drag_events()
        #self.add_keyboard_events()

        if pathed:

            assert(node is not None), """pivy_trackers::GeometryTracker.add_node_events() - Node is NoneType.  Cannot apply event path"""

            self.pathed_cb_nodes[-1].path_node = node

    def reset(self):
        """
        Reset the coordinates and transform
        """

        super().reset()
        self.geometry.set_rotation(0.0, (0.0, 0.0, 0.0))
        self.geometry.set_translation((0.0, 0.0, 0.0))

    def before_drag(self, user_data):
        """
        Start of drag operations
        """

        super().before_drag(user_data)

    def on_drag(self, user_data):
        """
        During drag operations
        """

        super().on_drag(user_data)

    def after_drag(self, user_data):
        """
        End-of-drag operations
        """

        todo.delay(
            self._after_drag_update,
            Drag.drag_tracker.get_matrix()
        )

        super().after_drag(user_data)

    def _after_drag_update(self, user_data):
        """
        Delayed update callback to allow for scene traversals to complete
        """

        print(self.name, '_after_drag_update...', user_data.getValue())
        self.linked_update(None, user_data)

    def linked_update(self, parent, matrix):
        """
        Takes a list of indices and a transformation matrix to update
        object coordiantes, as well as trigger updates for it's own objects
        """

        #avoid looping updates
        if matrix is self.last_matrix:
            return

        self.last_matrix = matrix

        #get the coordinates as a list of 3-tuples
        _coords = [_v.getValue()
            for _v in self.geometry.coordinate.point.getValues()]

        _indices = list(range(0, len(_coords)))

        #get the point that is linked to other dragged geometry
        if parent is not None:

            _indices = self.linked_geometry[parent]

            if not _indices:
                return

        _xf_coords = []

        print('\n\t{}.linked_update: {}'.format(self.name, str(_indices)))

        #iterate through the linked indices and add them to the list
        #of coordinates to transform
        for _idx in _indices:

            if _idx == -1:
                _xf_coords = _coords
                break

            _xf_coords.append(_coords[_idx])

        print('\tcoordinates:',str(_xf_coords))

        #transform the linked point by the drag transformation
        _xf_coords = \
            self.view_state.transform_points(_xf_coords, matrix)

        print('\ttransforms:',str(_xf_coords))

        #update the coordinate list with the transformed coordinates
        for _i, _idx in enumerate(_indices):

            if _idx == -1:
                _coords = _xf_coords
                break

            _coords[_idx] = _xf_coords[_i]

        #trigger linked updates for other geometry
        for _v in self.linked_geometry:

            #don't update the parent triggering the update
            if _v == parent:
                continue

            print('\t\tupdate linked geometry {}'.format(_v[0].name))
            _w = self.linked_geometry[_v]

            #if any of the indices in the linked geometry are the indices
            #being updated in the current geometry, then trigger the linked geo.
            if any([_x in _indices for _x in _w]):
                _v[0].linked_update(self, matrix)

        self.update(_coords, notify=False)

    def update(self, coordinates, notify=True):
        """
        Override of Geometry method to provide messaging support
        """

        if not coordinates:
            return

        _c = coordinates

        if not isinstance(_c, list):
            _c = [_c]

        is_unique = len(self.prev_coordinates) != len(_c)

        if not is_unique:

            for _i, _v in enumerate(self.prev_coordinates):

                if _v != _c[_i]:
                    is_unique = True
                    break

        if not is_unique:
            return

        super().update(coordinates)

        self.coordinates = coordinates

        if not notify:
            return

        if not isinstance(coordinates, list):
            coordinates = [coordinates]

        #self.dispatch_geometry(coordinates)

    def notify_geometry(self, event, message):
        """
        Override of Message method to provide geometry update support
        """

        super().notify_geometry(event, message)

    def finish(self):

        Base.finish(self)
        Message.finish(self)
        Style.finish(self)
        Geometry.finish(self)
        Event.finish(self)
        Pick.finish(self)
        Select.finish(self)
        Drag.finish(self)

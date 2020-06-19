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

from collections.abc import Iterable

from freecad_python_support.tuple_math import TupleMath

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

    def __init__(self, name, parent, is_geo=False, view=None):
        """
        Constructor
        """

        Geometry.init_graph(is_geo=is_geo)

        super().__init__(name=name, parent=parent, view=view)

        self.coin_style = CoinStyles.DEFAULT
        self.is_draggable = True
        self._setting_up_linked_drag = False

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

        if not isinstance(target_idx, Iterable):
            target_idx = [target_idx]

        self._link_geometry(self, target, source_idx, target_idx)

        if not target_only:

            for _v in target_idx:

                #cannot reverse link for full-transformed geometries
                if _v == -1:
                    continue

                #-1 indicates the entire geometry is linked by transform
                self._link_geometry(target, self, _v, [source_idx])

    def _link_geometry(self, source, target, s_idx, t_idx):
        """
        Worker function for self.link_geometry

        source - the object which triggers an update in the target
        target - the object which is updated
        s_idx - the index of the source coordinate triggering the update
        t_idx - list of the index or indices of the target coordinate to update
        """

        #add the source to the target's linked_geometry dict
        #and set up the index dict
        if source not in target.linked_geometry:

            _dict = {}
            target.linked_geometry[source] = _dict

        if not source in source.linked_geometry:
            source.linked_geometry[source] = []

        if not target in source.linked_geometry[source]:
            source.linked_geometry[source].append(target)

        #retrieve the existing index dict
        else:
            _dict = target.linked_geometry[source]

        #if the source index is not already in the dict, add it with the target
        if s_idx not in _dict:
            _dict[s_idx] = []

        _dict[s_idx] += t_idx

    def setup_linked_drag(self, parent=None):
        """
        Set up all linked geometry for a drag oepration
        """

        #abort nested calls
        if self._setting_up_linked_drag:
            return

        #abort call with no parent link
        if parent and (parent not in self.linked_geometry):
            return

        #add to drag list if not previously added
        if not self in Drag.drag_list and self.is_draggable:
            self.drag_copy = self.geometry.copy()
            Drag.drag_list.append(self)

        _indices = []

        #if parent exists and object is not selected, get partial drag indices
        if parent and self not in Select.selected:

            _idx = parent.drag_indices
            _p_idx = self.linked_geometry[parent]

            for _i in _idx:
                if _i in _p_idx:
                    self.drag_indices += _p_idx[_i]

        #otherwise, assume fully-dragged
        else:

            self.is_full_drag = True
            self.drag_indices = list(range(0, len(self.coordinates)))

        #if no dragging occurs, stop here
        if not self.drag_indices:
            return

        if not self in self.linked_geometry:
            return

        self._setting_up_linked_drag = True

        #call linked geometry to set up dragging based on passed indices
        for _v in self.linked_geometry[self]:
            _v.setup_linked_drag(self)

        self._setting_up_linked_drag = False

    def add_node_events(self, node=None, pathed=True):
        """
        Set up node events for the passed node
        """

        #events are added to the last-added event callback node
        self.add_select_events()
        self.add_drag_events()
        self.add_keyboard_events()

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

        self.setup_linked_drag()

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
        #self.view_state.dump()
        todo.delay(self._after_drag, Drag.drag_tracker.get_matrix())
        super().after_drag(user_data)

    def _after_drag(self, matrix):
        """
        Proxy function to handle delayed calls
        """

        self.update(matrix=matrix)

    def update(self, coordinates, matrix=None, notify = False):
        """
        Override of geometry.update()
        """

        super().update(coordinates, matrix)

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

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
Drag traits for Tracker objects
"""

import signal, traceback

from collections.abc import Iterable

from ..coin.todo import todo
from ..coin import coin_utils
from types import SimpleNamespace

from ..trait.select import Select
from ..tracker.drag_tracker import DragTracker

class Drag():
    """
    Drag traits for tracker classes
    """

    #prototypes from Base, Select, Event, and Geometry
    base = None
    name = ''
    mouse_state = None
    view_state = None
    select = None
    coordinates = None

    def set_event_path(self, callback, is_pathed=True): """prototype"""
    def is_selected(self): """prototype"""

    #prototype to be implemented by inheriting class
    def update_drag_center(self): """prototype"""

    #default lambda for place-holder functions
    #returns tuple of passed parameters
    default_fn = lambda _self, _x:\
        lambda _u_d, _n=_self.name, _m=_x: (_u_d, _n, _m)

    #Class static reference to global DragTracker
    drag_tracker = None

    def __init__(self):
        """
        Constructor
        """

        assert(self.select is not None), \
            """
            Select must precede Drag in method resolution order
            """

        # instances / initializes singleton DragTracker on first inherit,
        # and adds callback for global tracker updating
        if not Drag.drag_tracker:
            Drag.drag_tracker = DragTracker(self.root)
            Drag.drag_tracker.update_center_fn = self.update_drag_center

        self.handle_drag_events = True
        self.drag_copy = None
        self.is_dragging = False
        self.is_full_drag = False
        self.partial_drag_index = -1

        self.drag_mouse_cb = None
        self.drag_button_cb = None

        #localized callback lists that are cleared at the end of
        #every drag operation
        self.on_drag_local_cb = []
        self.before_drag_local_cb = []
        self.after_drag_local_cb = []

        #system-wide callbacks that persist across drag oeprations
        self.before_drag_callbacks = []
        self.on_drag_callbacks = []
        self.after_drag_callbacks = []

        super().__init__()

    def get_drag_matrix(self):
        """
        Return a copy of the drag tracker transformation matrix
        """

        return Drag.drag_tracker.get_matrix()

    def get_drag_coordinates(self):
        """
        Transform the object coordinates by the drag tracker matrix
        """

        if self.coordinates is None:
            return None

        _c = self.coordinates

        if not self.is_full_drag:

            print('self.partial_drag_index', self.partial_drag_index)
            if self.partial_drag_index == -1:
                return None

            print(_c[self.partial_drag_index])
            _c = [_c[self.partial_drag_index]]


        _c = self.view_state.transform_points(
            _c, Drag.drag_tracker.get_matrix())

        if not self.is_full_drag:
            _coords = self.coordinates[:]
            _coords[self.partial_drag_index] = _c[0]

        else:
            _coords = _c

        return _coords

    def set_translate_increment(self, increment = 0.0):
        """
        Set the increment of translation - 0.0 = free translation
        """

        Drag.drag_tracker.translate_increment = increment

    def set_rotate_increment(self, increment = 0.0):
        """
        Set the increment of rotation in radians - 0.0 = free rotation
        """

        Drag.drag_tracker.rotate_increment = increment

    def add_drag_events(self):
        """
        Add drag events to the coin graph
        """

        self.drag_mouse_cb = self.add_mouse_event(self.drag_mouse_event)
        self.drag_button_cb = self.add_button_event(self.drag_button_event)

    def enable_drag_translation(self):
        """
        Enable drag translation
        """

        Drag.drag_tracker.translation_enabled = True

    def disable_drag_translation(self):
        """
        Disable drag translation
        """

        Drag.drag_tracker.translation_enabled = False

    def enable_drag_rotation(self):
        """
        Enable drag rotation
        """

        Drag.drag_tracker.rotation_enabled = True

    def disable_drag_rotation(self):
        """
        Disable drag rotation
        """

        Drag.drag_tracker.rotation_enabled = False

    def set_drag_axis(self, axis=None):
        """
        Set the axis along which dragging is constrained
        """

        Drag.drag_tracker.set_drag_axis(axis)

    def drag_mouse_event(self, user_data, event_cb):
        """
        Coin-level drag mouse event callback
        """

        if self.handle_drag_events or self.handle_events:
            event_cb.setHandled()

        self.on_drag(user_data)

    def drag_button_event(self, user_data, event_cb):
        """
        Coin-level drag button event callback
        """

        if self.handle_drag_events or self.handle_events:
            event_cb.setHandled()

        if not self.is_selected:
            return

        #conflicting / undefined state, abort
        if self.mouse_state.button1.dragging:
            return

        #end of drag operations
        if self.is_dragging:

            #re-enable selective pathing
            self.set_event_path(self.drag_mouse_cb, True)
            self.set_event_path(self.drag_button_cb, True)
            self.is_dragging = False

            self.after_drag(self)

            self.drag_tracker.end_drag()
            todo.delay(self.teardown_drag, None)

        #start of drag operations
        else:

            #set the event path to none to enable constant drag
            self.set_event_path(self.drag_mouse_cb, False)
            self.set_event_path(self.drag_button_cb, False)
            self.is_dragging = True

            self.before_drag(user_data)

            todo.delay(self.setup_drag, None)

    def _setup_drag(self, source, source_indices):
        """
        Setup dragging worker function
        linked_geometry:
            key - target objects or self
            item - dict
                key - source index
                item - list of target indices
        """

        #iterate linked targets for this geometry
        for _k, _v in source.linked_geometry.items():

            _k.drag_copy = _k.geometry.copy()

            if _k is self:
                continue

            print (self.name,_v)

            #iterate target indices keyed to source index
            for _l, _w in _v.items():

                if _l not in source_indices:
                    continue

                for _x in _w:
                    _offsets = [_x + _y for _y in [-1, 0, 1]]

                    if _offsets[-1] == len(_k.coordinates):
                        _offsets[-1] = -1

                    print('{}:{} insert partial drag'.format(self.name, _k.name))
                    self.drag_tracker.insert_partial_drag(
                        _k.geometry.top, _offsets)

                    #set up the text drag
                    if _k.text_nodes:

                        _text_group = _k.drag_copy.getChild(3)

                        if _text_group:
                            print('{}:{} insert full drag'.format(self.name, _k.name))
                            self.drag_tracker.insert_full_drag(_text_group)

    def setup_drag(self):
        """
        Setup dragging at start of drag ops
        """

        #enabling sinks mouse events at the drag tracker
        Drag.drag_tracker.drag_center = self.update_drag_center()

        for _v in Select.selected:

            _v.ignore_notify = True
            _v.is_full_drag = True

            _v.drag_copy = _v.geometry.copy()
            Drag.drag_tracker.insert_full_drag(_v.drag_copy)

            self._setup_drag(_v, list(range(0, len(_v.coordinates))))

        self.drag_tracker.begin_drag()

        return

    def before_drag(self, user_data):
        """
        Called before drag operations begin
        """

        for _cb in self.before_drag_callbacks + self.before_drag_local_cb:
            _cb(user_data)

    def on_drag(self, user_data):
        """
        Called during drag operations
        """

        if not self.is_dragging:
            return

        for _cb in self.on_drag_callbacks + self.on_drag_local_cb:
            _cb(user_data)

        self.drag_tracker.update_drag()

    def after_drag(self, user_data):
        """
        Called at end of drag operations
        """

        print(self.name, 'Drag.after_drag()')
        for _cb in self.after_drag_callbacks + self.after_drag_local_cb:
            _cb(user_data)

    def teardown_drag(self):
        """
        Called after end of drag operations
        """

        self.before_drag_local_cb = []
        self.on_drag_local_cb = []
        self.after_drag_local_cb = []

        self.drag_copy = None
        self.is_full_drag = False
        self.is_dragging = False

    def finish(self):
        """
        Cleanup
        """

        if not Drag.drag_tracker:
            return

        Drag.drag_tracker.finish()
        Drag.drag_tracker = None

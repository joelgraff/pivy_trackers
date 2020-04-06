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
        self.drag_indices = []
        self._is_setting_up = False

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

        if  not self.coordinates:
            return None

        if not self.drag_indices:
            return None

        #get coordinates being dragged
        _c = [self.coordinates[_v] for _v in self.drag_indices]

        #transform them according to the drag tracker's matrix
        _c = self.view_state.transform_points(
            _c, Drag.drag_tracker.get_matrix())

        _coords = []

        #update the coordinate list with the transformations
        if len(self.coordinates) == len(_c):
            _coords = _c

        else:

            _coords = self.coordinates[:]

            for _i, _v in enumerate(self.drag_indices):
                _coords[_v] = _c[_i]

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

    def _setup_drag(self, drag_list, parent=None):
        """
        """

        #abort nested calls
        if self._is_setting_up:
            return

        #abort call with no parent link
        if parent and (parent not in self.linked_geometry):
            return

        print('{}._setup_drag()'.format(self.name), self.drag_indices)

        #add to drag list if not previously added
        if not self in drag_list:
            self.drag_copy = self.geometry.copy()
            drag_list.append(self)

        _indices = []

        #get parent drag indices, otherwise assume full drag
        if parent:

            _idx = parent.drag_indices
            _p_idx = self.linked_geometry[parent]

            for _i in _idx:
                if _i in _p_idx:
                    self.drag_indices += _p_idx[_i]

            print(_idx, _p_idx)

        else:

            self.is_full_drag = True
            self.drag_indices = list(range(0, len(self.coordinates)))

        print(self.name, self.drag_indices)
        #call geometry linked to this object
        self._is_setting_up = True

        #call linked geometry to set up dragging based on passed indices
        for _v in self.linked_geometry[self]:
            _v._setup_drag(drag_list, self)

        self._is_setting_up = False

        print(self.name, 'setup_drag complete')
    def setup_drag(self):
        """
        Setup dragging at start of drag ops
        """

        #enabling sinks mouse events at the drag tracker
        Drag.drag_tracker.drag_center = self.update_drag_center()

        drag_list = []

        for _v in Select.selected:

            _v.ignore_notify = True
            self._setup_drag(drag_list)

        for _v in drag_list:

            #remove duplicates
            _v.drag_indices = list(set(_v.drag_indices))

            print('{}.setup_drag: {}'.format(_v.name, str(_v.drag_indices)))
            #if all the coordinate indices are added, switch to full drag
            if len(_v.drag_indices) == len(_v.coordinates):
                _v.is_full_drag = True

            if _v.is_full_drag:

                print('\tFULL DRAG FOR', _v.name)
                Drag.drag_tracker.insert_full_drag(_v.drag_copy)
                continue

            if not _v.drag_indices:
                continue

            #get the starting and ending points of the range
            _idx_range = [_v.drag_indices[0] - 1, _v.drag_indices[-1] + 1]

            #adjust points to ensure they are valid list indices
            if _idx_range[0] < 0:
                _idx_range[0] = 0

            if _idx_range[1] >= len(_v.coordinates):
                _idx_range[1] = len(_v.coordinates) - 1

            print('\n\tPARTIAL DRAG FOR', _v.name, _idx_range, _v.drag_indices)
            self.drag_tracker.insert_partial_drag(
                _v.geometry.top, _idx_range, _v.drag_indices)

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

        #abort if no drag copy to prevent recursion
        if not self.drag_copy:
            return

        self.before_drag_local_cb = []
        self.on_drag_local_cb = []
        self.after_drag_local_cb = []
        self.drag_indices = []
        self._has_setup = False

        self.drag_copy = None
        self.is_full_drag = False
        self.is_dragging = False

        for _k in self.linked_geometry[self]:
            _k.teardown_drag()

    def finish(self):
        """
        Cleanup
        """

        if not Drag.drag_tracker:
            return

        Drag.drag_tracker.finish()
        Drag.drag_tracker = None

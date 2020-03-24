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

        print('get_drag_coordinates')
        print('self.coordinates',self.coordinates)

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

            self.after_drag(user_data)

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

    def setup_drag(self):
        """
        Setup dragging at start of drag ops
        """

        #enabling sinks mouse events at the drag tracker
        Drag.drag_tracker.drag_center = self.update_drag_center()

        for _v in Select.selected:

            _v.ignore_notify = True
            _v.drag_copy = _v.geometry.copy()
            _v.is_full_drag = True

            Drag.drag_tracker.insert_full_drag(_v.drag_copy)

            #iterate through linked geometry for partial dragging
            for _k in _v.linked_geometry:

                print ('\t-------> ',_k.name)

                if self not in _k.linked_geometry:
                    continue

                _k.drag_copy = _k.geometry.copy()

                _idx = _k.linked_geometry[self]

                print ('partial index', _idx)

                _k.partial_drag_index = _idx[0]

                if _idx == -1:
                    continue

                #picked coordinate is always middle index
                #if picked is first or last coordinate,
                #previous / next index == -1
                _c = [_idx[0] + _v for _v in [-1, 0, 1]]

                if _c[-1] == len(_k.coordinates):
                    _c[-1] = -1

                #set drag callbacks which are removed at end of drag ops
                self.before_drag_local_cb.append(_k.before_drag)
                self.after_drag_local_cb.append(_k.after_drag)

                self.drag_tracker.insert_partial_drag(_k.geometry.top, _c)

                #set up the text drag
                if _k.text_nodes:
                    _text_group = _k.drag_copy.getChild(3)
                    self.drag_tracker.insert_full_drag(_text_group)

        print('Drag.setup_drag() - begin dragtracker')
        self.drag_tracker.begin_drag()

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

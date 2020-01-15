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

from ..trait.select import Select

from ..tracker.drag_tracker import DragTracker

class Drag():
    """
    Drag traits for tracker classes
    """

    #prototypes from Base, Select, and Event
    base = None
    name = ''
    mouse_state = None
    view_state = None
    select = None

    def set_event_path(self, callback, is_pathed=True): """prototype"""
    def is_selected(self): """prototype"""
    #def add_mouse_event(self, callback): """prototype"""; pass
    #def add_button_event(self, callback): """prototype"""; pass

    #prototype to be implemented by inheriting class
    def update_drag_center(self): """prototype"""

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

        self.drag_mouse_cb = None
        self.drag_button_cb = None

        super().__init__()

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

    def on_drag(self, user_data, event_cb):
        """
        On drag callback, called during drag operations
        """

        self.drag_tracker.update_drag()

    def drag_mouse_event(self, user_data, event_cb):
        """
        Coin-level mouse event callback
        """

        if self.handle_drag_events or self.handle_events:
            event_cb.setHandled()

        if not self.is_dragging:
            return

        self.on_drag(user_data, event_cb)

    def drag_button_event(self, user_data, event_cb):
        """
        Coin-level button event callback
        """

        if self.handle_drag_events or self.handle_events:
            event_cb.setHandled()
        
        if not self.is_selected:
            return

        #conflicting / undefined state, abort
        if self.mouse_state.button1.dragging:
            return

        if self.is_dragging:

            self.set_event_path(self.drag_mouse_cb, True)
            self.set_event_path(self.drag_button_cb, True)
            self.is_dragging = False

            self.drag_tracker.end_drag()

        else:

            self.before_drag(user_data, event_cb)

            self.set_event_path(self.drag_mouse_cb, False)
            self.set_event_path(self.drag_button_cb, False)
            self.is_dragging = True

            self.drag_tracker.start_drag()

    def before_drag(self, user_data, event_cb):
        """
        Before drag callback, called at start of drag operations
        """

        #enabling sinks mouse events at the drag tracker
        Drag.drag_tracker.drag_center = self.update_drag_center()

        for _v in Select.selected:

            _v.ignore_notify = True
            _v.drag_copy = _v.geometry.copy()
            Drag.drag_tracker.insert_full_drag(_v.drag_copy)

            #iterate through linked geometry for partial dragging
            for _k in _v.linked_geometry:

                if self not in _k.linked_geometry:
                    continue

                _k.drag_copy = _k.geometry.copy()
                _idx = _k.linked_geometry[self]
                _coords = []
                _len = len(_k.coordinates)

                #get the first two coordinates
                if _idx[0] == 0:
                    _coords = _k.coordinates[:2]

                #get the last two coordinates
                elif _idx[0] == _len - 1:
                    _coords = _k.coordinates[-2:]

                #more than two coordinates.
                #get the coordinate on either side of the index
                else:
                    _start = _idx[0] - 1
                    _coords = _k.coordinates[_start:_start + 3]

                self.drag_tracker.\
                    insert_partial_drag(_k.drag_copy, _coords, _idx[0])

    def after_drag(self, user_data, event_cb):
        """
        Called at end of drag operations
        """

        #iterate selected elements, transforming points and updating,
        #triggering notifications to linked trackers, if any
        for _v in Select.selected:

            if not _v.drag_copy:
                continue

            _points = self.view_state.transform_points(
                _v.get_coordinates(), _v.drag_copy.getChild(1))

            _v.update(_points)
            _v.drag_copy = None

        #re-enable notifications only after drag updates are complete
        for _v in Select.selected:
            _v.ignore_notify = False

    def finish(self):
        """
        Cleanup
        """

        if not Drag.drag_tracker:
            return

        Drag.drag_tracker.finish()
        Drag.drag_tracker = None

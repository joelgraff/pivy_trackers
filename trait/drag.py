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
    select = None

    def is_selected(self): """prototype"""; pass
    def add_mouse_event(self, callback): """prototype"""; pass
    def add_button_event(self, callback): """prototype"""; pass

    #Class static reference to global DragTracker
    tracker = None

    def __init__(self):
        """
        Constructor
        """

        assert(self.select is not None), \
            """
            Select must precede Drag in method resolution order
            """

        #instances singleton DragTracker on first inherit
        if not Drag.tracker:
            Drag.tracker = DragTracker(self.base)

        self.add_mouse_event(self.drag_mouse_event)
        #self.add_button_event(self.drag_button_event)

        super().__init__()

    def drag_mouse_event(self, user_data, event_cb):
        """
        Drag mouse movement event callback
        """

        if not self.is_selected() or not self.mouse_state.button1.dragging:
            return

        Drag.tracker.insert_full_drag(self.base.copy())

#    def select_button_event(self, user_data, event_cb):
#        """
#        Select event override
#        """

#        Select.select_button_event(self, user_data, event_cb)


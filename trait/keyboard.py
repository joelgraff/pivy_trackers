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
Provides SoKeyboardEvent support for tracker classes
"""

from pivy import coin

from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.coin_enums import Keys

class Keyboard():
    """
    Provides SoKeyboardEvent support for tracker classes
    """

    #Base prototypes
    name = None
    names = []
    base = None

    def __init__(self):
        """
        Constructor
        """
        #Pylint doesn't see self.base members...
        #pylint: disable=no-member

        assert(self.names), """
        Keyboard.__init__(): No names defined.  Is Base inherited?
        """

        assert(self.event), """
        Keyboard.__init__(): No event node defined.  Is Event inherited?
        """

        self.handle_keyboard_events = False
        self.keybaord_event_cb = None
        self.keydown_callbacks = {}
        self.keyup_callbacks = {}

        super().__init__()

    def add_keyboard_events(self):
        """
        Add the event callback to the coin graph for trapping key presses
        """

        self.keyboard_event_cb = self.add_keyboard_event(self.keyboard_event)

    def set_keypress_callback(self, keys, callback, is_keydown=False):
        """
        Set a callback for a specific key or list of keys on key down
        """

        _dict = self.keyup_callbacks

        if is_keydown:
            _dict = self.keydown_callbacks

        if not isinstance(keys, list):
            keys = [keys]

        for _key in keys:

            if not _key in _dict:
                _dict[_key] = []

            _dict[_key].append(callback)

    def keyboard_event(self, user_data, event_cb):
        """
        Keyboard event callback
        """

        _evt = event_cb.getEvent()

        if self.handle_keyboard_events or self.handle_events:
            event_cb.setHandled()

        is_keydown = _evt.isKeyPressEvent(_evt, Keys.ANY)

        self.on_key_press(_evt.getKey(), is_keydown)

    def on_key_press(self, key, is_keydown):
        """
        Base event callback class

        Callback signature: my_callback(object, key)
        """

        _dict = self.keyup_callbacks

        if is_keydown:
            _dict = self.keydown_callbacks

        if not key in _dict:
            return

        for _cb in _dict[key]:
            _cb(self, key)

    def finish(self):
        """
        Cleanup
        """

        self.keyboard = None

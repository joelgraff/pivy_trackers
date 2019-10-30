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
Event class for Tracker objects
"""
import weakref

from ..support.smart_tuple import SmartTuple

from ..coin.coin_group import CoinGroup
from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.coin_enums import MouseEvents as MouseEvents
from ..coin import coin_utils

class Event():
    """
    Event Callback traits.
    """

    #Base prototypes
    base = None
    view_state = None
    mouse_state = None
    name = ''

    _self_weak_list = []
    _default_callback_node = None

    @staticmethod
    def set_paths():
        """
        Static class method for setting paths on registered callbacks after
        scene insertion.
        """

        for _v in Event._self_weak_list:
            _v().set_event_paths()

    is_switched = None
    is_separated = None
    switch_first = None

    @staticmethod
    def init_graph(is_switched=True, is_separated=False, switch_first=True):
        Event.is_switched = is_switched
        Event.is_separated = is_separated
        Event.switch_first = switch_first

    def __init__(self):
        """
        Constructor
        """

        self.event = CoinGroup(
            switch_first=Event.switch_first,
            is_separated=Event.is_separated,
            is_switched=Event.is_switched,
            parent=self.base, name=self.name + '__EVENTS')

        self.event.callbacks = []
        self.callbacks = []

        self.path_nodes = []

        self.handle_events = False

        #create a global callback for managing mouse updates
        if not Event._default_callback_node:

            self.add_mouse_event(self._event_mouse_event)
            self.add_button_event(self._event_button_event)
            Event._default_callback_node = self.event.callbacks[0]

        self.event.set_visibility(True)

        Event._self_weak_list.append(weakref.ref(self))

        Event.init_graph()

        super().__init__()

    def _event_mouse_event(self, data, event_cb):
        """
        Default mouse location event
        """

        self.mouse_state.update(event_cb, self.view_state)

        if not (self.mouse_state.shift_down and \
            self.mouse_state.button1.dragging):

            return

        _vec = SmartTuple._scl(self.mouse_state.vector, 0.10)
        _pos = SmartTuple._add(self.mouse_state.prev_position, _vec)
        self.mouse_state.set_mouse_position(self.view_state, _pos)

    def _event_button_event(self, data, event_cb):
        """
        Default button event
        """

        self.mouse_state.update(event_cb, self.view_state)

    def add_event_callback_node(self):
        """
        Add an event callback node to the current group
        """

        self.event.callbacks.append(
            self.event.add_node(Nodes.EVENT_CB, 'EVENT_CALLBACK')
        )

        self.callbacks.append({})

    def remove_event_callback_node(self, index):
        """
        Remove an event callback node from the current group
        """

        node = self.event.callbacks[index]

        if node not in self.event.callbacks:
            return

        self.event.remove_node(node)

        del self.event.callbacks[index]
        del self.callbacks[index]

    def set_event_paths(self):
        """
        Set the specified path on the event callback at the specified index
        """

        if not self.path_nodes:
            return

        _path_nodes = self.path_nodes[:]

        _len_cb = len(self.event.callbacks)
        _len_pn = len(self.path_nodes)

        #if too few path nodes exist, pad the path_nodes list with the last
        #element.
        if _len_cb > _len_pn:
            _path_nodes += [_path_nodes[-1]]*(_len_cb - _len_pn)

        for _i, _node in enumerate(self.callbacks):

            _node = _path_nodes[_i]
            _sa = coin_utils.search(_node, self.view_state.sg_root)

            self.event.callbacks[_i].setPath(_sa.getPath())

    def add_event_callback(self, event_type, callback, index=-1):
        """
        Add an event callback
        """

        #if none exist, add a new one
        #otherwise default behavior reuses last-created SoEventCb node
        if not self.event.callbacks:
            self.add_event_callback_node()

        _et = event_type.getName().getString()

        if not _et in self.callbacks:
            self.callbacks[index][_et] = {}

        _cbs = self.callbacks[index][_et]

        if callback in _cbs:
            return

        _cbs[callback] = \
            self.event.callbacks[index].addEventCallback(event_type, callback)

    def remove_event_callback(self, event_type, callback, index=-1):
        """
        Remove an event callback
        """

        _et = event_type.getName().getString()

        if _et not in self.callbacks:
            return

        _cbs = self.callbacks[index][_et]

        if callback not in _cbs:
            return

        self.event.callbacks[index].removeEventCallback(
            event_type, _cbs[callback])

        del _cbs[callback]

        if not _cbs:
            self.remove_event_callback_node(index)

    def add_mouse_event(self, callback):
        """
        Convenience function
        """

        self.add_event_callback(MouseEvents.LOCATION2, callback)

    def add_button_event(self, callback):
        """
        Convenience function
        """

        self.add_event_callback(MouseEvents.MOUSE_BUTTON, callback)

    def remove_mouse_event(self, callback):
        """
        Convenience function
        """

        self.remove_event_callback(MouseEvents.LOCATION2, callback)

    def remove_button_event(self, callback):
        """
        Convenience function
        """

        self.remove_event_callback(MouseEvents.MOUSE_BUTTON, callback)

    def events_enabled(self):
        """
        Returns whether or not event switch is on
        """

        return self.event.whichChild == 0

    def toggle_event_callbacks(self):
        """
        Switch event callbacks on / off
        """
        #PyLint doesn't detect getValue()
        #pylint: disable=no-member

        if self.event.whichChild.getValue() == 0:
            self.event.whichChild = -1

        else:
            self.event.whichChild = 0

Event.init_graph()

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
Event class for Tracker objects
"""
import weakref
from types import SimpleNamespace

from pivy_trackers import TupleMath

from ..coin.coin_group import CoinGroup
from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.coin_enums import InputEvent as InputEvent
from ..coin.coin_enums import Keys
from ..coin import coin_utils
from ..coin.todo import todo

class Event():
    """
    Event Callback traits.
    """

    #Base prototypes
    base = None
    view_state = None
    mouse_state = None
    name = ''

    #class statics
    _self_weak_list = {}
    global_cb_node = None

    @staticmethod
    def set_paths():
        """
        Static class method for setting paths on registered callbacks after
        scene insertion.
        """

        for _v in Event._self_weak_list.values():
            _v().set_event_paths()

    is_switched = None
    is_separated = None
    switch_first = None

    @staticmethod
    def init_graph(is_switched=True, is_separated=False, switch_first=True):
        Event.is_switched = is_switched
        Event.is_separated = is_separated
        Event.switch_first = switch_first

    @staticmethod
    def callback_container(node=None, callback=None, event_type=None):
        """
        Create a callback container for event callbacks
        """

        return types.SimpleNamespace(
            callback=callback,
            type=event_type
        )

    def __init__(self):
        """
        Constructor
        """

        self.event = CoinGroup(
            switch_first=Event.switch_first,
            is_separated=Event.is_separated,
            is_switched=Event.is_switched,
            parent=self.base, name=self.name + '__EVENTS')

        self.pathed_switch = self.event.add_node(Nodes.SWITCH, 'PATH_SWITCH')
        self.local_switch = self.event.add_node(Nodes.SWITCH, 'LOCAL_SWITCH')

        self.pathed_cb_nodes = [SimpleNamespace(
                cb_node=coin_utils.add_child(
                    Nodes.EVENT_CB,
                    self.pathed_switch,
                    self.name + '_PATHED_CB_NODE'),
                path_node=None,
                callbacks=[]
            )]

        self.local_cb_node = coin_utils.add_child(
            Nodes.EVENT_CB, self.local_switch, 'LOCAL_CB_NODE')

        self.handle_events = False

        #create a global callback for managing mouse updates
        if not Event.global_cb_node:

            self.add_mouse_event(self._event_mouse_event)
            self.add_button_event(self._event_button_event)

            Event.global_cb_node =\
                self.event.add_node(Nodes.EVENT_CB, 'GLOBAL_EVENT_CALLBACK')

        self.event.set_visibility(True)

        Event._self_weak_list[self] = weakref.ref(self)
        Event.init_graph()

        self.toggle_pathed_event_callbacks()
        self.toggle_local_event_callbacks()

        super().__init__()

    def _event_mouse_event(self, data, event_cb):
        """
        Default mouse location event
        """

        self.mouse_state.update(event_cb, self.view_state)

        if not (self.mouse_state.shift_down and \
            self.mouse_state.button1.dragging):

            return

        _vec = TupleMath.scale(self.mouse_state.vector, 0.10)
        _pos = TupleMath.add(self.mouse_state.prev_position, _vec)

        self.mouse_state.set_mouse_position(self.view_state, _pos)

    def _event_button_event(self, data, event_cb):
        """
        Default button event
        """

        self.mouse_state.update(event_cb, self.view_state)

    def set_event_paths(self):
        """
        Set paths on every callback node that has a path
        """

        for _sn in self.pathed_cb_nodes:

            _sa = coin_utils.search(_sn.path_node, self.view_state.sg_root)
            _sn.cb_node.setPath(_sa.getPath())

    def set_event_path(self, callback, pathed=True):
        """
        Set/clear a path on a specific callback node
        """

        _cb = self.pathed_cb_nodes[-1]

        _path = None

        if pathed:

            for _c in self.pathed_cb_nodes:

                for _d in _c.callbacks:

                    if _d != callback[0]:
                        continue

                    _sa = coin_utils.search(
                        _cb.path_node, self.view_state.sg_root)

                    _path = _sa.getPath()

                    break

        _cb.cb_node.setPath(_path)

    def add_event_callback(self, event_type, callback, pathed=True):
        """
        Add an event callback
        """

        _node = self.pathed_cb_nodes[-1].cb_node

        if not pathed:
            _node = self.local_cb_node

        else:
            self.pathed_cb_nodes[-1].callbacks.append(callback)

        return _node.addEventCallback(event_type, callback)

    def remove_event_callback(
        self, event_type=None, callback=None, pathed=True):
        """
        Remove an event callback.

        index - index of callback node.
        event_type - event type of callback to remove (optional).
        callback - Callback to remove.  If None, removes all by event_type
        """

        assert((callback is not None) or (event_type is not None)), """
        Event.remove_event_callback():callback and event_type are None
        """

        _node = self.pathed_cb_nodes[-1].cb_node

        if not pathed:
            _node = self.local_cb_node

        _node.removeEventCallback(callback)

    def add_keyboard_event(self, callback, pathed=False):
        """
        Convenience function
        """

        return self.add_event_callback(InputEvent.KEYBOARD, callback, pathed)

    def add_mouse_event(self, callback, pathed=True):
        """
        Convenience function
        """

        return self.add_event_callback(InputEvent.LOCATION2, callback, pathed)

    def add_button_event(self, callback, pathed=True):
        """
        Convenience function
        """

        return self.add_event_callback(
            InputEvent.MOUSE_BUTTON, callback, pathed)

    def remove_keyboard_event(self, callback, pathed=False):
        """
        Convenience function
        """

        self.remove_event_callback(InputEvent.KEYBOARD, callback, pathed)

    def remove_mouse_event(self, callback, pathed=True):
        """
        Convenience function
        """

        self.remove_event_callback(InputEvent.LOCATION2, callback, pathed)

    def remove_button_event(self, callback, pathed=True):
        """
        Convenience function
        """

        self.remove_event_callback(InputEvent.MOUSE_BUTTON, callback, pathed)

    def events_enabled(self):
        """
        Returns whether or not event switch is on
        """

        return self.event.whichChild == 0

    def toggle_pathed_event_callbacks(self):
        """
        Switch pathed events on / off
        """

        coin_utils.toggle_switch(self.pathed_switch)

    def toggle_local_event_callbacks(self):
        """
        Switch event callbacks on / off
        """

        coin_utils.toggle_switch(self.local_switch)

    def finish(self):
        """
        Cleanup
        """

        self.event.finalize()
        self.handle_events = False
        self.local_cb_node = None
        self.pathed_switch = None
        self.local_switch = None
        self.pathed_cb_nodes = []

        Event._self_weak_list = {}
        Event.global_cb_node = None


Event.init_graph()

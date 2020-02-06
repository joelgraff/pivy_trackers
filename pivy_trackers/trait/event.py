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


from ..support.tuple_math import TupleMath

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

    #class statics
    _self_weak_list = {}
    _default_callback_node = None

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

        self.callback_nodes = []

        self.handle_events = False

        #create a global callback for managing mouse updates
        if not Event._default_callback_node:

            self.add_mouse_event(self._event_mouse_event)
            self.add_button_event(self._event_button_event)
            Event._default_callback_node = self.callback_nodes[0].cb_node

        self.event.set_visibility(True)

        Event._self_weak_list[self] = weakref.ref(self)

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

        _vec = TupleMath.scale(self.mouse_state.vector, 0.10)
        _pos = TupleMath.add(self.mouse_state.prev_position, _vec)

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

        self.callback_nodes.append(
            SimpleNamespace(
                cb_node=self.event.add_node(Nodes.EVENT_CB, 'EVENT_CALLBACK'),
                path_node=None,
                callbacks=[]
            )
        )

    def remove_event_callback_node(self, node=None, index=-1):
        """
        Remove an event callback node from the current group

        """

        if node is None:
            node = self.callback_nodes[index].cb_node

        self.event.remove_node(node)

        del self.callback_nodes[index]

    def set_event_paths(self):
        """
        Set paths on every callback node that has a path
        """

        for _c in self.callback_nodes:
            
            if not _c.path_node:
                continue

            _sa = coin_utils.search(_c.path_node, self.view_state.sg_root)
            _c.cb_node.setPath(_sa.getPath())

    def set_event_path(self, callback, is_pathed=True):
        """
        Set/clear a path on a specific callback node
        """

        for _c in self.callback_nodes:

            for _d in _c.callbacks:
                if _d != callback:
                    continue

            _path = None

            if is_pathed and _c.path_node:
                _sa = coin_utils.search(_c.path_node, self.view_state.sg_root)
                _path = _sa.getPath()

            _c.cb_node.setPath(_path)

            break

    def add_event_callback(self, event_type, callback, index=-1):
        """
        Add an event callback
        """

        #if none exist, add a new one
        #otherwise default behavior reuses last-created SoEventCb node
        if not self.callback_nodes:
            self.add_event_callback_node()

        assert(index < len(self.callback_nodes)), """
        Event.add_event_callback(): index {} exceeds callback list length.
        """.format(str(index))
        
        _cb_node = self.callback_nodes[index].cb_node
        _cb = _cb_node.addEventCallback(event_type, callback)

        self.callback_nodes[index].callbacks.append(
            SimpleNamespace(
                callback=_cb,
                event_type=event_type
            )
        )

        return _cb

    def remove_event_callback(self, event_type=None, callback=None, index=-1):
        """
        Remove an event callback.

        index - index of callback node.
        event_type - event type of callback to remove (optional).
        callback - Callback to remove.  If None, removes all by event_type
        """

        if not self.callback_nodes:
            return

        assert((callback is not None) or (event_type is not None)), """
        Event.remove_event_callback():callback and event_type are None
        """
        assert(index < len(self.callback_nodes)), """
        Event.add_event_callback(): index {} exceeds callback list length.
        """.format(str(index))

        for _c in self.callback_nodes:

            for _d in list(_c.callbacks):

                if (event_type is not None) and (_d.event_type != event_type):
                    continue

                if callback and (callback != _d.callback):
                    continue

                _c.callbacks.remove(_d)
                _c.node.removeEventCallback(callback)

            if not _c.callbacks:
                self.remove_event_callback_node(index)

    def add_mouse_event(self, callback):
        """
        Convenience function
        """

        return self.add_event_callback(MouseEvents.LOCATION2, callback)

    def add_button_event(self, callback):
        """
        Convenience function
        """

        return self.add_event_callback(MouseEvents.MOUSE_BUTTON, callback)

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

    def finish(self):
        """
        Cleanup
        """

        self.event.finalize()
        self.callback_nodes = []
        self.handle_events = False

        Event._self_weak_list = {}
        Event._default_callback_node = None


Event.init_graph()

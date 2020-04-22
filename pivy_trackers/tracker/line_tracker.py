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
Line tracker class for tracker objects
"""

import random

from ..coin import coin_utils

from collections.abc import Iterable
from ..support.tuple_math import TupleMath

from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.todo import todo

from .geometry_tracker import GeometryTracker
from .marker_tracker import MarkerTracker

from ..trait.text import Text
from ..trait.keyboard import Keyboard

class LineTracker(GeometryTracker, Text, Keyboard):
    """
    Tracker object for SoLineSet
    """

    def __init__(self, name, points, parent, view=None, selectable=True):
        """
        Constructor
        """

        super().__init__(name=name, parent=parent, view=view)

        #build node structure for the node tracker
        self.line = self.geometry.add_node(Nodes.LINE_SET, name)

        self.markers =\
            MarkerTracker(name + '_marker_tracker', None, self.base)

        self.markers.set_visibility(False)

        #add events to specific geometry
        self.add_node_events(self.line)
        #self.add_keyboard_events()

        self.groups = []

        self.center = (0.0, 0.0, 0.0)

        #definte the base/parent node for text nodes to be the geometry node
        self.text_base = self.geometry.top

        self.set_style()
        self.set_visibility(True)

        self.update_cb = None
        self.update(coordinates=points, notify=False)

        self.draggable_text = True
        self.drag_style = self.DragStyle.CURSOR
        self.drag_axis = None

        _fn = lambda:\
            self.markers.geometry.remove_node(self.markers.geometry.coordinate)

        #callback to be triggered after graph is inserted into scenegraph
        self.on_insert_callbacks.append(_fn)

    def get_drag_nodes(self):
        """
        Internal function for use with todo.delay()
        """

        if not self.draggable_text:
            return []

        if not self.text:
            return []

        _top = self.text.top.copy()

        #reset when drag nodes are requested
        self.text_copies = []

        #save the copies of the text nodes to the CoinText object
        for _i in range(2, _top.getNumChildren()):
            self.text_copies.append(_top.getChild(_i).getChild(0))

        return [_top]

    def add_text(
        self, name=None, text=None, has_transform=False, has_font=False):
        """
        Convenience override of Text.add_text
        """

        super().add_text(name, text, has_transform, has_font)

        #position text at midpoint of line and force transform update
        self.text_offset = self.center
        self.set_text_translation((0.0, 0.0, 0.0))

    def get_length(self):
        """
        Return the line length
        """

        if not self.coordinates:
            return 0.0

        return TupleMath.length(self.coordinates)

    def set_length(self, length):
        """
        Set the length of the line by scaling the line points about the
        line's center
        """

        _scale = length / self.get_length()

        _coords = self.coordinates[:]

        for _i, _c in enumerate(_coords):

            _delta = TupleMath.subtract(_c, self.center)
            _delta = TupleMath.scale(_delta, _scale)
            _coords[_i] = TupleMath.add(_delta, self.center)

        self.update(coordinates=_coords)
        self.set_text(str(length))

    def show_markers(self):
        """
        Show the SoMarkerSet
        """

        self.markers.set_visibility(True)

    def hide_markers(self):
        """
        hide the SoMarkerSet
        """

        self.markers.set_visibility(False)

    def set_vertex_groups(self, groups):
        """
        Set the vertex groups for the line tracker

        groups - an itearable of vertex groupings
        """

        assert(sum(groups) == len(self.pionts)),\
            'LineTracker.set_vertex_groups: group count does not match number of points'

        self.line.numVertices.setValues(0, len(groups), groups)

    def update(self, coordinates=None, matrix=None, groups=None, notify=True):
        """
        Override of Geometry method
        """

        super().update(coordinates=coordinates, matrix=matrix, notify=notify)

        if self.text and self.text.is_visible():

            self.text.set_translation(
                TupleMath.mean(self.coordinates)
            )

        if self.update_cb:
            self.update_cb()

        if groups:
            self.groups = groups
            self.line.numVertices.setValues(0, len(groups), groups)

        if self.coordinates:
            self.center = TupleMath.mean(self.coordinates)

        self.text_center = self.center
        self.set_text_translation((0.0, 0.0, 0.0))

    def drag_text_update(self, text):
        """
        Update the drag text.  Called from inheriting class
        """

        #directly update the text of the node in the drag copy
        #with the supplied string

        for _v in self.text_copies:
            self.set_text(text, _v)

    def before_drag(self, user_data):
        """
        Start of drag operations
        """

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

        self.text_copies = []
        super().after_drag(user_data)

    def drag_mouse_event(self, user_data, event_cb):
        """
        Override of Drag.drag_mouse_event()
        """

        self.set_drag_axis(self.drag_axis)
        super().drag_mouse_event(user_data, event_cb)

    def link_marker(self, marker, index):
        """
        Link a marker node to the line for automatic updates
        """

        self.link_geometry(marker, index, 0)

    def update_drag_center(self):
        """
        Override of Drag method
        """

        #default to the current cursor position
        _pt = self.mouse_state.world_position

        #average the coordinates to calculate the centerpoint
        if self.drag_style == self.DragStyle.AVERAGE:

            _pt = (0.0, 0.0, 0.0)

            for _p in self.coordinates:
                _pt = TupleMath.add(_pt, _p)

            _pt = TupleMath.multiply(_pt, 0.5)

        #use Manhattan distance to find nearest endpoint
        elif self.drag_style == self.DragStyle.ENDPOINT:

            _dist = -1
            _cursor = self.mouse_state.world_position
            _pt = _cursor

            _fn = lambda p1, p2: abs(_pt[0] - _p[0])\
                        + abs(_pt[1] - _p[1])\
                        + abs(_pt[2 - _p[2]])

            for _p in self.coordinates:

                if _dist == -1:
                    _dist = _fn(_cursor, _p)
                    continue

                _new_dist = _fn(_cursor, _p)

                if _new_dist < _dist:
                    _dist = _new_dist
                    _pt = _p

        return _pt

    def notify_geometry(self, event, message):
        """
        Geometry message notification override
        """
        super().notify_geometry(event, message)

        if not self.is_valid_notify:
            return

        _coordinates = self.coordinates[:]

        #test for update from a linked geometry
        if hasattr(message.sender, 'linked_geometry'):

            #if linked, update points according to specified indices
            if message.sender in self.linked_geometry:

                _self_idx = self.linked_geometry[message.sender][0]
                _target_idx = message.sender.linked_geometry[self][0]

                _coordinates[_self_idx] = message.data[_target_idx]

        self.coordinates = _coordinates

        #Add sender to the excluded subscribers list, call update and
        #dispatch messages, then remove the sender
        self.excluded_subscribers.append(message.sender)
        self.update(coordinates=self.coordinates)
        del self.excluded_subscribers[-1]

    def notify_widget(self, event, message):
        """
        UI message notification override
        """
        super().notify_widget(event, message)

    def reset(self):
        """
        Reset geometry
        """

        self.line.numVertices.setValues(0,0,[])
        self.line.numVertices.touch()
        super().reset()

    def finish(self):
        """
        Cleanup
        """

        self.line = None
        self.drag_style = None
        self.linked_geometry = None

        super().finish()

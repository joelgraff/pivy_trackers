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
Geometry tracker base class
"""

from ..trait.base import Base
from ..trait.message import Message
from ..trait.style import Style
from ..trait.event import Event
from ..trait.pick import Pick
from ..trait.select import Select
from ..trait.drag import Drag
from ..trait.geometry import Geometry

from ..trait import enums

from ..coin.coin_styles import CoinStyles

class GeometryTracker(
    Base, Message, Style, Geometry, Event, Pick, Select, Drag):

    """
    Geometry tracker base class
    """

    #static alias for DragStyle class
    DragStyle = enums.DragStyle

    def __init__(self, name, parent, view=None):
        """
        Constructor
        """

        super().__init__(name=name, parent=parent, view=view)

        self.linked_geometry = {}
        self.coin_style = CoinStyles.DEFAULT

    def link_geometry(self, target, source_index, target_index):
        """
        Link another geometry to the line for automatic updates

        target - reference to geometry to be linked
        source_index - index updated by target geometry
        target_index - index updated by this geometry
        """

        if target not in self.linked_geometry:

            #register the line and geometry with each other
            self.register_geometry(target, True)
            self.linked_geometry[target] = []

        self.linked_geometry[target].append(source_index)

        if self not in target.linked_geometry:
            target.linked_geometry[self] = []

        target.linked_geometry[self].append(target_index)

    def add_node_events(self, node=None, add_callback=False, pathed=True):
        """
        Set up node events for the passed node
        """

        #optionally create a separate callback node for new geometry
        if add_callback:
            pathed = True
            self.add_event_callback_node()

        #events are added to the last-added event callback node
        self.add_mouse_event(self.select_mouse_event)
        self.add_button_event(self.select_button_event)

        if pathed:

            assert(node is not None), """pivy_trackers::GeometryTracker.add_node_events() - Node is NoneType.  Cannot apply event path"""

            self.path_nodes.append(node)

    def reset(self):
        """
        Reset the coordinates and transform
        """

        super().reset()
        self.geometry.set_rotation(0.0, (0.0, 0.0, 0.0))
        self.geometry.set_translation((0.0, 0.0, 0.0))

    def update(self, coordinates, notify=True):
        """
        Override of Geometry method to provide messaging support
        """

        if not coordinates:
            return

        _c = coordinates

        if not isinstance(_c, list):
            _c = [_c]

        is_unique = len(self.prev_coordinates) != len(_c)

        if not is_unique:

            for _i, _v in enumerate(self.prev_coordinates):

                if _v != _c[_i]:
                    is_unique = True
                    break

        if not is_unique:
            return

        super().update(coordinates)

        self.coordinates = coordinates

        if not notify:
            return

        if not isinstance(coordinates, list):
            coordinates = [coordinates]

        self.dispatch_geometry(coordinates)

    def notify_geometry(self, event, message):
        """
        Override of Message method to provide geometry update support
        """

        super().notify_geometry(event, message)

    def finish(self):

        Base.finish(self)
        Message.finish(self)
        Style.finish(self)
        Geometry.finish(self)
        Event.finish(self)
        Pick.finish(self)
        Select.finish(self)
        Drag.finish(self)
 
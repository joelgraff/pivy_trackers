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
Geometry nodes for Tracker objects
"""

from ..support.smart_tuple import SmartTuple

from ..coin.coin_group import CoinGroup
from ..coin.coin_enums import NodeTypes as Nodes

class Geometry():
    """
    Geometry nodes for Tracker objects
    """

    #members provided by Base, Style
    base = None
    active_style = None
    name = ''

    def set_visibility(self, visible=True): """prototype"""; pass

    is_switched = None
    is_separated = None
    switch_first = None

    @staticmethod
    def init_graph(is_switched=False, is_separated=False, switch_first=True):
        Geometry.is_switched = is_switched
        Geometry.is_separated = is_separated
        Geometry.switch_first = switch_first

    def __init__(self):
        """
        Constructor
        """

        assert(all([self.active_style, self.base])),"""
        Geometry trait initialization failed - missing required traits.
        """

        self.geometry = CoinGroup(
            is_separated=Geometry.is_separated,
            is_switched=Geometry.is_switched,
            switch_first=Geometry.switch_first,
            parent=self.base, name=self.name + '__GEOMETRY')

        self.geometry.transform = self.geometry.add_node(Nodes.TRANSFORM)
        self.geometry.coordinate = self.geometry.add_node(Nodes.COORDINATE)

        self.coordinates = []
        self.prev_coordinates = []

        #reset the graph node parameters
        Geometry.init_graph()

        super().__init__()

    def reset(self):
        """
        Reset the coordinate node
        """

        self.geometry.coordinate.point.setValue([1, 1, 0])
        self.coordinates = []
        self.prev_coordinates = []

    def update(self, coordinates):
        """
        Update implementation
        """

        self.set_coordinates(coordinates)

    def transform_points(self, points=None):
        """
        Transform points by the transformation matrix
        points = a list / tuple of 3D coordinates in tuple form
        """

        if points is None:
            points = self.get_coordinates()

        #no node, use the coordinate node local to this group
        return self.view_state.transform_points(
            points, self.geometry.coordinate, True)

    def set_coordinates(self, coordinates):
        """
        Update the SoCoordinate3 with the passed coordinates
        Assumes coordinates is a list of 3-float tuples
        """

        #encapsulate a single coordinate as a list
        if not isinstance(coordinates, list):
            coordinates = [coordinates]

        self.prev_coordinates = self.get_coordinates()
        self.geometry.coordinate.point.setValues(coordinates)
        self.coordinates = coordinates

    def get_coordinates(self, _dtype=tuple):
        """
        Return the coordinates as the specified iterable type
        """

        return [
            _dtype(_v.getValue()) \
                for _v in self.geometry.coordinate.point.getValues()
        ]

    def finish(self):
        """
        Cleanup
        """

        self.geometry.transform = None
        self.geometry.coordinate = None

        self.geometry.finalize()

Geometry.init_graph()

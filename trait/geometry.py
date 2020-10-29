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
Geometry nodes for Tracker objects
"""

from collections.abc import Iterable

from ..support.core.tuple_math import TupleMath

from ..coin.coin_group import CoinGroup
from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.todo import todo

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
    is_geo = None
    switch_first = None

    @staticmethod
    def init_graph(
        is_switched=False, is_separated=False, switch_first=True, is_geo=False):

        Geometry.is_switched = is_switched
        Geometry.is_separated = is_separated
        Geometry.switch_first = switch_first
        Geometry.is_geo = is_geo

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

        self.geometry.transform =\
            self.geometry.add_node(Nodes.TRANSFORM, self.name + '_transform')

        _type = Nodes.COORDINATE
        _name = self.name + '_Coordinate'

        #set up the GeoNode support structure
        if self.is_geo:

            _type = Nodes.GEO_COORDINATE
            _name = self.name + '_GeoCoordinate'

        self.geometry.coordinate = self.geometry.add_node(_type, _name)

        self.coordinates = []
        self.prev_coordinates = []
        self.linked_geometry = {}
        self.in_update = False
        self.linked_parent = None
        self.do_linked_update = True

        #flag to update the transform node instead of the coordinate node
        self.update_transform = False

        #reset the graph node parameters
        Geometry.init_graph()

        super().__init__()

    def set_geo_reference(self, system, coords):
        """
        Set the system and coordinates of the passed node.
        If none, then sets the existing separator and coordinate nodes
        """

        _top = None

        if isinstance(self.geometry.top, Nodes.GEO_SEPARATOR):
            _top = self.geometry.top

        elif isinstance(self.geometry.root, Nodes.GEO_SEPARATOR):
            _top = self.geometry.root

        if _top:
            _top.geoSystem.setValues(system)
            _top.geoCoords.setValue(coords[0], coords[1], coords[2])

        if isinstance(self.geometry.coordinate, Nodes.GEO_COORDINATE):
            self.geometry.coordinate.geoSystem.setValues(system)

    def get_matrix(self):
        """
        Return the transformation matrix applied to the coordinate
        """

        self.view_state.get_matrix(self.geometry.coordinate)

    def reset(self):
        """
        Reset the coordinate node
        """

        self.geometry.coordinate.point.setValue([1, 1, 0])
        self.coordinates = []
        self.prev_coordinates = []

    def update(self, coordinates, matrix=None, notify=False):
        """
        Updates the coordinates of the current object and triggers
        linked object updates
        """

        #Examine the passed coordinates, identifying which have changed
        #Pass a list of the changed indices and coordinates to linked_update

        if self.in_update or (not coordinates and not matrix):
            return

        _c = coordinates

        #compute transformation if matrix is specified
        #otherwise, ensure the coordinates are encapsulated in a list
        if matrix and self.coordinates:
            _c = self.view_state.transform_points(self.coordinates, matrix)

        if _c[0] is not None and not isinstance(_c[0], Iterable):
            _c = (_c,)

        #replace any None values with the current coordinate to ensure a zero delta
        for _i, _v in enumerate(_c):

            if _v is None and self.coordinates:
                _c[_i] = self.coordinates[_i]

        if self.coordinates:

            #abort if no change
            if self.coordinates == _c:
                return

            #abort if there are a different number of new coordinates
            if len(self.coordinates) != len(_c):
                return

        #compute the changes in coordinates
        _deltas = _c

        if self.coordinates:
            _deltas = TupleMath.subtract(_c, self.coordinates)

        #deltas need to be encapsulated as tuples in a tuple as it's assumed
        #a separate delta for each coordinate
        if not isinstance(_deltas[0], Iterable):
            _deltas = (_deltas,)

        #no changes, either by coordinate update or matrix transformation.
        if not _deltas or all([_v==(0.0, 0.0, 0.0) for _v in _deltas]):
           return

        #get a list of the coordinates which differ from current
        _indices = [_i for _i, _v in enumerate(self.coordinates)\
            if _v and _v != (0.0, 0.0, 0.0)
        ]

        if self.do_linked_update:

            self.in_update = True

            #process linked updates if responsible for any
            if self.coordinates and self in self.linked_geometry:

                for _v in self.linked_geometry[self]:

                    if _v is self.linked_parent:
                        continue

                    _v.linked_update(self, _indices, _deltas)

            self.in_update = False

        self.prev_coordinates = self.get_coordinates()
        self.coordinates = _c

        #process updates to the current geometry
        if not self.update_transform:
            todo.delay(self.set_coordinates, _c)

        else:
            _t = self.geometry.get_translation()
            self.geometry.set_translation(TupleMath.add(_t, _c[0]))

    def linked_update(self, parent, indices, deltas):
        """
        Updates geometry linked to this object
        """

        if not parent in self.linked_geometry:
            print('ABORT: {} not linked to {}'.format(parent.name, self.name))
            return

        if self.in_update:
            print('ABORT:{} already updating!!'.format(self.name))
        #indices in this object which are linked to the parent
        _link_indices = self.linked_geometry[parent]
        _link_coords = [_v.getValue()\
                for _v in self.geometry.coordinate.point.getValues()
            ]

        #iterate the changed indices, adding the corresponding parent delta
        for _i, _v in enumerate(indices):

            if _v not in _link_indices:
                continue

            #update by transform or update all coordinates
            if any(_w == -1 for _w in _link_indices[_v]):
                _link_coords = deltas[_v]

            #iterate each linked index, and update the corresponding coordinate
            else:

                for _x in _link_indices[_v]:
                    _link_coords[_x] =\
                        TupleMath.add(deltas[_i], _link_coords[_x])

        self.linked_parent = parent
        self.update(_link_coords, notify = "1")
        self.linked_parent = None

    def transform_points(self, points=None):
        """
        Transform points by the transformation matrix
        points = a list / tuple of 3D coordinates in tuple form
        """

        if points is None:
            points = self.get_coordinates()

        _matrix = self.view_state.get_matrix(
            self.geometry.coordinate, self.geometry.base)

        #no node, use the coordinate node local to this group
        return self.view_state.transform_points(
            points, _matrix)

    def set_coordinates(self, coordinates):
        """
        Update the SoCoordinate3 with the passed coordinates
        Assumes coordinates is a list of 3-float tuples
        """

        self.geometry.coordinate.point.setValues(
            0, len(coordinates), coordinates)

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

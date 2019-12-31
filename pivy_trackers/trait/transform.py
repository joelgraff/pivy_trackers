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
Transform node for Tracker objects
"""

from ..coin.coin_group import CoinGroup
from ..coin.coin_enums import NodeTypes as Nodes

class Transform():
    """
    Transform node for Tracker objects
    """

    #members provided by Base, Style
    base = None
    name = ''

    is_switched = None
    is_separated = None
    switch_first = None

    @staticmethod
    def init_graph(is_switched=False, is_separated=False, switch_first=True):
        Transform.is_switched = is_switched
        Transform.is_separated = is_separated
        Transform.switch_first = switch_first

    def __init__(self):
        """
        Constructor
        """

        assert(self.base),"""
        Transform trait initialization failed - missing required traits.
        """

        self.transform = CoinGroup(
            is_separated=Transform.is_separated,
            is_switched=Transform.is_switched,
            switch_first=Transform.switch_first,
            parent=self.base, name=self.name + '__GEOMETRY')

        self.transform.transform = self.geometry.add_node(Nodes.TRANSFORM)

        #reset the graph node parameters
        Transform.init_graph()

        super().__init__()

    def update(self, coordinates):
        """
        Update implementation
        """

        self.set_coordinates(coordinates)

    def transform_points(self, points):
        """
        Transform points by the transformation matrix
        points = a list / tuple of 3D coordinates in tuple form
        """

        assert(points),\
            'Trasnsform.transform_points(): cannot transform NoneType')

        #no node, use the coordinate node local to this group
        return self.view_state.transform_points(
            points, self.transform, True)

    def finish(self):
        """
        Cleanup
        """

        self.tranform.transform = None
        self.transform.finalize()

Transform.init_graph()

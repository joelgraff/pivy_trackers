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
Box tracker class
"""

from ..support.tuple_math import TupleMath
from ..coin.coin_enums import NodeTypes as Nodes

from .line_tracker import LineTracker

class BoxTracker(LineTracker):
    """
    Box tracker class
    """

    def __init__(self, name, corners, parent, view=None):
        """
        Constructor

        corners - List of corners as 2 or 3-coordinate tuples (z-coord ignored)
        """

        self.dimensions = TupleMath.subtract(corners[1], corners[0])[0:2]
        self.corners = []

        for _p in corners:

            self.corners.append(_p)

            if len(_p) == 2:
                self.corners[-1] = _p + (0.0,)

        #generate formal coordinate list
        _points = (
            self.corners[0], (self.corners[1][0], self.corners[0][1], 0.0),
            self.corners[1], (self.corners[0][0], self.corners[1][1], 0.0),
            self.corners[0]
        )

        #build the box
        super().__init__(name=name, points=_points, parent=parent, view=view)

        self.hide_markers()

    def finish(self):
        """
        Cleanup
        """

        self.dimensions = None

        super().finish()

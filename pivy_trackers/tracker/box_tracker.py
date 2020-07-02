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

from pivy_trackers.pivy_trackers import TupleMath

from ..trait.base import Base
from ..trait.geometry import Geometry

from .polyline_tracker import PolyLineTracker

class BoxTracker(PolyLineTracker):
    """
    Box tracker class
    """

    def __init__(self, name, corners, parent,
                 is_resizeable=True, update_transform=True, view=None):

        """
        Constructor

        corners - List of corners as 2 or 3-coordinate tuples (z-coord ignored)
        parent - the reference to the parent node
        is_resizeable - determines whether or not box dimensions can change
        update_transform - when linked to other geomtry, update single transform
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
            self.corners[1], (self.corners[0][0], self.corners[1][1], 0.0)
        )

        super().__init__(
            name=name, parent=parent, view=view, is_adjustable=is_resizeable, points=_points, is_closed=True)

        self.set_visibility()

    def finish(self):
        """
        Cleanup
        """

        self.dimensions = None

        super().finish()

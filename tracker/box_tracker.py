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

from ..support.core.tuple_math import TupleMath

from ..trait.base import Base
from ..trait.geometry import Geometry

from .polyline_tracker import PolyLineTracker

class BoxTracker(PolyLineTracker):
    """
    Box tracker class
    """

    def __init__(self, name, points, parent,
                 is_resizeable=True, update_transform=True, view=None):

        """
        Constructor

        points - points which completely define the box in one of three formats:
            1.  Corners ([tuple, tuple]) - tuples of opposing corners
            2.  Points ([tuple, tuple, tuple, tuple]) - tuples of all corners
            3.  Center/Size ([tuple, float, float]) - tuple of box center and float of width / height (one float) or width, height (two floats)

        parent - the reference to the parent node
        is_resizeable - determines whether or not box dimensions can change
        update_transform - when linked to other geomtry, update single transform
        """

        self.coordinates = self._coordinates(points)

        super().__init__(
            name=name, parent=parent, view=view, is_adjustable=is_resizeable, points=self.coordinates, is_closed=True)

        self.set_visibility()

    def _coordinates(self, points):
        """
        Parse the list of points to determine the box coordinates
        """

        assert isinstance(points, list), """
        BoxTracker: Points not contained in a list
        """

        assert isinstance(points[0], tuple), """
        BoxTracker: First point in list must be tuple
        """

        _result = []

        #box defined by opposing corners.  iterate and pad if necessary
        if len(points) == 2:

            if isinstance(points[1], tuple):

                self.pad_points(points)

                _result = (
                    self.coordinates[0],
                    (self.coordinates[1][0], self.coordinates[0][1], 0.0),
                    self.coordinates[1],
                    (self.coordinates[0][0], self.coordinates[1][1], 0.0)
                )

        elif len(points) == 4:
            assert all([isinstance(_v, tuple) for _v in points]), """
            BoxTracker: 4 element list must be tuples
            """

            self.pad_points(points)

            _result = points

        elif isinstance(points[-1], float):

            _w = 0.0
            _h = 0.0
            _c = points[0]

            if len(points) == 2:
                _w = points[-1] / 2.0
                _h = _w

            elif len(points) == 3:

                assert isinstance(points[-2], float), """
                BoxTracker: [tuple, float, float] format required
                """

                _w = points[-2] / 2.0
                _h = points[-1] / 2.0

            _result = [
                (_c[0] - _w, _c[1] - _h, 0.0),
                (_c[0] + _w, _c[1] - _h, 0.0),
                (_c[0] + _w, _c[1] + _h, 0.0),
                (_c[0] - _w, _c[1] + _h, 0.0)
            ]

        assert _result, """
        BoxTracker: undefined coordinate format for {}
        """.format(str(points))

        return _result

    def pad_points(self, points, length=3, value=0.0):
        """
        Pad a 2-tuple with an extra 0.0
        """

        for _p in points:

            if len(_p) == length:
                continue

            while len(_p) < length:
                _p += (0.0,)

    def finish(self):
        """
        Cleanup
        """

        self.dimensions = None

        super().finish()

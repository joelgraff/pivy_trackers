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
Polyline tracker class
"""

from pivy_trackers.pivy_trackers import TupleMath

from ..trait.base import Base
from ..trait.geometry import Geometry

from .line_tracker import LineTracker
from .geometry_tracker import GeometryTracker
from .marker_tracker import MarkerTracker

class PolyLineTracker(GeometryTracker):
    """
    PolyLine tracker class
    """

    def __init__(self, name, points, parent, is_adjustable=True,
                 is_closed=False, view=None, index=-1):
        """
        Constructor

        points - a list of tuples defining the points (2D or 3D)
        parent - the parenting object
        is_adjustable - move line segments independently (linked)
        is_closed - connect the last point to the first
        """

        super().__init__(name=name, parent=parent, view=view)

        self.points = []
        self.lines = []

        _prev = None

        for _i, _p in enumerate(points):

            if len(_p) == 2:
               _p += (0.0,)

            if is_adjustable:

                if self.points:

                    self.lines.append(LineTracker('segment ' + str(_i),
                        [_prev, _p], self.base, index=index)
                    )

                    _count = len(self.lines)

                    if _count > 1:

                        self.lines[_count - 2].link_geometry(
                            self.lines[-1], 1, [0])

                    _indices = [0]

                    if _i == len(points) - 1:
                        _indices = []

                    self.lines[-1].enable_markers(_indices)

            self.points.append(_p)

            _prev = _p

        _points = self.points

        if is_closed:

            _points.append(_points[0])

            if is_adjustable:

                self.lines.append(LineTracker('segment' + str(len(points) + 1),
                    [_prev, self.points[0]], self.base, index=index
                ))

        if not self.lines:

            self.lines = [
                LineTracker('segment 0', _points, self.base, index=index)]

        self.set_visibility()

    def finish(self):
        """
        Cleanup
        """

        self.lines = []
        self.points = []

        super().finish()

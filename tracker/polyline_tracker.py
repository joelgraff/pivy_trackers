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

from .line_tracker import LineTracker
from .context_tracker import ContextTracker

class PolyLineTracker(ContextTracker):
    """
    PolyLine tracker class
    """

    def __init__(self, name, points, parent, is_adjustable=True,
                 is_closed=False, view=None, index=-1, subdivided=True):
        """
        Constructor

        points - a list of tuples defining the points (2D or 3D)
        parent - the parenting object
        is_adjustable - move line segments independently (linked)
        is_closed - connect the last point to the first
        """

        super().__init__(name=name, parent=parent, view=view)

        self.points = [_v + (0.0,) if len(_v) == 2 else _v for _v in points]
        self.lines = []
        self.is_linked = is_adjustable
        self.is_subdivided = subdivided

        _prev = None

        if subdivided:
            self.build_subd_tracker(points, index, is_closed)

        else:

            self.lines = [LineTracker(
                self.name + '_segment', points, self.base, index=index)]


    def build_subd_tracker(self, points, index, is_closed):
        """
        Build a subdivided tracker for each point pair
        """

        for _i, (_v, _w) in enumerate(zip(self.points[:-1], self.points[1:])):

            _line = LineTracker(f'{self.name}_segment{str(_i)}',
                [_v, _w], self.base, index=index)

            self.lines.append(_line)

            _count = len(self.lines)

            if self.is_linked:

                if _count > 1:

                    self.lines[-2].link_geometry(_line, 1, [0])

            _indices = [0]

            if _i == len(points) - 2:
                _indices = []

            _line.enable_markers(_indices, self.is_linked)

        _points = self.points

        if is_closed:

            _points.append(_points[0])

            self.lines.append(
                LineTracker(self.name + '_segment' + str(len(points)),
                [_prev, self.points[0]], self.base, index=index
            ))

            if self.is_linked:

                self.lines[-2].link_geometry(self.lines[-1], 1, [0])
                self.lines[-1].link_geometry(self.lines[0], 1, [0])

    def get_coordinates(self):
        """
        Return the line coordinates
        """

        #return every other item starting with the first as each endpoint
        #is duplicated as the start point of the next line
        _t = [_w for _v in self.lines for _w in _v.coordinates][0::2]
        _t.append(self.lines[-1].coordinates[-1])

        return _t

    def update(self, coordinates):
        """
        Updates line coordinates.  List is mapped 1:1 to lines in order of
        creation.  Terminates early with shorter lists, ignores coordinates
        exceeding line count with longer lists
        """

        _prev = coordinates[0]
        self.points = coordinates

        if not self.is_subdivided:
            return

        for _i, _v in enumerate(coordinates[1:]):

            _line = self.lines[_i]
            _line.do_linked_update = False
            _line.update([_prev, _v], notify='2')
            _line.do_linked_update = self.is_linked

            if not self.is_linked:

                for _i, _m in enumerate(_line.markers):
                    _m.update(_line.coordinates[_i])

            _prev = _v

    def invalidate(self, lines=[], markers=[]):
        """
        Invalidate geometry to prevent updates (drag operations)
        lines / markers, indices of geometry to invalidate
        """

        #if no indices are passed, invalideate everything
        if not lines and not markers:
            lines = tuple(range(0, len(self.lines)))

        for _i in lines:
            self.lines[_i].invalidate()

        for _i in markers:
            self.lines[_i].markers[0].invalidate()


    def finish(self):
        """
        Cleanup
        """

        self.lines = []
        self.points = []

        super().finish()

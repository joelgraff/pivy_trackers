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
Tracker for alignment editing
"""

from ..tracker.base_tracker import BaseTracker
from ..tracker.marker_tracker import MarkerTracker
from ..tracker.line_tracker import LineTracker

class PivyTracker(BaseTracker):
    """
    Pivy Tracker example
    """

    def __init__(self, view):
        """
        Constructor
        """

        super().__init__(name='dcoument.object.tracker', view=view)

        #generate initial node trackers and wire trackers for mouse interaction
        #and add them to the scenegraph
        self.trackers = []
        self.build_trackers()

        self.set_visibility(True)

    def build_trackers(self):
        """
        Build the node and wire trackers that represent the selectable
        portions of the alignment geometry
        """

        #a data model of four tuples, defining the corners of a box
        _model = [
            (100.0, 100.0, 0.0),
            (-100.0, 100.0, 0.0),
            (-100.0, -100.0, 0.0),
            (100.0, -100.0, 0.0)
        ]

        #create the marker trackers
        for _i, _v in enumerate(_model):

            self.trackers.append(
                MarkerTracker(
                    name='MARKER-' + str(_i),
                    point=_v,
                    parent=self.base
                )
            )

        _prev = _model[0]

        #create the line trackers
        for _i, _v in enumerate(_model):

            if _i > 0:
                self.trackers.append(
                    LineTracker(
                        name='LINE-' + str(_i),
                        points=[_prev, _v],
                        parent=self.base
                    )
                )

            _prev = _v

        #connect bact to the start
        self.trackers.append(
            LineTracker(
                name='LINE-4', points=[_model[0], _model[3]], parent=self.base)
        )

    def finalize(self, node=None, parent=None):
        """
        Cleanup the tracker
        """

        for _t in self.trackers:

            for _u in _t:
                _u.finalize()

        super().finalize(node, parent)

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
Link trait for Tracker objects
"""

class Link():
    """
    Class definition for Link trait
    """

    def __init__(self):
        """
        Constructor
        """

        self._setting_up_linked_drag = False


    def before_drag(self, user_data):
        """
        Start of drag operations
        """

        self.setup_linked_drag()

        super().before_drag(user_data)



    def link_geometry(self, target, source_idx, target_idx, target_only=False):
        """
        Link another geometry to the line for automatic updates

        target - reference to geometry to be linked
        source_idx - index updated by target geometry
        target_idx - index updated by this geometry
        target_only - if True, source is not updated by changes in target
        index values = 0 to max # of vertices in target line
        index value = -1 = all indices are updated
        """

        if not isinstance(target_idx, Iterable):
            target_idx = [target_idx]

        self._link_geometry(self, target, source_idx, target_idx)

        if not target_only:

            for _v in target_idx:

                #cannot reverse link for full-transformed geometries
                if _v == -1:
                    continue

                #-1 indicates the entire geometry is linked by transform
                self._link_geometry(target, self, _v, [source_idx])

    def _link_geometry(self, source, target, s_idx, t_idx):
        """
        Worker function for self.link_geometry

        source - the object which triggers an update in the target
        target - the object which is updated
        s_idx - the index of the source coordinate triggering the update
        t_idx - list of the index or indices of the target coordinate to update
        """

        #add the source to the target's linked_geometry dict
        #and set up the index dict
        if source not in target.linked_geometry:

            _dict = {}
            target.linked_geometry[source] = _dict

        if not source in source.linked_geometry:
            source.linked_geometry[source] = []

        if not target in source.linked_geometry[source]:
            source.linked_geometry[source].append(target)

        #retrieve the existing index dict
        else:
            _dict = target.linked_geometry[source]

        #if the source index is not already in the dict, add it with the target
        if s_idx not in _dict:
            _dict[s_idx] = []

        _dict[s_idx] += t_idx

    def setup_linked_drag(self, parent=None):
        """
        Set up all linked geometry for a drag oepration
        """

        #abort nested calls
        if self._setting_up_linked_drag:
            return

        #abort call with no parent link
        if parent and (parent not in self.linked_geometry):
            return

        #add to drag list if not previously added
        if not self in Drag.drag_list and self.is_draggable:
            self.drag_copy = self.geometry.copy()
            Drag.drag_list.append(self)

        _indices = []

        #if parent exists and object is not selected, get partial drag indices
        if parent and self not in Select.selected:

            _idx = parent.drag_indices
            _p_idx = self.linked_geometry[parent]

            for _i in _idx:
                if _i in _p_idx:
                    self.drag_indices += _p_idx[_i]

        #otherwise, assume fully-dragged
        else:

            self.is_full_drag = True
            self.drag_indices = list(range(0, len(self.coordinates)))

        #if no dragging occurs, stop here
        if not self.drag_indices:
            return

        if not self in self.linked_geometry:
            return

        self._setting_up_linked_drag = True

        #call linked geometry to set up dragging based on passed indices
        for _v in self.linked_geometry[self]:
            _v.setup_linked_drag(self)

        self._setting_up_linked_drag = False

    def update(self, coordinates, matrix=None, notify=False):
        """
        Updates the coordinates of the current object and triggers
        linked object updates
        """

        #Examine the passed coordinates, identifying which have changed
        #Pass a list of the changed indices and coordinates to linked_update

        if self.in_update:
            return

        if not coordinates and not matrix:
            return

        _c = coordinates

        #compute transformation if matrix is specified
        #otherwise, ensure the coordinates are encapsulated in a list
        if matrix and self.coordinates:
            _c = self.view_state.transform_points(self.coordinates, matrix)

        elif not isinstance(_c[0], Iterable):
            _c = [_c]

        _indices = []
        _deltas = _c

        if self.coordinates:

            #abort if there are a different number of new coordinates
            if len(self.coordinates) != len(_c):
                return

        #compute the changes in coordinates
        _deltas = TupleMath.subtract(_c, self.coordinates)

        #no changes, either by coordinate update or matrix transformation.
        if not _deltas or all([_v==(0.0, 0.0, 0.0) for _v in _deltas]):
            return

        #get a list of the coordinates which differ from current
        _indices = [_i for _i, _v in enumerate(self.coordinates)\
            if _v != (0.0, 0.0, 0.0)
        ]

        self.in_update = True

        #process linked updates if responsible for any
        if self.coordinates and self in self.linked_geometry:

            for _v in self.linked_geometry[self]:
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
            return

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

        self.update(_link_coords)

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
Support class for creating Coin3D node structures
"""

from collections.abc import Iterable

from . import coin_utils as utils
from .coin_enums import NodeTypes as Nodes

class CoinGroup(object):
    """
    Basic coin scenegraph node structure for use with trackers
    """

    scenegraph_root = None

    def __init__(self, is_separated=False, is_switched=False, switch_first=True,
                 parent=None, is_geo=False, name='', index=-1, root_nodes=None):
        """
        Constructor
        parent = CoinGroup or SoNode
        """

        self.name = name

        if not self.name:
            self.name = 'CoinGroup'

        self.top = None
        self.parent = parent
        self.group = None
        self.callback = None
        self.pick = None
        self.draw_style = None
        self.transform = None
        self.coordinate = None
        self.color = None
        self.switch = None
        self.line_set = None
        self.marker_set = None
        self.root = None
        self.font = None

        _parent = None

        if not root_nodes:
            root_nodes = ()

            if is_switched:
                root_nodes += (Nodes.SWITCH,)

            if is_separated:
                root_nodes += (Nodes.SEPARATOR,)

            if is_geo:
                root_nodes += (Nodes.GEO_SEPARATOR,)

        _val_nodes = self.validate_root_nodes(root_nodes)

        for _n in self.validate_root_nodes(root_nodes):

            if _n == Nodes.SWITCH:
                _parent = utils.add_child(Nodes.SWITCH, _parent, self.name + "_Switch")
                self.switch = _parent
                self.set_visibility()

            elif _n == Nodes.SEPARATOR:
                _parent = utils.add_child(Nodes.SEPARATOR, _parent, self.name + '_Separator')
                self.separator = _parent

            elif _n == Nodes.GROUP:
                _parent = utils.add_child(Nodes.GROUP, _parent, self.name + '_Group')
                self.group = _parent

            if not self.root:
                self.root = _parent

            self.top = _parent

        if not self.parent:
            return

        if not self.root:
            self.root = utils.add_child(Nodes.GROUP, _parent, self.name + '_GROUP')
            self.top = self.root

        if isinstance(self.parent, CoinGroup):
            self.parent = self.parent.top

        else:
            assert (isinstance(self.parent, Nodes.NODE)),\
                'CoinGroup parent not of CoinGroup or SoNode type'

        utils.insert_child(self.root, self.parent, index=index)


    def validate_root_nodes(self, root_nodes):
        """
        Validate the root node structure, ensuring specified nodes
        are valid.  Prints warnings and returns valid root nodes
            """

        #single node case
        if not isinstance(root_nodes, Iterable):
            root_nodes = (root_nodes,)

        #valid node list
        _default_set = set((Nodes.GROUP, Nodes.SWITCH, Nodes.SEPARATOR, Nodes.GEO_SEPARATOR))
        _node_set = set(root_nodes)

        #default node configuration
        #if not root_nodes:
        #    return (Nodes.SWITCH, Nodes.SEPARATOR)

        #valid list
        #if _node_set.issubset(_default_set):
            #return root_nodes

        return _node_set & _default_set

    def set_visibility(self, visible=True, child=-3):
        """
        Update the tracker visibility

        visible - whether or not children are visible
        child - specific child to show, -3 = all children
        """

        if not self.switch:
            return

        if visible:
            self.switch.whichChild = child

        else:
            self.switch.whichChild = -1

    def is_visible(self):
        """
        Return the visibility of the tracker
        """
        #pylint: disable=no-member

        if not self.switch:
            return True

        return self.switch.whichChild.getValue() != -1

    def add_group(self, name='', parent=None, index=-1):
        """
        Add a Group node to the specified parent.

        name - name of node
        parent - parent node = top node (default)
        index - position in child list = -1m end-of-list (default)
        """

        return self.add_node(Nodes.GROUP, name, parent, index)

    def insert_node(self, node, parent=None, index=-1):
        """
        Insert an existing node into the current group default node

        node - node to insert
        parent - parent node, None = group top node (default)
        index - position in child list, -1 = end of list (default)
        """

        if parent is None:
            parent = self.top

        utils.insert_child(node, parent, index)

    def add_node(self, event_class, name='', parent=None, index=-1):
        """
        Add a new node to the current group
        """

        if not name:
            name = f'{self.name}_{str(event_class.getClassTypeId().getName())}'

        if not parent:
            parent = self.top

        return utils.add_child(event_class, parent, name, index)

    def remove_node(self, node, parent=None):
        """
        Remove an existing node from the current group's top, unless
        parent is specified
        """

        if not parent:
            parent = self.top

        utils.remove_child(node, parent)

    def copy(self):
        """
        Return a copy of the group root node
        """

        return self.root.copy()

    def remove(self):
        """
        Remove the coin group from it's parent node, return a reference to
        the root node
        """

        utils.remove_child(self.root, self.parent)

    def remove_all_children(self):
        """
        Remove all children under the top node.
        """

        self.top.removeAllChildren()

    def dump(self, node=None):
        """
        Convenience function to dump contents of CoinGroup
        """

        if node is None:
            node = self.root

        utils.dump_node(node)

    def finalize(self, parent=None):
        """
        Destroy the CoinGroup Node
        """

        _parent = parent

        if not _parent:
            _parent = self.parent

        utils.remove_child(self.root, _parent)

    def get_child(self, name, node=None):
        """
        Return a list of all children containing the specified name
        """

        if not node:
            node = self.root

        return utils.find_child_by_name(name, node)

    def get_center(self):
        """
        Return the center of the group SoTransform node as a tuple
        """

        if not self.transform:
            return

        return self.transform.center.getValue()

    def get_rotation(self):
        """
        Return the axis as a tuple and angle of rotation in radians
        """

        _result = self.transform.rotation.getValue().getAxisAngle()

        return [_result[0].getValue(), _result[1]]

    def get_translation(self):
        """
        Return the translation of the gou SoTransform node as a tuple
        """

        if not self.transform:
            return

        return self.transform.translation.getValue().getValue()

    def set_translation(self, point):
        """
        Set the translation of the group SoTransform node
        """

        if not self.transform:
            return

        self.transform.translation.setValue(point)

    def set_center(self, point):
        """
        Set the center point of the group SoTransform node
        point - center point as a tuple
        """

        if not self.transform:
            return

        self.transform.center.setValue(point)

    def set_rotation(self, angle=None, center=None):
        """
        Set the rotation of the group SoTransform node
        """

        if not self.transform:
            return

        if center is None:
            center = self.get_center

        if angle is None:
            angle = self.get_rotation()[1]

        self.transform.rotation = utils.get_rotation(angle)
        self.transform.rotation.center = center

    def transform_points(self, points, viewport=None, matrix=None):
        """
        Transform points using provided parametres.  If none, uses matrix
        from existing transform
        """

        if not matrix:

            if not viewport:
                return points

            matrix = self.get_view_matrix(viewport, self.transform)

        return utils.transform_points(points, matrix)

    def get_matrix(self,
        translation=(0.0, 0.0, 0.0), axis=(0.0, 0.0, 1.0), angle=0.0):
        """
        Return a matrix defined by the passed parameters
        """

        return utils.create_matrix(translation, axis=axis, angle=angle)

    def get_view_matrix(self, viewport, node=None):
        """
        Return the transformation matrix at the Transform node
        """

        if not node:
            node = self.root

        return utils.get_matrix(node, viewport)

    def copy_matrix(self, node, viewport):
        """
        Copy the matrix from the transform node to the target
        """

        _node = node

        if isinstance(node, CoinGroup):
            _node = node.transform

        utils.copy_matrix(self.transform, node, viewport)

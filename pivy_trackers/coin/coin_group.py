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

from . import coin_utils as utils
from .coin_enums import NodeTypes as Nodes

class CoinGroup(object):
    """
    Basic coin scenegraph node structure for use with trackers
    """

    scenegraph_root = None

    def __init__(self, is_separated=False, is_switched=False,
                 switch_first=True, parent=None, name=''):
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

        _top_group = None

        if is_switched:
            self.switch = utils.add_child(
                Nodes.SWITCH, None, self.name + '__Switch')

            self.root = self.switch

        if is_separated:
            self.separator = utils.add_child(
                Nodes.SEPARATOR, None, self.name + '__TopSeparator')

            _top_group = self.separator

        else:
            self.group = utils.add_child(
                Nodes.GROUP, None, self.name + '__TopGroup')

            _top_group = self.group

        self.top = _top_group

        if not self.root:
            self.root = self.top

        else:
            if not switch_first:
                self.top, self.root = self.root, self.top

            self.root.addChild(self.top)

        if not self.parent:
            return

        if isinstance(self.parent, CoinGroup):
            self.parent = self.parent.top

        else:
            assert (isinstance(self.parent, Nodes.NODE)),\
                'CoinGroup parent not of CoinGroup or SoNode type'

        utils.insert_child(self.root, self.parent)

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
            return False

        return self.switch.whichChild.getValue() == 0

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

    def add_node(self, event_class, name='', index=-1):
        """
        Add a new node to the current group
        """

        if not name:
            name = str(event_class.getClassTypeId().getName())

        _name = self.name + '__' + name

        return utils.add_child(event_class, self.top, _name, index)

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

    def dump(self):
        """
        Convenience function to dump contents of CoinGroup
        """

        utils.dump_node(self.root)

    def finalize(self, parent=None):
        """
        Destroy the CoinGroup Node
        """

        _parent = parent

        if not _parent:
            _parent = self.parent

        utils.remove_child(self.root, _parent)

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
            angle = self.get_rotation[1]

        self.transform.rotation = utils.get_rotation(angle)
        self.transform.rotation.center = center

    def get_matrix(self, viewport, node=None):
        """
        Return the transformation matrix at the Transform node
        """

        if not node:
            node = self.root

        return utils.get_matrix(self.root, viewport)

    def copy_matrix(self, node, viewport):
        """
        Copy the matrix from the transform node to the target
        """

        _node = node

        if isinstance(node, CoinGroup):
            _node = node.transform

        print('coin_group.copy_matrix()\n',self.transform)
        print(self.transform.translation.getValue().getValue())
    
        utils.copy_matrix(self.transform, node, viewport)

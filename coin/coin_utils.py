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
General utilities for pivy.coin objects
"""
import math

from ..support.core.const import Const

from pivy import coin

from .todo import todo

from pivy_trackers import GEO_SUPPORT

from .coin_enums import MarkerStyles

_NEAR_ZERO = 10**-30

class Describe(Const):
    """
    Describe nodes
    """

    def __init__(self):
        """
        Constructor
        """

        self.node_points = lambda n:\
            [_v.getValue for _v in n.point.getValues()]

        _pts = lambda n: [_v.getValue for _v in n.point.getValues()]

        self.format = {
            coin.SoGroup: lambda n: str(n.getNumChildren()),

            coin.SoSwitch: lambda n:
                f'{str(n.getNumChildren())}/{str(n.whichChild.getValue())}',

            coin.SoCoordinate3: lambda n:
                f'points ({str(n.point.getNum())}) = {str(_pts(n))}',

            coin.SoGeoCoordinate3: lambda n:
                f"""
                    system = {str(n.geoSystem.getValues())}; points ({str(n.point.getNum())}) = {str(_pts(n))}'
                """,

            coin.SoDrawStyle: lambda n:
                f"""
                    style={str(n.style.get())}, size={str(n.pointSize.getValue())}, width={str(n.lineWidth.getValue())}, pattern={hex(n.linePattern.getValue())}
                """,

            coin.SoMarkerset: lambda n:
                f'shape={str(MarkerStyles.get_by_value(n.markerIndex))}',

            coin.SoFont: lambda n:
                f'name={n.name.getValue()}, size={str(n.size.getValue())}',

            coin.SoText2: lambda n: f'text={n.string.getValue()}',

            coin.SoTransform: lambda n:
                f"""
                    translation={str(n.translation.getValue().getValue())}; rotation=<{str(n.rotation.getValue().getAxisAngle()[0].getValue())}>, {str(n.rotation.getValue().getAxisAngle()[1].getValue())} rad; center={str(n.center.getValue().getValue())}
                """,

            coin.SoGeoOrigin: lambda n:
                f"""
                    system={str(n.geoSystem.getValues())}; coordinates={str(n.geoCoords.getValue().getValue())}
                """
        }

        def apply(self, node):
            """
            Apply formatting to the target node
            """


def describe(node):
    """
    Returns a string describing the node and selected attributes
    """

    if isinstance(node, coin.SoGroup):

        _suffix = '{}'.format(str(node.getNumChildren()))

        if isinstance(node, coin.SoSwitch):
            _suffix += '/{}'.format(str(node.whichChild.getValue()))

        return _suffix

    if isinstance(node, coin.SoCoordinate3):

        _pts = [_v.getValue() for _v in node.point.getValues()]

        return 'points ({}) = {}'\
            .format(str(node.point.getNum()), str(_pts))


    if GEO_SUPPORT:

        if isinstance(node, coin.SoGeoCoordinate):

            _pts = [_v.getValue() for _v in node.point.getValues()]

            return 'system = {}; points ({}) = {}'.format(
                str(node.geoSystem.getValues()), str(node.point.getNum()), str(_pts)
            )

    if isinstance(node, coin.SoDrawStyle):
        return 'style={}, size={}, width={}, pattern={}'\
            .format(
                str(node.style.get()), str(node.pointSize.getValue()),
                str(node.lineWidth.getValue()),
                hex(node.linePattern.getValue())
            )

    if isinstance(node, coin.SoMarkerSet):
        return 'shape={}'.format(MarkerStyles.get_by_value(node.markerIndex))

    if isinstance(node, coin.SoFont):
        return 'name={}, size={}'\
            .format(node.name.getValue(), str(node.size.getValue()))

    if isinstance(node, coin.SoText2):
        return 'text={}'.format(str(node.string.getValues()))

    if isinstance(node, coin.SoTransform):
        return 'translation={}; rotation=<{}>, {} rad; center={}'.format(
            str(node.translation.getValue().getValue()),
            str(node.rotation.getValue().getAxisAngle()[0].getValue()),
            str(node.rotation.getValue().getAxisAngle()[1]),
            str(node.center.getValue().getValue())
        )

    if GEO_SUPPORT:

        if isinstance(node, coin.SoGeoOrigin):
            return 'system={}; coordinates={}'.format(
                str(node.geoSystem.getValues()),
                str(node.geoCoords.getValue().getValue()))

    return ''

def get_matrix(node, viewport):
    """
    Return the transformation matrix applied to the node
    """

    _action = coin.SoGetMatrixAction(viewport)

    node.getMatrix(_action)

    return _action.getMatrix()

def copy_matrix(source, destination, viewport):
    """
    Copy the transformation matrix from the source to the destination
    """

    destination.setMatrix(get_matrix(source, viewport))

def dump_node(node, indent=''):
    """
    Dump a formatted output of sceneegraph node structure to console
    """

    assert (node),\
        'coin_utils.dump_node():NoneType passed as node.'

    _indent = indent

    if _indent:
        _indent += '---'

    _prefix = indent + '\n' + _indent
    _title = str(node.getName())
    _suffix = ' (' + describe(node) + ')'

    print(_prefix + _title + _suffix)

    if not isinstance(node, coin.SoGroup):
        return

    for _i in range(0, node.getNumChildren()):
        dump_node(node.getChild(_i), indent + '   |')

def search(node, parent):
    """
    Returns a search action
    """
    _sa = coin.SoSearchAction()
    _sa.setNode(node)
    _sa.apply(parent)

    return _sa

def remove_child(node, parent):
    """
    Convenience wrapper for _remove_node
    """

    if parent.findChild(node) >= 0:
        todo.delay(parent.removeChild, node)

def insert_child(node, parent, index=-1):
    """
    Insert a node as a child of the passed node
    """

    _fn = parent.addChild

    if index >= 0:
        _fn = lambda _x: parent.insertChild(_x, index)

    todo.delay(_fn, node)

def add_child(event_class, parent, name='', index=-1):
    """
    Node creation/insertion function

    event_class - event class or NodeTypes enumerator
    parent - if None, returns created node without inserting it
    name - string name
    index - position in parent in which to insert, -1 = end
    """

    _name = name

    if _name == '':
        _name = str(event_class.getClassTypeId().getName())

    _node = event_class()

    if hasattr(_node, 'setName'):
        _node.setName(_name)

    if parent:
        insert_child(_node, parent, index)

    return _node

def find_child_by_name(name, node):
    """
    Return a list of all children containing the specified name
    """

    #define the search path
    _search = coin.SoSearchAction()
    _search.setName(name)
    _search.apply(node)

    _path = _search.getPath()

    if not _path:
        return None

    return _path.getTail()

def get_rotation(angle, axis=(0.0, 0.0, 1.0)):
    """
    Return a coin SbRotation object based on the passed center and angle.
    center - the center point as a tuple
    angle - then angle in radians
    """

    return coin.SbRotation(coin.SbVec3f(axis), angle)

def create_matrix(translation=(0.0, 0.0, 0.0), angle=0.0, axis=(0.0, 0.0, 1.0)):
    """
    Generate a Coin3D matrix based on the passed parameters
    """

    _rot = get_rotation(angle, axis)

    _mat = coin.SbMatrix()
    _mat.setRotate(_rot)

    _mat.setTranslate(coin.SbVec3f(translation))

    return _mat

def toggle_switch(switch, toggle_all=False, index=-3):
    """
    Toggle a switch between off (-1) and on (-3 or >-1)
    """
    #PyLint doesn't detect getValue()
    #pylint: disable=no-member

    if switch.whichChild.getValue() == -1:
        switch.whichChild = index

    else:
        switch.whichChild = -1

def transform_points(points, matrix):
    """
    Transform selected points by the transformation matrix
    """

    #store the view state matrix if a valid node is passed.
    #subsequent calls with null node will re-use the last valid node matrix

    _matrix = matrix

    if _matrix is None:
        return points

    _xlate = _matrix.getValue()[3]

    if any(math.isnan(_v) for _v in _xlate):
        return points

    if all([_v < _NEAR_ZERO for _v in _xlate]):
        return points

    #append fourth point to each coordinate
    _pts = [_v + (1.0,) for _v in points]

    _s = 0
    _result = []
    _l = len(_pts)

    #iterate the list, processing it in sets of four coordinates at a time
    while _s < _l:

        _mat_pts = _pts[_s:_s + 4]

        _last_point = len(_mat_pts)

        #pad the list if less than four points
        for _i in range(len(_mat_pts), 4):
            _mat_pts.append((0.0, 0.0, 0.0, 1.0))

        #convert and transform
        _mat = coin.SbMatrix(_mat_pts)

        for _v in _mat.multRight(_matrix).getValue()[:_last_point]:
            _result.append(tuple(_v)[0:3])

        _s += 4

    return _result
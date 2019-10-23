# -*- coding: utf-8 -*-
#***********************************************************************
#*                                                                     *
#* Copyright (c) 2018 Joel Graff <monograff76@gmail.com>               *
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
Module for spatial / vector calculation routines
"""

import math

from pivy import coin

from .coin_enums import Axis

_COIN_MATH_TWO_PI = math.pi * 2.0

def get_rotation_dir(from_vector, to_vector=Axis.Z):
    """
    Returns the rotation angle between two 3D vectors as a signed integer:
    1 = cw, -1 = ccw, 0 = fail

    Vectors sepcified as tuples
    """

    if len(from_vector) != 3:
        return 0

    if len(to_vector) != len(from_vector):
        return 0

    _from = coin.SbVec3f(from_vector)
    _to = coin.SbVec3f(to_vector)

    return -1 * math.copysign(1, _from.cross(_to).getValue()[2])

def get_rotation_angle(from_vector, to_vector):
    """
    Calculate the SbRotation between two vectors, specified as tuples
    """

    _from = coin.SbVec3f(from_vector)
    _to = coin.SbVec3f(to_vector)

    _angle = 0.0

    _rot = coin.SbRotation(_from, _to)
    return _rot.getAxisAngle()[1]

def get_bearing(vector, reference=Axis.Y):
    """
    Returns the absolute bearing of the passed vector.

    Bearing is measured clockwise from +y 'north' (0,1,0)
    Vector is a coordinate or a vector as a tuple
    """

    rot_dir = get_rotation_dir(reference, vector)
    angle = rot_dir * get_rotation_angle(reference, vector)

    if angle < 0.0:
        angle += _COIN_MATH_TWO_PI

    return angle

def normalize_angle(angle):
    """
    Normalize the provided angle (radians) between -pi and +pi
    """

    _factor = angle / math.pi
    _scale = int(_factor / 2.0)
    _nfactor = _factor - (_scale*2.0)

    if _nfactor < -1.0:
        _nfactor += 2.0

    elif _nfactor > 1.0:
        _nfactor -= 2.0

    return _nfactor * (angle/_factor)

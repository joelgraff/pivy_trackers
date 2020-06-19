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
Coin-based enumerations
"""

from freecad_python_support.const import Const

from pivy import coin

class Axis(Const):
    """
    Tuple definitions of unit axes
    """

    X = (1.0, 0.0, 0.0)
    Y = (0.0, 1.0, 0.0)
    Z = (0.0, 0.0, 1.0)
    XY = (1.0, 1.0, 0.0)
    YZ = (0.0, 1.0, 1.0)
    XZ = (1.0, 0.0, 1.0)

class InputEvent(Const):
    """
    Mouse state event constant enumerants
    """
    LOCATION2 = coin.SoLocation2Event.getClassTypeId()
    MOUSE_BUTTON = coin.SoMouseButtonEvent.getClassTypeId()
    KEYBOARD = coin.SoKeyboardEvent.getClassTypeId()

class FontStyles(Const):
    """
    SoFont style enumerants
    """

    NORMAL = ''
    BOLD = 'Bold'
    ITALIC = 'Italic'
    BOLD_ITALIC = 'Bold Italic'

class PickStyles(Const):
    """
    SoPickStyle enumerants
    """

    UNPICKABLE = coin.SoPickStyle.UNPICKABLE
    SHAPE = coin.SoPickStyle.SHAPE
    BOX = coin.SoPickStyle.BOUNDING_BOX
    SHAPE_ON_TOP = coin.SoPickStyle.SHAPE_ON_TOP
    BOX_ON_TOP = coin.SoPickStyle.BOUNDING_BOX_ON_TOP
    FACES = coin.SoPickStyle.SHAPE_FRONTFACES


class Keys(Const):
    """
    Enumerants for Coin3D trappable keys for SoKeyboardEvent
    """

    ANY = coin.SoKeyboardEvent.ANY
    UNDEFINED = coin.SoKeyboardEvent.UNDEFINED
    LEFT_SHIFT = coin.SoKeyboardEvent.LEFT_SHIFT
    RIGHT_SHIFT = coin.SoKeyboardEvent.RIGHT_SHIFT
    LEFT_CONTROL = coin.SoKeyboardEvent.LEFT_CONTROL
    RIGHT_CONTROL = coin.SoKeyboardEvent.RIGHT_CONTROL
    LEFT_ALT = coin.SoKeyboardEvent.LEFT_ALT
    RIGHT_ALT = coin.SoKeyboardEvent.RIGHT_ALT
    NUMBER_0 = coin.SoKeyboardEvent.NUMBER_0
    NUMBER_1 = coin.SoKeyboardEvent.NUMBER_1
    NUMBER_2 = coin.SoKeyboardEvent.NUMBER_2
    NUMBER_3 = coin.SoKeyboardEvent.NUMBER_3
    NUMBER_4 = coin.SoKeyboardEvent.NUMBER_4
    NUMBER_5 = coin.SoKeyboardEvent.NUMBER_5
    NUMBER_6 = coin.SoKeyboardEvent.NUMBER_6
    NUMBER_7 = coin.SoKeyboardEvent.NUMBER_7
    NUMBER_8 = coin.SoKeyboardEvent.NUMBER_8
    NUMBER_9 = coin.SoKeyboardEvent.NUMBER_9
    A = coin.SoKeyboardEvent.A
    B = coin.SoKeyboardEvent.B
    C = coin.SoKeyboardEvent.C
    D = coin.SoKeyboardEvent.D
    E = coin.SoKeyboardEvent.E
    F = coin.SoKeyboardEvent.F
    G = coin.SoKeyboardEvent.G
    H = coin.SoKeyboardEvent.H
    I = coin.SoKeyboardEvent.I
    J = coin.SoKeyboardEvent.J
    K = coin.SoKeyboardEvent.K
    L = coin.SoKeyboardEvent.L
    M = coin.SoKeyboardEvent.M
    N = coin.SoKeyboardEvent.N
    O = coin.SoKeyboardEvent.O
    P = coin.SoKeyboardEvent.P
    Q = coin.SoKeyboardEvent.Q
    R = coin.SoKeyboardEvent.R
    S = coin.SoKeyboardEvent.S
    T = coin.SoKeyboardEvent.T
    U = coin.SoKeyboardEvent.U
    V = coin.SoKeyboardEvent.V
    W = coin.SoKeyboardEvent.W
    X = coin.SoKeyboardEvent.X
    Y = coin.SoKeyboardEvent.Y
    Z = coin.SoKeyboardEvent.Z
    HOME = coin.SoKeyboardEvent.HOME
    LEFT_ARROW = coin.SoKeyboardEvent.LEFT_ARROW
    UP_ARROW = coin.SoKeyboardEvent.UP_ARROW
    RIGHT_ARROW = coin.SoKeyboardEvent.RIGHT_ARROW
    DOWN_ARROW = coin.SoKeyboardEvent.DOWN_ARROW
    PAGE_UP = coin.SoKeyboardEvent.PAGE_UP
    PAGE_DOWN = coin.SoKeyboardEvent.PAGE_DOWN
    END = coin.SoKeyboardEvent.END
    PRIOR = coin.SoKeyboardEvent.PRIOR
    NEXT = coin.SoKeyboardEvent.NEXT
    PAD_ENTER = coin.SoKeyboardEvent.PAD_ENTER
    PAD_F1 = coin.SoKeyboardEvent.PAD_F1
    PAD_F2 = coin.SoKeyboardEvent.PAD_F2
    PAD_F3 = coin.SoKeyboardEvent.PAD_F3
    PAD_F4 = coin.SoKeyboardEvent.PAD_F4
    PAD_0 = coin.SoKeyboardEvent.PAD_0
    PAD_1 = coin.SoKeyboardEvent.PAD_1
    PAD_2 = coin.SoKeyboardEvent.PAD_2
    PAD_3 = coin.SoKeyboardEvent.PAD_3
    PAD_4 = coin.SoKeyboardEvent.PAD_4
    PAD_5 = coin.SoKeyboardEvent.PAD_5
    PAD_6 = coin.SoKeyboardEvent.PAD_6
    PAD_7 = coin.SoKeyboardEvent.PAD_7
    PAD_8 = coin.SoKeyboardEvent.PAD_8
    PAD_9 = coin.SoKeyboardEvent.PAD_9
    PAD_ADD = coin.SoKeyboardEvent.PAD_ADD
    PAD_SUBTRACT = coin.SoKeyboardEvent.PAD_SUBTRACT
    PAD_MULTIPLY = coin.SoKeyboardEvent.PAD_MULTIPLY
    PAD_DIVIDE = coin.SoKeyboardEvent.PAD_DIVIDE
    PAD_SPACE = coin.SoKeyboardEvent.PAD_SPACE
    PAD_TAB = coin.SoKeyboardEvent.PAD_TAB
    PAD_INSERT = coin.SoKeyboardEvent.PAD_INSERT
    PAD_DELETE = coin.SoKeyboardEvent.PAD_DELETE
    PAD_PERIOD = coin.SoKeyboardEvent.PAD_PERIOD
    F1 = coin.SoKeyboardEvent.F1
    F2 = coin.SoKeyboardEvent.F2
    F3 = coin.SoKeyboardEvent.F3
    F4 = coin.SoKeyboardEvent.F4
    F5 = coin.SoKeyboardEvent.F5
    F6 = coin.SoKeyboardEvent.F6
    F7 = coin.SoKeyboardEvent.F7
    F8 = coin.SoKeyboardEvent.F8
    F9 = coin.SoKeyboardEvent.F9
    F10 = coin.SoKeyboardEvent.F10
    F11 = coin.SoKeyboardEvent.F11
    F12 = coin.SoKeyboardEvent.F12
    BACKSPACE = coin.SoKeyboardEvent.BACKSPACE
    TAB = coin.SoKeyboardEvent.TAB
    RETURN = coin.SoKeyboardEvent.RETURN
    ENTER = coin.SoKeyboardEvent.ENTER
    PAUSE = coin.SoKeyboardEvent.PAUSE
    SCROLL_LOCK = coin.SoKeyboardEvent. SCROLL_LOCK
    ESCAPE = coin.SoKeyboardEvent.ESCAPE
    DELETE = coin.SoKeyboardEvent.DELETE
    KEY_DELETE = coin.SoKeyboardEvent.DELETE
    PRINT = coin.SoKeyboardEvent. PRINT
    INSERT = coin.SoKeyboardEvent.INSERT
    NUM_LOCK = coin.SoKeyboardEvent.NUM_LOCK
    CAPS_LOCK = coin.SoKeyboardEvent.CAPS_LOCK
    SHIFT_LOCK = coin.SoKeyboardEvent.SHIFT_LOCK
    SPACE = coin.SoKeyboardEvent.SPACE
    APOSTROPHE = coin.SoKeyboardEvent.APOSTROPHE
    COMMA = coin.SoKeyboardEvent.COMMA
    MINUS = coin.SoKeyboardEvent.MINUS
    PERIOD = coin.SoKeyboardEvent.PERIOD
    SLASH = coin.SoKeyboardEvent.SLASH
    SEMICOLON = coin.SoKeyboardEvent.SEMICOLON
    EQUAL = coin.SoKeyboardEvent.EQUAL
    BRACKETLEFT = coin.SoKeyboardEvent.BRACKETLEFT
    BACKSLASH = coin.SoKeyboardEvent.BACKSLASH
    BRACKETRIGHT = coin.SoKeyboardEvent.BRACKETRIGHT
    GRAVE = coin.SoKeyboardEvent.GRAVE

    #def __str__(self):
    #    """
    #    Stringify
    #    """

    #    return coin.

class MarkerStyles(Const):
    """
    Const class of enumerants for coin SoMarkerSet.SoMarkerType
    """

    NONE = coin.SoMarkerSet.NONE

    #size 5
    CROSS_5 = coin.SoMarkerSet.CROSS_5_5
    PLUS_5 = coin.SoMarkerSet.PLUS_5_5
    MINUS_5 = coin.SoMarkerSet.MINUS_5_5
    SLASH_5 = coin.SoMarkerSet.SLASH_5_5
    BACKSLASH_5 = coin.SoMarkerSet.BACKSLASH_5_5
    BAR_5 = coin.SoMarkerSet.BAR_5_5
    STAR_5 = coin.SoMarkerSet.STAR_5_5
    Y_5 = coin.SoMarkerSet.Y_5_5
    LIGHTNING_5 = coin.SoMarkerSet.LIGHTNING_5_5
    WELL_5 = coin.SoMarkerSet.WELL_5_5
    CIRCLE_LINE_5 = coin.SoMarkerSet.CIRCLE_LINE_5_5
    SQUARE_LINE_5 = coin.SoMarkerSet.SQUARE_LINE_5_5
    DIAMOND_LINE_5 = coin.SoMarkerSet.DIAMOND_LINE_5_5
    TRIANGLE_LINE_5 = coin.SoMarkerSet.TRIANGLE_LINE_5_5
    RHOMBUS_LINE_5 = coin.SoMarkerSet.RHOMBUS_LINE_5_5
    HOURGLASS_LINE_5 = coin.SoMarkerSet.HOURGLASS_LINE_5_5
    SATELLITE_LINE_5 = coin.SoMarkerSet.SATELLITE_LINE_5_5
    PINE_TREE_LINE_5 = coin.SoMarkerSet.PINE_TREE_LINE_5_5
    CAUTION_LINE_5 = coin.SoMarkerSet.CAUTION_LINE_5_5
    SHIP_LINE_5 = coin.SoMarkerSet.SHIP_LINE_5_5
    CIRCLE_FILLED_5 = coin.SoMarkerSet.CIRCLE_FILLED_5_5
    SQUARE_FILLED_5 = coin.SoMarkerSet.SQUARE_FILLED_5_5
    DIAMOND_FILLED_5 = coin.SoMarkerSet.DIAMOND_FILLED_5_5
    TRIANGLE_FILLED_5 = coin.SoMarkerSet.TRIANGLE_FILLED_5_5
    RHOMBUS_FILLED_5 = coin.SoMarkerSet.RHOMBUS_FILLED_5_5
    HOURGLASS_FILLED_5 = coin.SoMarkerSet.HOURGLASS_FILLED_5_5
    SATELLITE_FILLED_5 = coin.SoMarkerSet.SATELLITE_FILLED_5_5
    PINE_TREE_FILLED_5 = coin.SoMarkerSet.PINE_TREE_FILLED_5_5
    CAUTION_FILLED_5 = coin.SoMarkerSet.CAUTION_FILLED_5_5
    SHIP_FILLED_5 = coin.SoMarkerSet.SHIP_FILLED_5_5

    #size 7
    CROSS_7 = coin.SoMarkerSet.CROSS_7_7
    PLUS_7 = coin.SoMarkerSet.PLUS_7_7
    MINUS_7 = coin.SoMarkerSet.MINUS_7_7
    SLASH_7 = coin.SoMarkerSet.SLASH_7_7
    BACKSLASH_7 = coin.SoMarkerSet.BACKSLASH_7_7
    BAR_7 = coin.SoMarkerSet.BAR_7_7
    STAR_7 = coin.SoMarkerSet.STAR_7_7
    Y_7 = coin.SoMarkerSet.Y_7_7
    LIGHTNING_7 = coin.SoMarkerSet.LIGHTNING_7_7
    WELL_7 = coin.SoMarkerSet.WELL_7_7
    CIRCLE_LINE_7 = coin.SoMarkerSet.CIRCLE_LINE_7_7
    SQUARE_LINE_7 = coin.SoMarkerSet.SQUARE_LINE_7_7
    DIAMOND_LINE_7 = coin.SoMarkerSet.DIAMOND_LINE_7_7
    TRIANGLE_LINE_7 = coin.SoMarkerSet.TRIANGLE_LINE_7_7
    RHOMBUS_LINE_7 = coin.SoMarkerSet.RHOMBUS_LINE_7_7
    HOURGLASS_LINE_7 = coin.SoMarkerSet.HOURGLASS_LINE_7_7
    SATELLITE_LINE_7 = coin.SoMarkerSet.SATELLITE_LINE_7_7
    PINE_TREE_LINE_7 = coin.SoMarkerSet.PINE_TREE_LINE_7_7
    CAUTION_LINE_7 = coin.SoMarkerSet.CAUTION_LINE_7_7
    SHIP_LINE_7 = coin.SoMarkerSet.SHIP_LINE_7_7
    CIRCLE_FILLED_7 = coin.SoMarkerSet.CIRCLE_FILLED_7_7
    SQUARE_FILLED_7 = coin.SoMarkerSet.SQUARE_FILLED_7_7
    DIAMOND_FILLED_7 = coin.SoMarkerSet.DIAMOND_FILLED_7_7
    TRIANGLE_FILLED_7 = coin.SoMarkerSet.TRIANGLE_FILLED_7_7
    RHOMBUS_FILLED_7 = coin.SoMarkerSet.RHOMBUS_FILLED_7_7
    HOURGLASS_FILLED_7 = coin.SoMarkerSet.HOURGLASS_FILLED_7_7
    SATELLITE_FILLED_7 = coin.SoMarkerSet.SATELLITE_FILLED_7_7
    PINE_TREE_FILLED_7 = coin.SoMarkerSet.PINE_TREE_FILLED_7_7
    CAUTION_FILLED_7 = coin.SoMarkerSet.CAUTION_FILLED_7_7
    SHIP_FILLED_7 = coin.SoMarkerSet.SHIP_FILLED_7_7

    #size 9
    CROSS_9 = coin.SoMarkerSet.CROSS_9_9
    PLUS_9 = coin.SoMarkerSet.PLUS_9_9
    MINUS_9 = coin.SoMarkerSet.MINUS_9_9
    SLASH_9 = coin.SoMarkerSet.SLASH_9_9
    BACKSLASH_9 = coin.SoMarkerSet.BACKSLASH_9_9
    BAR_9 = coin.SoMarkerSet.BAR_9_9
    STAR_9 = coin.SoMarkerSet.STAR_9_9
    Y_9 = coin.SoMarkerSet.Y_9_9
    LIGHTNING_9 = coin.SoMarkerSet.LIGHTNING_9_9
    WELL_9 = coin.SoMarkerSet.WELL_9_9
    CIRCLE_LINE_9 = coin.SoMarkerSet.CIRCLE_LINE_9_9
    SQUARE_LINE_9 = coin.SoMarkerSet.SQUARE_LINE_9_9
    DIAMOND_LINE_9 = coin.SoMarkerSet.DIAMOND_LINE_9_9
    TRIANGLE_LINE_9 = coin.SoMarkerSet.TRIANGLE_LINE_9_9
    RHOMBUS_LINE_9 = coin.SoMarkerSet.RHOMBUS_LINE_9_9
    HOURGLASS_LINE_9 = coin.SoMarkerSet.HOURGLASS_LINE_9_9
    SATELLITE_LINE_9 = coin.SoMarkerSet.SATELLITE_LINE_9_9
    PINE_TREE_LINE_9 = coin.SoMarkerSet.PINE_TREE_LINE_9_9
    CAUTION_LINE_9 = coin.SoMarkerSet.CAUTION_LINE_9_9
    SHIP_LINE_9 = coin.SoMarkerSet.SHIP_LINE_9_9
    CIRCLE_FILLED_9 = coin.SoMarkerSet.CIRCLE_FILLED_9_9
    SQUARE_FILLED_9 = coin.SoMarkerSet.SQUARE_FILLED_9_9
    DIAMOND_FILLED_9 = coin.SoMarkerSet.DIAMOND_FILLED_9_9
    TRIANGLE_FILLED_9 = coin.SoMarkerSet.TRIANGLE_FILLED_9_9
    RHOMBUS_FILLED_9 = coin.SoMarkerSet.RHOMBUS_FILLED_9_9
    HOURGLASS_FILLED_9 = coin.SoMarkerSet.HOURGLASS_FILLED_9_9
    SATELLITE_FILLED_9 = coin.SoMarkerSet.SATELLITE_FILLED_9_9
    PINE_TREE_FILLED_9 = coin.SoMarkerSet.PINE_TREE_FILLED_9_9
    CAUTION_FILLED_9 = coin.SoMarkerSet.CAUTION_FILLED_9_9
    SHIP_FILLED_9 = coin.SoMarkerSet.SHIP_FILLED_9_9

    #no @staticmethod decorator or self argument for Const object methods
    def get(shape, size): # lgtm[py/not-named-self]
        """
        Convenience function to get marker index using shape / size arguments
        """
        #pylint: disable=no-self-argument

        return MarkerStyles.__dict__.get(shape.upper() + '_' + str(size))

    def get_by_value(value): # lgtm[py/not-named-self]
        """
        Return the marker name using the markerIndex value
        """
        #pylint: disable=no-self-argument

        if isinstance(value, coin.SoMFInt32):
            value = value.getValues()[0]

        _vals = list(MarkerStyles.__dict__.values())
        _keys = list(MarkerStyles.__dict__.keys())

        if value in _vals:
            return _keys[_vals.index(value)]

        return ''


class NodeTypes(Const):
    """
    Const class of enumerants correlating to coin node types
    """

    COLOR = coin.SoBaseColor
    COORDINATE = coin.SoCoordinate3
    DRAW_STYLE = coin.SoDrawStyle
    EVENT_CB = coin.SoEventCallback
    FONT = coin.SoFont
    GEO_COORDINATE = coin.SoGeoCoordinate
    GEO_ORIGIN = coin.SoGeoOrigin
    GEO_SEPARATOR = coin.SoGeoSeparator
    GROUP = coin.SoGroup
    KEYBOARD_EVENT = coin.SoKeyboardEvent
    LINE_SET = coin.SoLineSet
    MARKER_SET = coin.SoMarkerSet
    NODE = coin.SoNode
    PICK_STYLE = coin.SoPickStyle
    SWITCH = coin.SoSwitch
    SEPARATOR = coin.SoSeparator
    TEXT = coin.SoText2
    TRANSFORM = coin.SoTransform
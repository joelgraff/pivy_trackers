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

from typing import Final

from pivy import coin

from ..support.core.const import Const
from pivy_trackers import GEO_SUPPORT

class Axis(Const):
    """
    Tuple definitions of unit axes
    """

    X: Final = (1.0, 0.0, 0.0)
    Y: Final = (0.0, 1.0, 0.0)
    Z: Final = (0.0, 0.0, 1.0)
    XY: Final = (1.0, 1.0, 0.0)
    YZ: Final = (0.0, 1.0, 1.0)
    XZ: Final = (1.0, 0.0, 1.0)

class InputEvent(Const):
    """
    Mouse state event constant enumerants
    """
    LOCATION2: Final = coin.SoLocation2Event.getClassTypeId()
    MOUSE_BUTTON: Final = coin.SoMouseButtonEvent.getClassTypeId()
    KEYBOARD: Final = coin.SoKeyboardEvent.getClassTypeId()

class FontStyles(Const):
    """
    SoFont style enumerants
    """

    NORMAL: Final = ''
    BOLD: Final = 'Bold'
    ITALIC: Final = 'Italic'
    BOLD_ITALIC: Final = 'Bold Italic'

class PickStyles(Const):
    """
    SoPickStyle enumerants
    """

    UNPICKABLE: Final = coin.SoPickStyle.UNPICKABLE
    SHAPE: Final = coin.SoPickStyle.SHAPE
    BOX: Final = coin.SoPickStyle.BOUNDING_BOX
    SHAPE_ON_TOP: Final = coin.SoPickStyle.SHAPE_ON_TOP
    BOX_ON_TOP: Final = coin.SoPickStyle.BOUNDING_BOX_ON_TOP
    FACES: Final = coin.SoPickStyle.SHAPE_FRONTFACES


class Keys(Const):
    """
    Enumerants for Coin3D trappable keys for SoKeyboardEvent
    """

    ANY: Final = coin.SoKeyboardEvent.ANY
    UNDEFINED: Final = coin.SoKeyboardEvent.UNDEFINED
    LEFT_SHIFT: Final = coin.SoKeyboardEvent.LEFT_SHIFT
    RIGHT_SHIFT: Final = coin.SoKeyboardEvent.RIGHT_SHIFT
    LEFT_CONTROL: Final = coin.SoKeyboardEvent.LEFT_CONTROL
    RIGHT_CONTROL: Final = coin.SoKeyboardEvent.RIGHT_CONTROL
    LEFT_ALT: Final = coin.SoKeyboardEvent.LEFT_ALT
    RIGHT_ALT: Final = coin.SoKeyboardEvent.RIGHT_ALT
    NUMBER_0: Final = coin.SoKeyboardEvent.NUMBER_0
    NUMBER_1: Final = coin.SoKeyboardEvent.NUMBER_1
    NUMBER_2: Final = coin.SoKeyboardEvent.NUMBER_2
    NUMBER_3: Final = coin.SoKeyboardEvent.NUMBER_3
    NUMBER_4: Final = coin.SoKeyboardEvent.NUMBER_4
    NUMBER_5: Final = coin.SoKeyboardEvent.NUMBER_5
    NUMBER_6: Final = coin.SoKeyboardEvent.NUMBER_6
    NUMBER_7: Final = coin.SoKeyboardEvent.NUMBER_7
    NUMBER_8: Final = coin.SoKeyboardEvent.NUMBER_8
    NUMBER_9: Final = coin.SoKeyboardEvent.NUMBER_9
    A: Final = coin.SoKeyboardEvent.A
    B: Final = coin.SoKeyboardEvent.B
    C: Final = coin.SoKeyboardEvent.C
    D: Final = coin.SoKeyboardEvent.D
    E: Final = coin.SoKeyboardEvent.E
    F: Final = coin.SoKeyboardEvent.F
    G: Final = coin.SoKeyboardEvent.G
    H: Final = coin.SoKeyboardEvent.H
    I: Final = coin.SoKeyboardEvent.I
    J: Final = coin.SoKeyboardEvent.J
    K: Final = coin.SoKeyboardEvent.K
    L: Final = coin.SoKeyboardEvent.L
    M: Final = coin.SoKeyboardEvent.M
    N: Final = coin.SoKeyboardEvent.N
    O: Final = coin.SoKeyboardEvent.O
    P: Final = coin.SoKeyboardEvent.P
    Q: Final = coin.SoKeyboardEvent.Q
    R: Final = coin.SoKeyboardEvent.R
    S: Final = coin.SoKeyboardEvent.S
    T: Final = coin.SoKeyboardEvent.T
    U: Final = coin.SoKeyboardEvent.U
    V: Final = coin.SoKeyboardEvent.V
    W: Final = coin.SoKeyboardEvent.W
    X: Final = coin.SoKeyboardEvent.X
    Y: Final = coin.SoKeyboardEvent.Y
    Z: Final = coin.SoKeyboardEvent.Z
    HOME: Final = coin.SoKeyboardEvent.HOME
    LEFT_ARROW: Final = coin.SoKeyboardEvent.LEFT_ARROW
    UP_ARROW: Final = coin.SoKeyboardEvent.UP_ARROW
    RIGHT_ARROW: Final = coin.SoKeyboardEvent.RIGHT_ARROW
    DOWN_ARROW: Final = coin.SoKeyboardEvent.DOWN_ARROW
    PAGE_UP: Final = coin.SoKeyboardEvent.PAGE_UP
    PAGE_DOWN: Final = coin.SoKeyboardEvent.PAGE_DOWN
    END: Final = coin.SoKeyboardEvent.END
    PRIOR: Final = coin.SoKeyboardEvent.PRIOR
    NEXT: Final = coin.SoKeyboardEvent.NEXT
    PAD_ENTER: Final = coin.SoKeyboardEvent.PAD_ENTER
    PAD_F1: Final = coin.SoKeyboardEvent.PAD_F1
    PAD_F2: Final = coin.SoKeyboardEvent.PAD_F2
    PAD_F3: Final = coin.SoKeyboardEvent.PAD_F3
    PAD_F4: Final = coin.SoKeyboardEvent.PAD_F4
    PAD_0: Final = coin.SoKeyboardEvent.PAD_0
    PAD_1: Final = coin.SoKeyboardEvent.PAD_1
    PAD_2: Final = coin.SoKeyboardEvent.PAD_2
    PAD_3: Final = coin.SoKeyboardEvent.PAD_3
    PAD_4: Final = coin.SoKeyboardEvent.PAD_4
    PAD_5: Final = coin.SoKeyboardEvent.PAD_5
    PAD_6: Final = coin.SoKeyboardEvent.PAD_6
    PAD_7: Final = coin.SoKeyboardEvent.PAD_7
    PAD_8: Final = coin.SoKeyboardEvent.PAD_8
    PAD_9: Final = coin.SoKeyboardEvent.PAD_9
    PAD_ADD: Final = coin.SoKeyboardEvent.PAD_ADD
    PAD_SUBTRACT: Final = coin.SoKeyboardEvent.PAD_SUBTRACT
    PAD_MULTIPLY: Final = coin.SoKeyboardEvent.PAD_MULTIPLY
    PAD_DIVIDE: Final = coin.SoKeyboardEvent.PAD_DIVIDE
    PAD_SPACE: Final = coin.SoKeyboardEvent.PAD_SPACE
    PAD_TAB: Final = coin.SoKeyboardEvent.PAD_TAB
    PAD_INSERT: Final = coin.SoKeyboardEvent.PAD_INSERT
    PAD_DELETE: Final = coin.SoKeyboardEvent.PAD_DELETE
    PAD_PERIOD: Final = coin.SoKeyboardEvent.PAD_PERIOD
    F1: Final = coin.SoKeyboardEvent.F1
    F2: Final = coin.SoKeyboardEvent.F2
    F3: Final = coin.SoKeyboardEvent.F3
    F4: Final = coin.SoKeyboardEvent.F4
    F5: Final = coin.SoKeyboardEvent.F5
    F6: Final = coin.SoKeyboardEvent.F6
    F7: Final = coin.SoKeyboardEvent.F7
    F8: Final = coin.SoKeyboardEvent.F8
    F9: Final = coin.SoKeyboardEvent.F9
    F10: Final = coin.SoKeyboardEvent.F10
    F11: Final = coin.SoKeyboardEvent.F11
    F12: Final = coin.SoKeyboardEvent.F12
    BACKSPACE: Final = coin.SoKeyboardEvent.BACKSPACE
    TAB: Final = coin.SoKeyboardEvent.TAB
    RETURN: Final = coin.SoKeyboardEvent.RETURN
    ENTER: Final = coin.SoKeyboardEvent.ENTER
    PAUSE: Final = coin.SoKeyboardEvent.PAUSE
    SCROLL_LOCK: Final = coin.SoKeyboardEvent. SCROLL_LOCK
    ESCAPE: Final = coin.SoKeyboardEvent.ESCAPE
    DELETE: Final = coin.SoKeyboardEvent.DELETE
    KEY_DELETE: Final = coin.SoKeyboardEvent.DELETE
    PRINT: Final = coin.SoKeyboardEvent. PRINT
    INSERT: Final = coin.SoKeyboardEvent.INSERT
    NUM_LOCK: Final = coin.SoKeyboardEvent.NUM_LOCK
    CAPS_LOCK: Final = coin.SoKeyboardEvent.CAPS_LOCK
    SHIFT_LOCK: Final = coin.SoKeyboardEvent.SHIFT_LOCK
    SPACE: Final = coin.SoKeyboardEvent.SPACE
    APOSTROPHE: Final = coin.SoKeyboardEvent.APOSTROPHE
    COMMA: Final = coin.SoKeyboardEvent.COMMA
    MINUS: Final = coin.SoKeyboardEvent.MINUS
    PERIOD: Final = coin.SoKeyboardEvent.PERIOD
    SLASH: Final = coin.SoKeyboardEvent.SLASH
    SEMICOLON: Final = coin.SoKeyboardEvent.SEMICOLON
    EQUAL: Final = coin.SoKeyboardEvent.EQUAL
    BRACKETLEFT: Final = coin.SoKeyboardEvent.BRACKETLEFT
    BACKSLASH: Final = coin.SoKeyboardEvent.BACKSLASH
    BRACKETRIGHT: Final = coin.SoKeyboardEvent.BRACKETRIGHT
    GRAVE: Final = coin.SoKeyboardEvent.GRAVE

class MarkerStyles(Const):
    """
    Const class of enumerants for coin SoMarkerSet.SoMarkerType
    """

    NONE: Final = coin.SoMarkerSet.NONE

    #size 5
    CROSS_5: Final = coin.SoMarkerSet.CROSS_5_5
    PLUS_5: Final = coin.SoMarkerSet.PLUS_5_5
    MINUS_5: Final = coin.SoMarkerSet.MINUS_5_5
    SLASH_5: Final = coin.SoMarkerSet.SLASH_5_5
    BACKSLASH_5: Final = coin.SoMarkerSet.BACKSLASH_5_5
    BAR_5: Final = coin.SoMarkerSet.BAR_5_5
    STAR_5: Final = coin.SoMarkerSet.STAR_5_5
    Y_5: Final = coin.SoMarkerSet.Y_5_5
    LIGHTNING_5: Final = coin.SoMarkerSet.LIGHTNING_5_5
    WELL_5: Final = coin.SoMarkerSet.WELL_5_5
    CIRCLE_LINE_5: Final = coin.SoMarkerSet.CIRCLE_LINE_5_5
    SQUARE_LINE_5: Final = coin.SoMarkerSet.SQUARE_LINE_5_5
    DIAMOND_LINE_5: Final = coin.SoMarkerSet.DIAMOND_LINE_5_5
    TRIANGLE_LINE_5: Final = coin.SoMarkerSet.TRIANGLE_LINE_5_5
    RHOMBUS_LINE_5: Final = coin.SoMarkerSet.RHOMBUS_LINE_5_5
    HOURGLASS_LINE_5: Final = coin.SoMarkerSet.HOURGLASS_LINE_5_5
    SATELLITE_LINE_5: Final = coin.SoMarkerSet.SATELLITE_LINE_5_5
    PINE_TREE_LINE_5: Final = coin.SoMarkerSet.PINE_TREE_LINE_5_5
    CAUTION_LINE_5: Final = coin.SoMarkerSet.CAUTION_LINE_5_5
    SHIP_LINE_5: Final = coin.SoMarkerSet.SHIP_LINE_5_5
    CIRCLE_FILLED_5: Final = coin.SoMarkerSet.CIRCLE_FILLED_5_5
    SQUARE_FILLED_5: Final = coin.SoMarkerSet.SQUARE_FILLED_5_5
    DIAMOND_FILLED_5: Final = coin.SoMarkerSet.DIAMOND_FILLED_5_5
    TRIANGLE_FILLED_5: Final = coin.SoMarkerSet.TRIANGLE_FILLED_5_5
    RHOMBUS_FILLED_5: Final = coin.SoMarkerSet.RHOMBUS_FILLED_5_5
    HOURGLASS_FILLED_5: Final = coin.SoMarkerSet.HOURGLASS_FILLED_5_5
    SATELLITE_FILLED_5: Final = coin.SoMarkerSet.SATELLITE_FILLED_5_5
    PINE_TREE_FILLED_5: Final = coin.SoMarkerSet.PINE_TREE_FILLED_5_5
    CAUTION_FILLED_5: Final = coin.SoMarkerSet.CAUTION_FILLED_5_5
    SHIP_FILLED_5: Final = coin.SoMarkerSet.SHIP_FILLED_5_5

    #size 7
    CROSS_7: Final = coin.SoMarkerSet.CROSS_7_7
    PLUS_7: Final = coin.SoMarkerSet.PLUS_7_7
    MINUS_7: Final = coin.SoMarkerSet.MINUS_7_7
    SLASH_7: Final = coin.SoMarkerSet.SLASH_7_7
    BACKSLASH_7: Final = coin.SoMarkerSet.BACKSLASH_7_7
    BAR_7: Final = coin.SoMarkerSet.BAR_7_7
    STAR_7: Final = coin.SoMarkerSet.STAR_7_7
    Y_7: Final = coin.SoMarkerSet.Y_7_7
    LIGHTNING_7: Final = coin.SoMarkerSet.LIGHTNING_7_7
    WELL_7: Final = coin.SoMarkerSet.WELL_7_7
    CIRCLE_LINE_7: Final = coin.SoMarkerSet.CIRCLE_LINE_7_7
    SQUARE_LINE_7: Final = coin.SoMarkerSet.SQUARE_LINE_7_7
    DIAMOND_LINE_7: Final = coin.SoMarkerSet.DIAMOND_LINE_7_7
    TRIANGLE_LINE_7: Final = coin.SoMarkerSet.TRIANGLE_LINE_7_7
    RHOMBUS_LINE_7: Final = coin.SoMarkerSet.RHOMBUS_LINE_7_7
    HOURGLASS_LINE_7: Final = coin.SoMarkerSet.HOURGLASS_LINE_7_7
    SATELLITE_LINE_7: Final = coin.SoMarkerSet.SATELLITE_LINE_7_7
    PINE_TREE_LINE_7: Final = coin.SoMarkerSet.PINE_TREE_LINE_7_7
    CAUTION_LINE_7: Final = coin.SoMarkerSet.CAUTION_LINE_7_7
    SHIP_LINE_7: Final = coin.SoMarkerSet.SHIP_LINE_7_7
    CIRCLE_FILLED_7: Final = coin.SoMarkerSet.CIRCLE_FILLED_7_7
    SQUARE_FILLED_7: Final = coin.SoMarkerSet.SQUARE_FILLED_7_7
    DIAMOND_FILLED_7: Final = coin.SoMarkerSet.DIAMOND_FILLED_7_7
    TRIANGLE_FILLED_7: Final = coin.SoMarkerSet.TRIANGLE_FILLED_7_7
    RHOMBUS_FILLED_7: Final = coin.SoMarkerSet.RHOMBUS_FILLED_7_7
    HOURGLASS_FILLED_7: Final = coin.SoMarkerSet.HOURGLASS_FILLED_7_7
    SATELLITE_FILLED_7: Final = coin.SoMarkerSet.SATELLITE_FILLED_7_7
    PINE_TREE_FILLED_7: Final = coin.SoMarkerSet.PINE_TREE_FILLED_7_7
    CAUTION_FILLED_7: Final = coin.SoMarkerSet.CAUTION_FILLED_7_7
    SHIP_FILLED_7: Final = coin.SoMarkerSet.SHIP_FILLED_7_7

    #size 9
    CROSS_9:            Final = coin.SoMarkerSet.CROSS_9_9
    PLUS_9:             Final = coin.SoMarkerSet.PLUS_9_9
    MINUS_9:            Final = coin.SoMarkerSet.MINUS_9_9
    SLASH_9:            Final = coin.SoMarkerSet.SLASH_9_9
    BACKSLASH_9:        Final = coin.SoMarkerSet.BACKSLASH_9_9
    BAR_9:              Final = coin.SoMarkerSet.BAR_9_9
    STAR_9:             Final = coin.SoMarkerSet.STAR_9_9
    Y_9:                Final = coin.SoMarkerSet.Y_9_9
    LIGHTNING_9:        Final = coin.SoMarkerSet.LIGHTNING_9_9
    WELL_9:             Final = coin.SoMarkerSet.WELL_9_9
    CIRCLE_LINE_9:      Final = coin.SoMarkerSet.CIRCLE_LINE_9_9
    SQUARE_LINE_9:      Final = coin.SoMarkerSet.SQUARE_LINE_9_9
    DIAMOND_LINE_9:     Final = coin.SoMarkerSet.DIAMOND_LINE_9_9
    TRIANGLE_LINE_9:    Final = coin.SoMarkerSet.TRIANGLE_LINE_9_9
    RHOMBUS_LINE_9:     Final = coin.SoMarkerSet.RHOMBUS_LINE_9_9
    HOURGLASS_LINE_9:   Final = coin.SoMarkerSet.HOURGLASS_LINE_9_9
    SATELLITE_LINE_9:   Final = coin.SoMarkerSet.SATELLITE_LINE_9_9
    PINE_TREE_LINE_9:   Final = coin.SoMarkerSet.PINE_TREE_LINE_9_9
    CAUTION_LINE_9:     Final = coin.SoMarkerSet.CAUTION_LINE_9_9
    SHIP_LINE_9:        Final = coin.SoMarkerSet.SHIP_LINE_9_9
    CIRCLE_FILLED_9:    Final = coin.SoMarkerSet.CIRCLE_FILLED_9_9
    SQUARE_FILLED_9:    Final = coin.SoMarkerSet.SQUARE_FILLED_9_9
    DIAMOND_FILLED_9:   Final = coin.SoMarkerSet.DIAMOND_FILLED_9_9
    TRIANGLE_FILLED_9:  Final = coin.SoMarkerSet.TRIANGLE_FILLED_9_9
    RHOMBUS_FILLED_9:   Final = coin.SoMarkerSet.RHOMBUS_FILLED_9_9
    HOURGLASS_FILLED_9: Final = coin.SoMarkerSet.HOURGLASS_FILLED_9_9
    SATELLITE_FILLED_9: Final = coin.SoMarkerSet.SATELLITE_FILLED_9_9
    PINE_TREE_FILLED_9: Final = coin.SoMarkerSet.PINE_TREE_FILLED_9_9
    CAUTION_FILLED_9:   Final = coin.SoMarkerSet.CAUTION_FILLED_9_9
    SHIP_FILLED_9:      Final = coin.SoMarkerSet.SHIP_FILLED_9_9

    #no @staticmethod decorator or self argument for Const object methods
    def get(shape, size): # lgtm[py/not-named-self]
        """
        Convenience function to get marker index using shape / size arguments
        """
        #pylint: disable=no-self-argument

        return MarkerStyles.__dict__.get(f'{shape.upper()}_{str(size)}')

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

    COLOR:      Final = coin.SoBaseColor
    COORDINATE: Final = coin.SoCoordinate3
    DRAW_STYLE: Final = coin.SoDrawStyle
    EVENT_CB:   Final = coin.SoEventCallback
    FONT:       Final = coin.SoFont

    if GEO_SUPPORT:

        GEO_COORDINATE: Final = coin.SoGeoCoordinate
        GEO_ORIGIN:     Final = coin.SoGeoOrigin
        GEO_SEPARATOR:  Final = coin.SoGeoSeparator

    GROUP:          Final = coin.SoGroup
    KEYBOARD_EVENT: Final = coin.SoKeyboardEvent
    LINE_SET:       Final = coin.SoLineSet
    MARKER_SET:     Final = coin.SoMarkerSet
    NODE:           Final = coin.SoNode
    PICK_STYLE:     Final = coin.SoPickStyle
    SWITCH:         Final = coin.SoSwitch
    SEPARATOR:      Final = coin.SoSeparator
    TEXT:           Final = coin.SoText2
    TRANSFORM:      Final = coin.SoTransform
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
Support class for managing Coin3D node styles
"""

from pivy import coin

from pivy_trackers import Const

class CoinStyles(Const):
    """
    Pre-defined styles for use with Coin3d scenegraph nodes
    """

    class Color(Const):
        """
        Color constants
        """
        BLACK = (0.0, 0.0, 0.0)
        WHITE = (1.0, 1.0, 1.0)
        RED = (1.0, 0.0, 0.0)
        GREEN = (0.0, 1.0, 0.0)
        BLUE = (0.0, 0.0, 1.0)
        YELLOW = (1.0, 1.0, 0.0)
        CYAN = (0.0, 1.0, 1.0)
        MAGENTA = (1.0, 0.0, 1.0)
        GRAY_75 = (0.75, 0.75, 0.75)

        MAROON = (0.5, 0.0, 0.0)
        FOREST = (0.0, 0.5, 0.0)
        NAVY = (0.0, 0.0, 0.5)
        OLIVE = (0.5, 0.5, 0.0)
        TEAL = (0.0, 0.5, 0.5)
        PURPLE = (0.5, 0.0, 0.5)
        GRAY_50 = (0.5, 0.5, 0.5)

        ORANGE = (1.0, 0.5, 0.0)
        GOLD = (1.0, 0.85, 0.0)

        @staticmethod
        def scale(color, value):
            """
            Scale the factors of a color by the provided value
            If float, all colors scaled, otherwise, per-element
            """

            if isinstance(value, float):
                return ([_v * value for _v in color])

            _c = color

            if len(value) < 3:
                _c = list(color) + [1.0]*(3-len(value))

            return (_c[0]*value[0], _c[1]*value[1], _c[2]*value[2])

    class Style():
        """
        Style internal class for CoinStyles class
        """

        def __init__(self, style_id, base_style=None,
                     style=coin.SoDrawStyle.FILLED,
                     shape='CIRCLE_FILLED', line_wdith=0.0,
                     line_pattern=0xffff, size=9, color=(1.0, 1.0, 1.0)):

            """
            Style constructor
            """

            if base_style:
                self.style = base_style.style
                self.shape = base_style.shape
                self.line_width = base_style.line_width
                self.line_pattern = base_style.line_pattern
                self.size = base_style.size
                self.color = base_style.color

                if style != coin.SoDrawStyle.FILLED:
                    self.style = style

                if shape != 'CIRCLE_FILLED':
                    self.shape = shape

                if line_wdith:
                    self.line_width = line_wdith

                if line_pattern != 0xffff:
                    self.line_pattern = line_pattern

                if size != 9:
                    self.size = size

                if color != (1.0, 1.0, 1.0):
                    self.color = color

            else:
                self.id = style_id
                self.style = style
                self.shape = shape
                self.line_width = line_wdith
                self.line_pattern = line_pattern
                self.size = size
                self.color = color


        def __str__(self):
            """
            String representation
            """

            return self.id

        def __repr__(self):

            return self.__str__()

    BASE = Style('base')
    DEFAULT = Style('default', color=Color.GRAY_75)
    DASHED = Style('dashed', line_pattern=0x0f0f)

    PARTIAL_SELECTED =\
        Style('partial selected', line_pattern=0x0fff,
              color=Color.scale(Color.GOLD, 0.9))

    SELECTED = Style('selected', color=Color.GOLD)
    ERROR = Style('error', color=Color.RED)

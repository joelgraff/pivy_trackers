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
Style support for Tracker objects
"""

from ..coin.coin_group import CoinGroup
from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.coin_styles import CoinStyles

class Style():
    """
    Style support for Tracker objects
    """

    #members added by Base
    base = None
    name = ''

    is_switched = None
    is_separated = None
    switch_first = None

    @staticmethod
    def init_graph(is_switched=False, is_separated=False, switch_first=True):
        Style.is_switched = is_switched
        Style.is_separated = is_separated
        Style.switch_first = switch_first

    def __init__(self):
        """
        Constructor
        """

        if not self.base:
            return

        self.style = CoinGroup(
            is_separated=Style.is_separated,
            is_switched=Style.is_switched,
            switch_first=Style.switch_first,
            parent=self.base, name=self.name +'_STYLE')

        self.style.draw_style = self.style.add_node(Nodes.DRAW_STYLE)
        self.style.color = self.style.add_node(Nodes.COLOR)

        self.coin_style = CoinStyles.BASE
        self.active_style = CoinStyles.BASE

        Style.init_graph()

        super().__init__()

    def set_style(self, style=None, draw=None, color=None):
        """
        Update the tracker style
        """

        if style is None:
            style = self.coin_style

        if self.active_style == style:
            return

        if not draw:
            draw = self.style.draw_style

        if not color:
            color = self.style.color

        if not style:
            style = self.coin_style

        draw.lineWidth = style.line_width
        draw.style = style.style
        draw.linePattern = style.line_pattern

        color.rgb = style.color

        self.active_style = style

    def finish(self):
        """
        Cleanup
        """

        self.style.finalize()
        self.style.draw_style = None
        self.style.color = None
        self.coin_style = None
        self.active_style = None

Style.init_graph()

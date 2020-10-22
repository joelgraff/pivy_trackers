# -*- coding: utf-8 -*-
#***********************************************************************
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
Text Tracker class
"""

from types import SimpleNamespace

from ..coin.coin_enums import FontStyles
from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.coin_group import CoinGroup

from .base import Base
from .text_label import TextLabel

class TextTracker(Base):
    """
    TextTracker class
    """

    #members added by Base
    base = None
    name = ''

    def __init__(self):
        """
        Constructor
        """

        if not self.base:
            return

        _idx = 1
        _index = ''
        _name = self.name + '__TEXT'

        while hasattr(self, _name + _index):
            _index = str(_idx)
            _idx += 1

        _name = _name + _index

        self.defaults = SimpleNamespace()
        self.defaults.font = ''
        self.defaults.style = FontStyles.NORMAL
        self.defaults.size = 100.0
        self.defaults.transform_node = True
        self.defaults.font_node = True

        self.font = self.base.add_node(Nodes.FONT)
        self.font.size.setValue(self.defaults.size)

        self.labels = []
        self.origin = (0.0, 0.0, 0.0)

        self.text.set_visibility(False)

        super().__init__()

    def update(self, position):
        """
        Update the translation of the labels based on provided position
        """

        for _label in labels.values():
            _label.set_translation(TUpleMath.subtract(position, self.origin))

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
Text trait class
"""

from types import SimpleNamespace

from ..coin.coin_enums import FontStyles
from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.coin_group import CoinGroup

from .text_label import TextLabel

class Text:
    """
    Text trait class
    """

    #members added by Base
    base = None
    name = ''

    is_switched = None
    is_separated = None
    switch_first = None

    @staticmethod
    def init_graph(is_switched=True, is_separated=True, switch_first=True):
        Text.is_switched = is_switched
        Text.is_separated = is_separated
        Text.switch_first = switch_first

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

        self.text = CoinGroup(
            is_separated=Text.is_separated,
            is_switched=Text.is_switched,
            switch_first=Text.switch_first,
            parent=self.base, name=_name)

        Text.init_graph()

        self.text.transform = self.text.add_node(Nodes.TRANSFORM)
        self.text.transform.translation.setValue((0.0, 0.0, 0.0))
        self.text.font = self.text.add_node(Nodes.FONT)

        self.defaults = SimpleNamespace()
        self.defaults.font = ''
        self.defaults.style = FontStyles.NORMAL
        self.defaults.size = 100.0
        self.defaults.transform_node = True
        self.defaults.font_node = True

        self.text.font.size.setValue(self.defaults.size)

        self.labels = {}
        self.origin = (0.0, 0.0, 0.0)

        self.text.set_visibility(False)

        super().__init__()

    def update(self, position):
        """
        Update the translation of the labels based on provided position
        """

        for _label in labels.values():
            _label.set_translation(TUpleMath.subtract(position, self.origin))

    def add_label(self, name=None, text=None, xf_node=None, font_node=None):
        """
        Add a new label nodegraph
        """

        _has_xf = self.defaults.transform_node
        _has_font = self.defaults.font_node

        if xf_node is not None:
            _has_xf = xf_node

        if font_node:
            _has_font = font_node

        _label = TextLabel(text, name, _has_xf, _has_font)

        #_label.set_size(self.defaults.size)
        #_label.set_font(
         #   self.defaults.font, self.defaults.style, self.defaults.size)

        self.labels[_label.group.name] = _label

        self.text.insert_node(_label.group.root)

        return _label

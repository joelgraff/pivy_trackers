# -*- coding: utf-8 -*-
#**************************************************************************
#*                                                                     *
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
Base class for Tracker objects
"""

from DraftGui import todo

from ..coin.coin_enums import NodeTypes as Nodes
from ..coin.coin_group import CoinGroup

from ..support.view_state import ViewState
from ..support.mouse_state import MouseState

from .event import Event

class Base():
    """
    Base class for Tracker objects
    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Class statics
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #global view state singleton
    view_state = None

    #global mouse state singleton
    mouse_state = None

    #global reference to the local root node at the top of the entire
    #structure for all trackers.  Typically, this is the 'task-level' root node
    local_root = None

    is_switched = None
    is_separated = None
    switch_first = None

    @staticmethod
    def init_graph(is_switched=True, is_separated=True, switch_first=True):
        Base.is_switched = is_switched
        Base.is_separated = is_separated
        Base.switch_first = switch_first

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Class Defiintion
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, name, view=None, parent=None):
        """
        Constructor
        """

        #name is three parts, delimited by periods ('doc.task.obj')
        #object name is always first
        self.names = name.split('.')[::-1]
        self.name = self.names[0]

        #pad array to ensure three elements
        if len(self.names) < 3:
            self.names += ['']*(3-len(self.names))

        if not Base.view_state:
            Base.view_state = ViewState(view)

        if not Base.mouse_state:
            Base.mouse_state = MouseState()

        #provide reference to scenegraph root for CoinGroup for default
        #node creation / destruction
        CoinGroup.scenegraph_root = Base.view_state.sg_root

        self.sg_root = self.view_state.sg_root

        self.callbacks = {}

        self.base = CoinGroup(
            is_separated=Base.is_separated,
            is_switched=Base.is_switched,
            switch_first=Base.switch_first,
            name=self.name + '_base', parent=parent)

        self.path_node = None
        self.transform = self.base.add_node(Nodes.TRANSFORM, 'Transform')

        self.top = self.base.top
        self.root = self.base.root

        #First-created tracker provides the local root node reference
        if not Base.local_root:
            Base.local_root = self.root

        Base.init_graph()

        super().__init__()

    def insert_into_scenegraph(self, verbose=False):
        """
        Insert the base node into the scene graph and trigger notifications
        """

        _fn = lambda _x: Base.view_state.sg_root.insertChild(_x, 0)

        todo.delay(self._do_insert, verbose)

    def _do_insert(self, verbose):
        """
        todo.delay callback for node insertion into scenegraph
        """

        Base.view_state.sg_root.insertChild(self.base.root, 0)
        Event.set_paths()

        if verbose:
            self.base.dump()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Wrappers for CoinGroup methods to expose them at the tracker level
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_visibility(self, visible=True):
        """Wrapper"""
        self.base.set_visibility(visible)

    def is_visible(self):
        """Wrapper"""
        return self.base.is_visible()

    def insert_group(self, coin_group):
        """Wrapper"""
        self.base.insert_node(coin_group.root)

    def copy(self):
        """Wrapper"""
        return self.base.copy()

    def finalize(self, node=None, parent=None):
        """
        Node destruction / cleanup
        """

        if self.view_state:
            self.view_state.finish()
            self.view_state = None

        #if self.mouse_state:
        #    self.mouse_state.finish()
        #    self.mouse_state = None

        self.base.finalize()

Base.init_graph()


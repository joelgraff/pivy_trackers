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
FreeCAD Command class for tracker selection / dragging
"""

import FreeCAD as App
import FreeCADGui as Gui

from DraftTools import Modifier

from .select_drag_linked_task import SelectDragLinkedTask

from .. import resources

class SelectDragUnlinkedCommand(Modifier):
    """
    Command Description
    """
    def __init__(self):
        """
        Constructor
        """

        self.doc = None
        self.task = None
        self.is_activated = False

    def IsActive(self):
        """
        Activation condition requires one alignment be selected
        """

        if Gui.Control.activeDialog():
            return False

        if not App.ActiveDocument:
            return False

        return True

    def GetResources(self):
        """
        Icon resources.
        """

        icon_path = resources.__path__[0] + '/icons/template_resource.svg'

        _tool_tip = 'Test pivy_trackers unlinked selection / dragging'

        return {'Pixmap'  : icon_path,
                'Accel'   : '',
                'MenuText': 'Pivy Tracker Unlinked Selection / Dragging Test',
                'ToolTip' : _tool_tip,
                'CmdType' : 'ForEdit'}

    def Activated(self):
        """
        Command activation method
        """
        #create alignment editing task
        self.task = SelectDragLinkedTask(is_linked=False, has_markers=True)

        Modifier.Activated(self, 'SelectDragUnlinkedCommand')

Gui.addCommand('SelectDragUnlinkedCommand', SelectDragUnlinkedCommand())

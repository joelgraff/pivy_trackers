# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2009 Yorik van Havre <yorik@uncreated.net>              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************
"""
Delayed function execution
"""
import traceback
import sys

from PySide import QtCore

class todo:
    """
    Delays execution of functions.

    Use todo.delay to schedule scenegraph changes which cannot occur
    during traversals

    List of (function, argument) pairs to be executed by
    QtCore.QTimer.singleShot(0,doTodo).
    """

    itinerary = []
    commitlist = []
    afteritinerary = []

    @staticmethod
    def doTasks():

        try:

            for f, arg in todo.itinerary:

                try:

                    if arg or (arg == False):
                        f(arg)

                    else:
                        f()

                except Exception:
                    print (traceback.format_exc(),
                    "\n[Draft.todo.tasks] Unexpected error:", \
                        sys.exc_info()[0], "in ", f, "(", arg, ")"
                    )

        except ReferenceError:

            print("""
                Debug: DraftGui.todo.doTasks: queue contains a deleted object, skipping
            """)

        todo.itinerary = []

        if todo.commitlist:

            for name, func in todo.commitlist:

                try:
                    func()

                except Exception:

                    print (
                        traceback.format_exc(),
                        "\n[todo.commit] Unexpected error:", \
                        sys.exc_info()[0], "in ", name, '-', func
                    )

        todo.commitlist = []

        for f, arg in todo.afteritinerary:

            try:

                if arg:
                    f(arg)

                else:
                    f()

            except Exception:

                print (traceback.format_exc(),
                    "\n[Draft.todo.tasks] Unexpected error:", \
                        sys.exc_info()[0], "in ", f, "(", arg, ")"
                )

        todo.afteritinerary = []

    @staticmethod
    def delay (f, arg):

        if todo.itinerary == []:
            QtCore.QTimer.singleShot(0, todo.doTasks)

        todo.itinerary.append((f,arg))

    @staticmethod
    def delayCommit (cl):
        QtCore.QTimer.singleShot(0, todo.doTasks)

        todo.commitlist = cl

    @staticmethod
    def delayAfter (f, arg):
        if todo.afteritinerary == []:
            QtCore.QTimer.singleShot(0, todo.doTasks)

        todo.afteritinerary.append((f,arg))

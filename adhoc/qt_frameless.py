import FreeCADGui as Gui

from PySide import QtCore, QtGui

class Qt_Frameless(QtGui.QLineEdit):
    """
    QT frameless widget base class
    """

    def __init__(self):
        """
        Constructor
        """

        super(Qt_Frameless, self).__init__(Gui.getMainWindow())

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)

        self.view = Gui.ActiveDocument.ActiveView

    def set_signal_callback(self, callback):
        """
        callback
        """

        self.editingFinished.connect(callback)

    def show(self, text, position):
        """
        Display the label with the provided text
        """

        _cur_cpos = self.view.getPoint(position)

        self.move(position[0] + 30, position[1] + 30)
        self.setText(text)
        super().show()

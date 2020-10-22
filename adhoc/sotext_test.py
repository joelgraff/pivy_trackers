from pivy import coin
import FreeCADGui as Gui
from DraftGui import todo
from ..coin import coin_utils as utils

_group = coin.SoGroup()
_font = coin.SoFont()
_text = coin.SoText2()
_transform = coin.SoTransform()
_coordinate = coin.SoCoordinate3()
_line = coin.SoLineSet()

_rot = coin.SbRotation(coin.SbVec3f((0.0, 0.0, 1.0)), 1.57)
_transform.rotation = _rot
_text.string.setValue('HELLO!')
_font.name.setValue('Arial')
_font.size.setValue(200.0)

_coordinate.point.setValues(0, 2, ((-100.0, -100.0, 0.0), (100.0, 100.0, 0.0)))

_group.addChild(_transform)
_group.addChild(_font)
_group.addChild(_text)
_group.addChild(_coordinate)
_group.addChild(_line)

Gui.ActiveDocument.ActiveView.getSceneGraph().insertChild(_group, 0)

utils.dump_node(Gui.ActiveDocument.ActiveView.getSceneGraph())

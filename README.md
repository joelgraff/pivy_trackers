# pivy_trackers

pivy_trackers is a 2D geometry library built on [pivy](https://github.com/FreeCAD/pivy), the python bindings library for Coin3D that is a part of the [FreeCAD](https://github.com/FreeCAD/FreeCAD) project.  

A "tracker" is simply geometry which "tracks with" the user as they interact with a tool to provide dynamic visual feedback.  A good example may be generating a "rubber band box" as a user clicks and drags over an area to select objects to provide a visual representation of the limits of their selection.

At the moment, pivy_trackers is tied to the FreeCAD API, though it may be adapted for another Coin3D application which implements pivy.

## Examples

Check out the wiki for [tracker examples](https://github.com/joelgraff/pivy_trackers/wiki/Examples)

## Motivation

Creating custom tools and workbenches in FreeCAD is greatly facilitated by the nearly one-to-one exposure of it's C++ API in Python, with the pivy Python bindings exposing to the underlying Coin3D scenegraph C++ API.

However, creating custom tools in FreeCAD that provide intuitive, visual feedback to the user poses a challenge as developers are forced to interact with the Coin3D scenegraph directly through pivy.  

Pivy_trackers eases this process and provides several basic features which are valuable to most any 3D modelling tool, like selection / multi-selection, dragging, and rotation, insulating the developer from most of the inner workings of the scenegraph while still allowing for full customization of the tracker behaviors.

## Requirements

While pivy_trackers aims to be dependent only on pivy (and, by extension, Coin3D), it is currently tied to FreeCAD's object libraries.

Specifically:
+ [FreeCAD/pivy](https://github.com/FreeCAD/pivy)
+ [FreeCAD/FreeCAD View3DViewerPy](https://github.com/FreeCAD/FreeCAD/blob/1995f9d0bac63820c5c42ac0075c91a49cbad119/src/Gui/View3DViewerPy.h)
+ [PySide QTimer](https://pypi.org/project/PySide2/)

**Note:** The PySide dependency for FreeCAD, specifically, is a unique package maintained via the [FreeCAD-Daily PPA](https://launchpad.net/~freecad-maintainers/+archive/ubuntu/freecad-daily).

## Getting Started

Clone the project into a path visible through your project's top-level module

```bash
cd /my/project/top/module/path
git clone https://github.com/joelgraff/pivy_trackers.git
```

## Usage

Pivy_trackers should be visible as a top-level module.  Thus, pivy_tracker classes can be imported directly as:

```python
from pivy_trackers.trait.base import Base
```

## Reference

+ [pivy](https://grey.colorado.edu/coin3d/index.html)
+ [pivy_trackers](https://github.com/joelgraff/pivy_trackers/wiki)

Note that while the pivy API is not directly documented, it is a one-to-one exposure of the Coin3D API.  Thus, reviewing the Coin3D documentation will provide the user with most relevant implementation details.  

Additional support can be found at the FreeCAD forums: https://forum.freecadweb.org/

## Contributors

Take a look at the wiki and project KanBan board for more information.  Feel free to reach out to me here or through the forums.  Contributions are greatly appreciated!

## License

[GNU LGPL v2.1](LICENSE)

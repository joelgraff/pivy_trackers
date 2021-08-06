def import_module(path, name):
    """
    Return an import of a module specified by path and module name
    """

    return __import__(path, globals(), locals(), [name])

def import_class(path, name):
    """
    Return a reference to the class specified by path and module name
    """

    return getattr(import_module(path, name), name)

import pivy

#Runtime-flag to indicate whether or not SoGeo nodes are supported.
GEO_SUPPORT = int(pivy.__version__.split('.')[1]) >=6 & \
    int(pivy.__version__.split('.')[2][0]) >= 5
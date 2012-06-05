

class ModuleNotFound(Exception):
    pass


class ModuleDef(object):
    name =  ''
    paths = []
    modules = []

    def __init__(self, name_mod, path_mods):
        self.name = name_mod
        self.paths = path_mods
        self.modules = [__import__(x) for x in path_mods]

    def has(self, cls):
        for module in self.modules:
            if cls.__name__ in dir(module):
                return True

        return False

    def __str__(self):
        return "<DCLModule %s>" % (self.name)



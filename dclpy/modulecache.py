

class ModuleCache(object):
	cache = {}

	@staticmethod
    def globals_of_module(mod_name, constants_included):
        if not cache[mod_name]:
            cache[mod_name] = []

        # Add the constants added do this module 
        cache[mod_name] += constants_included


"""
    @staticmethod
    def add_mod(mod_name, path):
        try:
            module = __import__(mod_name)
        except ImportError:
            print "Erro ao inserir módulo: %s não está no path ou não é o nome " \
                  "de um módulo Python."


        for attr in dir(module):
            item = getattr(module, attr)

            if isinstance(item, (types.FunctionType, types.BuiltinFunctionType)):
                lista.append(item)
"""

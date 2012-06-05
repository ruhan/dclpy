# -*- coding: utf-8 -*-
from moduledef import ModuleDef
from rules import TheRule, OnlyRule, ListRule
from exception import *

class ModuleDefNotFound(Exception):
    pass



class _DCL(object):
    rules = ListRule()
    mods = {}
    facts = []

    def __init__(self):
        self.rules = ListRule()
        self.mods = {}
        self.facts = []

    def mod(self, name_mod, *path_mods):
        self.mods[name_mod] = ModuleDef(name_mod, path_mods)

    def get_mod(self, name_mod):
        module = self.mods.get(name_mod, None)
        if not module:
            raise ModuleDefNotFound(name_mod)

        return module

    def the(self, mod_name, type_interaction, mod_target):
        self.rules.append(
            TheRule(
                self.get_mod(mod_name), 
                type_interaction, 
                self.get_mod(mod_target)
            )
        )

    def only(self, mod_name, type_interaction, mod_target):
        self.rules.append(
            OnlyRule(
                self.get_mod(mod_name), 
                type_interaction, 
                self.get_mod(mod_target)
            )
        )

    def init(self):
        from trace import set_listening
        set_listening()

    def notify_fact(self, fact):
        rules = self.rules.filter_by_type(fact['type'])

        for rule in rules:
            rule.verify(fact)



DCL = _DCL()



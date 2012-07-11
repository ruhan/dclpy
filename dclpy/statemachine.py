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

    # the abscence that the system founded
    resolved_absences = []

    def __init__(self):
        self.rules = ListRule()
        self.mods = {}
        self.facts = []

        self.resolved_absences = []

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

    def conclude(self):
        #if not self.resolved_absences: return

        print "\n\n"
        print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        print "%d abscences found " % len(self.resolved_absences)
        print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        print 

        for exp in self.resolved_absences:
            print exp.message


    def notify_fact(self, fact):
        rules = self.rules.filter_by_type(fact['type'])

        for rule in rules:
            try:
                rule.verify(fact)
            except DivergenceException as e:
                # TODO: do it in a best way
                # print e.message
                pass
            except ResolvedAbsenceException as e:
                # stores to report on the end of the executing
                self.resolved_absences.append(e)

DCL = _DCL()



# -*- coding: utf8 -*-
from exception import *


class Constraint(object):
    def __init__(self, mod, mod_target):
        self.mod = mod
        self.mod_target = mod_target


class CanAccess(Constraint):
    def check(self, fact):
        if fact['sender']:
            if self.mod.has(fact['sender']) and self.mod_target.has(fact['object']):
                return True

        return False


class CanInherit(Constraint):
    def check(self, fact):
        if fact['parent']:
            if self.mod.has(fact['parent']) and self.mod_target.has(fact['cls']):
                return True

        return False


class CanCreate(Constraint):
    def check(self, fact):
        if fact['sender']:
            if self.mod.has(fact['sender']) and self.mod_target.has(fact['object']):
                return True

        return False






class CantAccess(CanAccess):
    def check(self, fact):
        if fact['sender']:
            if super(CantAccess, self).check(fact):
                raise ViolationException(
                    fact, "%s can't access a method in %s" % (self.mod, self.mod_target)
                )

class CantInherit(CanInherit):
    def check(self, fact):
        if fact['parent']:
            if super(CantInherit, self).check(fact):
                raise ViolationException(
                    fact, "%s can't inherit from %s" % (self.mod, self.mod_target)
                )


class CantCreate(CanCreate):
    def check(self, fact):        
        if fact['sender']:
            if super(CantCreate, self).check(fact):
                raise ViolationException(
                    fact, "%s can't create %s" % (self.mod, self.mod_target)
                )



class ListRule(list):

    def filter_by_type(self, tipo):
        if tipo == 'objcreation':
            return filter(lambda x: x.constraint.__class__.__name__ in ['CanCreate', 'CantCreate'], self)
        elif tipo == 'inheritance':
            return filter(lambda x: x.constraint.__class__.__name__ in ['CanInherit', 'CantInherit'], self)
        elif tipo == 'methodcall':
            return filter(lambda x: x.constraint.__class__.__name__ in ['CanAccess', 'CantAccess'], self)


class Rule(object):
    def __init__(self, mod, type_interaction, mod_target):
        self.constraint = type_interaction(
            mod, 
            mod_target
        )

    def verify(self, fact):
        try:
            self.constraint.check(fact)
        except ViolationException as e:
            # TODO: do it in a best way
            print e.message


class TheRule(Rule):
    pass

class OnlyRule(Rule):
    # TODO: limit for valid ONLY descriptor
    pass
    """
    only urls publicas (X) podem acessar os modelos (Y)
    Quer dizer que para cada novo fatos de acesso, caso mod_target == Y, 
    se mos != (X), temos uma violação
    """




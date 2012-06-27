# -*- coding: utf8 -*-
from exception import *

class AffirmativeConstraint(object):
    """
    Base class for the Can* restrictions
    """
    
class NegativeConstraint(object):
    """
    Base class for the Cant* restrictions
    """
    

class Constraint(object):
    def __init__(self, mod, mod_target):
        self.mod = mod
        self.mod_target = mod_target


class CanAccess(Constraint, AffirmativeConstraint):
    def check(self, fact):
        if fact['sender']:
            if self.mod.has(fact['sender']) and self.mod_target.has(fact['receiver']):
                return True

        return False


class CanInherit(Constraint, AffirmativeConstraint):
    def check(self, fact):
        if fact['sender']:
            if self.mod.has(fact['sender']) and self.mod_target.has(fact['receiver']):
                return True

        return False


class CanCreate(Constraint, AffirmativeConstraint):
    def check(self, fact):
        if fact['sender']:
            if self.mod.has(fact['sender']) and self.mod_target.has(fact['receiver']):
                return True

        return False






class CantAccess(CanAccess, NegativeConstraint):
    def check(self, fact):
        if fact['sender']:
            if super(CantAccess, self).check(fact):
                raise ViolationException(
                    fact, "%s can't access a method in %s" % (self.mod, self.mod_target)
                )

class CantInherit(CanInherit, NegativeConstraint):
    def check(self, fact):
        if fact['sender']:
            if super(CantInherit, self).check(fact):
                raise ViolationException(
                    fact, "%s can't inherit from %s" % (self.mod, self.mod_target)
                )


class CantCreate(CanCreate, NegativeConstraint):
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


class TheRule(Rule):
    def verify(self, fact):
        try:
            self.constraint.check(fact)
        except ViolationException as e:
            # TODO: do it in a best way
            a = open('/tmp/arqerrors.txt', 'a')
            a.write(e.message)
            a.close()
            print e.message


class OnlyRule(Rule):
    def verify(self, fact):
        if issubclass(self.constraint.__class__, NegativeConstraint):
            return TheRule(self.constraint).verify(fact)

        mod = fact['sender']
        mod_target = fact['receiver']

        if self.constraint.mod_target.has(mod_target):
            if not self.constraint.mod.has(mod):
                print 'Erro ONLY ' + str(self.constraint.mod) + " " + str(self.constraint) + " " + str(self.constraint.mod_target)
                print 'fato contratiou: ' + str(fact)



# -*- coding: utf8 -*-
from exception import *


###############################################################################
# BASE CLASSES
###############################################################################

class AffirmativeConstraint(object):
    """
    Base class for the Can* restrictions
    """
    
class NegativeConstraint(object):
    """
    Base class for the Cant* restrictions
    """

class CommitmentConstraint(object):
    """
    Base classe for the Must* restrictions
    """


class Constraint(object):
    """
    Abstract class for all constraints. ( a trait, maybe? o.o )
    """
    def __init__(self, mod, mod_target):
        self.mod = mod
        self.mod_target = mod_target


###############################################################################
# POSITIVE ONES
###############################################################################

class CanAccess(Constraint, AffirmativeConstraint):
    def check(self, fact):
        if fact['sender']:
            if self.mod.has(fact['sender']) and self.mod_target.has(fact['receiver']):
                return True

        return False

    def raise_only_exception(self, fact):
        raise DivergenceException(
            fact, 
            message="Only %s can access %s, but %s did" % (
                self.mod, self.mod_target, fact['sender'].__name__
            )
        )



class CanInherit(Constraint, AffirmativeConstraint):
    def check(self, fact):
        if fact['sender']:
            if self.mod.has(fact['sender']) and self.mod_target.has(fact['receiver']):
                return True

        return False

    def raise_only_exception(self, fact):
        raise DivergenceException(
            fact, 
            message="Only %s can inherit from %s, but %s did" % (
                self.mod, self.mod_target, fact['sender'].__name__
            )
        )


class CanCreate(Constraint, AffirmativeConstraint):
    def check(self, fact):
        if fact['sender']:
            if self.mod.has(fact['sender']) and self.mod_target.has(fact['receiver']):
                return True

        return False

    def raise_only_exception(self, fact):
        raise DivergenceException(
            fact, 
            message="Only %s can create instances of %s, but %s did" % (
                self.mod, self.mod_target, fact['sender'].__name__
            )
        )



###############################################################################
# NEGATIVE ONES
###############################################################################

class CantAccess(CanAccess, NegativeConstraint):
    def check(self, fact):
        if fact['sender']:
            if super(CantAccess, self).check(fact):
                raise DivergenceException(
                    fact, "%s can't access a method in %s" % (self.mod, self.mod_target)
                )

class CantInherit(CanInherit, NegativeConstraint):
    def check(self, fact):
        if fact['sender']:
            if super(CantInherit, self).check(fact):
                raise DivergenceException(
                    fact, "%s can't inherit from %s" % (self.mod, self.mod_target)
                )


class CantCreate(CanCreate, NegativeConstraint):
    def check(self, fact):        
        if fact['sender']:
            if super(CantCreate, self).check(fact):
                raise DivergenceException(
                    fact, "%s can't create %s" % (self.mod, self.mod_target)
                )


###############################################################################
# COMMITMENT ONES
###############################################################################

class MustCreate(CanCreate, CommitmentConstraint):
    def check(self, fact):
        print fact
        if fact['sender']:
            if super(MustCreate, self).check(fact):
                raise ResolvedAbsenceException(
                    fact, "%s created %s" % (self.mod, self.mod_target)
                )

class MustAccess(CanAccess, CommitmentConstraint):
    def check(self, fact):
        if fact['sender']:
            if super(MustAccess, self).check(fact):
                raise ResolvedAbsenceException(
                    fact, "%s accessed %s" % (self.mod, self.mod_target)
                )


class MustInherit(CanInherit, CommitmentConstraint):
    def check(self, fact):
        if fact['sender']:
            if super(MustInherit, self).check(fact):
                raise ResolvedAbsenceException(
                    fact, "%s inherits from %s" % (self.mod, self.mod_target)
                )



class ListRule(list):

    def filter_by_type(self, tipo):
        if tipo == 'objcreation':
            return filter(
                lambda x: x.constraint.__class__.__name__ in ['CanCreate', 'CantCreate', 'MustCreate'], 
                self
            )
        elif tipo == 'inheritance':
            return filter(
                lambda x: x.constraint.__class__.__name__ in ['CanInherit', 'CantInherit', 'MustInherit'], 
                self
            )
        elif tipo == 'methodcall':
            return filter(
                lambda x: x.constraint.__class__.__name__ in ['CanAccess', 'CantAccess', 'MustAccess'], 
                self
            )


class Rule(object):
    def __init__(self, mod, type_interaction, mod_target):
        self.constraint = type_interaction(
            mod, 
            mod_target
        )


class TheRule(Rule):
    def verify(self, fact):
        self.constraint.check(fact)


class OnlyRule(Rule):
    def verify(self, fact):
        # If I want that only module X can't access Y, the others can access 
        # it, unless X
        # If I want that the module X can't access Y, the others can access 
        # it, unless X
        # So, use the 'only' is unnecessary, we can use the same semantic of
        # the 'the' statement
        if issubclass(self.constraint.__class__, NegativeConstraint):
            return TheRule(self.constraint).verify(fact)

        mod = fact['sender']
        mod_target = fact['receiver']

        if self.constraint.mod_target.has(mod_target):
            if not self.constraint.mod.has(mod):
                self.constraint.raise_only_exception(fact)




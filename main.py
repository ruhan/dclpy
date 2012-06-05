# -*- coding: utf-8 -*-
from trace import *
from controller import *
from dclpy import *


def start_system():
    c = Controller("Home")
    c.dispatch('/')
    #c.dispatch('/aereo/')

    print 'FIM'

    import sys
    sys.exit(0)



if __name__ == "__main__":
    DCL.mod('urls_publicas', 'controller')
    DCL.mod('modelos', 'models')
    DCL.mod('utilidades', 'models')

    DCL.the('urls_publicas', CantAccess, 'modelos')  
    DCL.the('urls_publicas', CantCreate, 'modelos')      
    DCL.the('urls_publicas', CantAccess, 'utilidades')
    DCL.the('modelos', CantInherit, 'modelos')

    #DCL.only('modelos', CanAccess, 'utilidades')

    DCL.init()

    start_system()


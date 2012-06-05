# -*- coding: utf-8 -*-
from statemachine import *


if __name__ == "__main__":

    set_listening()

    DCL.add_mod('controller', 'system.controller')
    DCL.add_mod('models', 'system.models')

    DCL.the('models', CANT_ACCESS, 'controller')

    from system import main
    main.execute()



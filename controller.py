from models import *
from utils import *

class Controller(object):
    def __init__(self, name):
        self.name = name

    def dispatch(self, url):
        view = View()
        view.render()

        model = Model()
        model.save()


class View(object):
    def render(self):
        util = Util()
        util.g()



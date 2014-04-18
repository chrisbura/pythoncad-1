
class Layer(object):
    def __init__(self, title='Untitled', drawing=None):
        self.title = title
        self.drawing = drawing

    def __repr__(self):
        return '<Layer "{0}">'.format(self.title)

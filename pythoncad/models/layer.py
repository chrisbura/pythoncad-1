
class Layer(object):
    def __init__(self, title='Untitled'):
        self.id = None
        self.title = title

    def __repr__(self):
        return '<Layer "{0}">'.format(self.title)

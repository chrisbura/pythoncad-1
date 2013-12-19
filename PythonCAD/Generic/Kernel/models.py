
class Layer(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Layer %r>' % (self.name)

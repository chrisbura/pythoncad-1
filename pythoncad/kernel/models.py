
class Layer(object):
    def __init__(self, name):
        self.name = name
        self.visible = True

    def __repr__(self):
        return '<Layer %r>' % (self.name)

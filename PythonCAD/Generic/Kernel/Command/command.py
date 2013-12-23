
class Command(object):
    def __init__(self, document):
        self.document = document
        self.db = self.document.db
        self.values = []
        self.active_input = 0
        self.can_preview = False

    @property
    def message(self):
        return self.inputs[self.active_input].message

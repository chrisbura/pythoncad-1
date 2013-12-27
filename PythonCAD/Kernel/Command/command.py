
class Command(object):
    def __init__(self, document):
        self.document = document
        self.db = self.document.db
        self.active_layer = self.document.get_layer_table().getActiveLayer()
        self.values = []
        self.active_input = 0
        self.can_preview = False

    @property
    def message(self):
        return self.inputs[self.active_input].message

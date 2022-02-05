
class RoseNode:
    def __init__(self, value):
        self.children = []
        self.parent = None
        self.value = value

    def add_child(self, child):
        self.children.append(child)

class RoseTree:
    def __init__(self, value):
       self.root = RoseNode(value)

class Parser:
    pass



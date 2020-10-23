import random as rand
import uuid

class Node:
    ''' Datastructure to handle the parser '''

    def __init__(self, value, level, parent=None, DEBUG=False):
        self.DEBUG = DEBUG
        self.value = value
        self.id = uuid.uuid1()
        self.children = set()
        self.level = level
        self.root = False
        self.parent = parent

        if level == 1:
            self.root = True

    def setParent(self, node):
        self.node = node

    def addChild(self, node):
        self.children.add(node)
        if self.DEBUG:
            print(self)

    def __str__(self):
        s = f"{self.level} NODE id: {self.id} value: {self.value}\n parent:{self.parent}"
        return s

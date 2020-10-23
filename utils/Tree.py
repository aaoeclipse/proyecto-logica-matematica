from utils.Node import Node
import networkx as nx

class Tree:
    ''' Node Manager '''

    def __init__(self, DEBUG):
        self.root_node = None
        self.DEBUG = DEBUG

    def create_graph_from_json(self,json):
        # reset
        self.root_node = None
        level = 0
        self.go_deep(json, level)
        G = nx.DiGraph()
        G.add_node(self.root_node.id, value=f'{self.root_node.value}i')
        # G.add_node(self.root_node.value)
        self.create_graph(G, self.root_node)
        return G
        
    def create_graph(self, G, node):
        for children in node.children:
            G.add_node(children.id, value=children.value)
            G.add_edge(children.parent.id, children.id)
            if(len(children.children) != 0):
                self.create_graph(G, children)
                

    def go_deep(self, curr_node, level, parent=None):
        ''' Deepness '''
        for left, right in curr_node.items():
            tmp_node = Node(left, level+1, parent, self.DEBUG)
            if (parent is not None):
                parent.addChild(tmp_node)
            else:
                self.root_node = tmp_node

            if (type(right) == dict):
                self.go_deep(right, level+1, tmp_node)
            else:
                parent.addChild(Node(right, level+2, tmp_node, self.DEBUG))

    def __str__(self):
        s = 'Printing: '
        s += f'{self.root_node}'
        return s



from collections import deque

class Node:
    def __init__(self,type,children=None,leaf=None):
        self.type = type
        if children:
            self.children = children              
        else:
            self.children = [ ]              
        self.leaf = leaf


def print_tree(current_node, spaces=0):
    printer = ''    
    printer += '| '*spaces 
    if(spaces > 0):
        printer = printer
    if(isinstance(current_node,Node)):     
        leafs = ""    
        leafs += str(current_node.leaf)
        print(str(printer) + current_node.type + " -> leafs: (" + leafs +")")
        for child in current_node.children:            
            print_tree(child, spaces+1)
    else:
        print(str(printer) + str(current_node))


#------------------------------graphviz------------------------------#

def tree_to_graphviz(current_node):
    ids = {}
    current = 0
    nodes = []
    edges = []

    stack = deque([(None, current_node, 0)])
    while stack:
        parent, node, num = stack.popleft()
        id_node = ids.get(id(node))
        if node is None:
            print(parent, nodes)
        if id_node is None:
            id_node = ids[id(node)] = "n{}".format(current)
            current += 1
            nodes.append('{} [label="{} {}"]'.format(id_node, num, node.type))
        if parent:
            edges.append('{} -> {}'.format(parent, id_node))
        for i, child in enumerate(node.children):
            stack.append((id_node, child, i))
        for leaf in node.leaf:
            id_leaf = "l{}".format(current)
            current += 1
            nodes.append('{} [label="{}", shape=box]'.format(id_leaf, leaf))
            edges.append('{} -> {}'.format(id_node, id_leaf))

    return """digraph {{
        {}
        {}
    }}""".format(
        "\n".join(nodes),
        "\n".join(edges)
    )

        

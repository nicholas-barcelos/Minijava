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

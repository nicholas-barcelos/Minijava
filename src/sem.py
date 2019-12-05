import src.node as nd

class Symbol:
    def __init__(self, vtype = None, prox = None):
        self.type = vtype
        self.prox = prox

    def __key(self):
        return (self.type, self.prox)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, A):
            return self.__key() == other.__key()
        return False

class Semantic:
    def __init__(self):
        self.stab = dict()

    def make_table(self,current_node):
        if(isinstance(current_node,nd.Node)):
            # tipo var;
            if current_node.type == 'var':
                vname = current_node.leaf[0]
                vtype = current_node.children[0].leaf[0]
                if vname not in self.stab:
                    # verify scope can error
                    self.stab[vname] = Symbol(vtype=vtype)
            # var = exp;
            elif(current_node.type == 'cmd' 
                    and len(current_node.leaf) > 1 
                    and current_node.leaf[1] == '='
                ):
                vname = current_node.leaf[0]
                if vname not in self.stab:
                    raise Exception("Atribuição de variavel inexistente.")
            # var[pos] = exp;
            elif(current_node.type == 'cmd' 
                    and len(current_node.leaf) > 3 
                    and current_node.leaf[3] == '='
                ):
                # ver como tratar posição de array na tabela
                vname = current_node.leaf[1]
                if vname not in self.stab:
                    raise Exception("Atribuição de variavel inexistente.")

            for child in current_node.children:            
                self.make_table(child)
import src.node as nd

class Symbol:
    def __init__(self, vtype = None, prox = None, len = None):
        self.vtype = vtype
        self.prox = prox
        self.len = len

    def __key(self):
        return (self.vtype, self.prox, self.len)

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
                vtype = None
                if len(current_node.children[0].leaf) > 1:
                    vtype = 'array'
                else:
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

                child = current_node.children[0]
                while child:
                    if len(child.children) > 0:
                        child = child.children[0]
                    else:
                        break
                arrlen = child.leaf[0]

                if vname in self.stab:
                    if self.stab[vname].vtype == 'array':
                        self.stab[vname].len = int(arrlen)
                else:
                    raise Exception(f"Atribuição de variavel {vname} inexistente.")
            # var[pos] = exp;
            elif(current_node.type == 'cmd' 
                    and len(current_node.leaf) > 3 
                    and current_node.leaf[3] == '='
                ):
                # ver como tratar posição de array na tabela
                vname = current_node.leaf[0]
                if vname not in self.stab:
                    raise Exception(f"Atribuição de variavel {vname} inexistente.")

            for child in current_node.children:            
                self.make_table(child)
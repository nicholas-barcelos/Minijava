import src.node as nd

class Symbol:
    def __init__(self, vtype = None, scopeVars = None, len = None, params = None, paramlen = None):
        self.vtype = vtype
        self.scopeVars = scopeVars
        self.len = len
        self.paramlen = paramlen
        self.params = params

    def __key(self):
        return (self.vtype, self.scopeVars, self.len)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, A):
            return self.__key() == other.__key()
        return False

class Semantic:
    def __init__(self):
        self.stab = dict()
        self.currClass = None
        self.currMethod = None

    def make_table(self,current_node):
        self.currClass = None
        self.currMethod = None
        self.table_step(current_node)

    def table_step(self,current_node):
        if(isinstance(current_node,nd.Node)):
            if current_node.type == 'main':
                self.currClass = current_node.leaf[1].lower()
                self.currMethod = "main"
                self.stab[self.currClass] = dict()

            elif current_node.type == 'classe':
                self.currClass = current_node.leaf[1].lower()
                self.currMethod = None
                self.stab[self.currClass] = dict()

            elif current_node.type == 'metodo':
                self.currMethod = current_node.leaf[1].lower()
                vtype = current_node.children[0].leaf[0]
                paramlen = 0
                params = dict()
                classe = self.stab[self.currClass]

                child = current_node.children[1] # optparams
                if len(child.children) > 0:
                    child = child.children[0] # params
                    ptype = child.children[0].leaf[0]
                    pname = child.leaf[0].lower()
                    params[pname] = Symbol(vtype=ptype)
                    # loopvirgulatipoid
                    while len(child.children) > 1:
                        child = child.children[1]
                        if len(child.leaf) > 0:
                            ptype = child.children[0].leaf[0]
                            pname = child.leaf[1].lower()
                            params[pname] = Symbol(vtype=ptype)
                        paramlen += 1

                classe[self.currMethod] = Symbol(vtype=vtype,params=params,paramlen=paramlen)
            # tipo var;
            elif current_node.type == 'var':
                classe = self.stab[self.currClass]
                metodo = None
                # base da classe já que métodos não podem começar com número
                if self.currMethod is None:
                    classe["0"] = Symbol()
                    metodo = classe["0"]
                # é variável de corpo método
                else:
                    metodo = classe[self.currMethod]
                
                vname = current_node.leaf[0].lower()
                vtype = None
                if len(current_node.children[0].leaf) > 1:
                    vtype = 'array'
                else:
                    vtype = current_node.children[0].leaf[0]
                
                if metodo.scopeVars is None:
                    metodo.scopeVars = dict()
                    metodo.scopeVars[vname] = Symbol(vtype=vtype)
                else:
                    metodo.scopeVars[vname] = Symbol(vtype=vtype)
            # var = exp;
            elif(current_node.type == 'cmd' 
                    and len(current_node.leaf) > 1 
                    and current_node.leaf[1] == '='
                ):
                classe = self.stab[self.currClass]
                metodo = None
                # base da classe já que métodos não podem começar com número
                if self.currMethod is None:
                    classe["0"] = Symbol()
                    metodo = classe["0"]
                # é variável de corpo método
                else:
                    metodo = classe[self.currMethod]

                vname = current_node.leaf[0].lower()

                if metodo.scopeVars is None:
                    raise Exception(f"Atribuição de variavel \'{vname}\' inexistente.")
                elif vname not in metodo.scopeVars:
                    raise Exception(f"Atribuição de variavel \'{vname}\' inexistente.")
                elif metodo.scopeVars[vname].vtype == 'array':
                    child = current_node.children[0]
                    while len(child.children) > 0:
                        child = child.children[0]
                    arrlen = int(child.leaf[0])

                    if vname in metodo.scopeVars:
                        metodo.scopeVars[vname].len = arrlen

            # var[pos] = exp;
            elif(current_node.type == 'cmd' 
                    and len(current_node.leaf) > 3 
                    and current_node.leaf[3] == '='
                ):
                classe = self.stab[self.currClass]
                metodo = None
                # base da classe já que métodos não podem começar com número
                if self.currMethod is None:
                    classe["0"] = Symbol()
                    metodo = classe["0"]
                # é variável de corpo método
                else:
                    metodo = classe[self.currMethod]

                vname = current_node.leaf[0].lower()

                if metodo.scopeVars is None:
                    raise Exception(f"Atribuição de variavel \'{vname}\' inexistente.")
                elif vname not in metodo.scopeVars:
                    raise Exception(f"Atribuição de variavel \'{vname}\' inexistente.")
                elif metodo.scopeVars[vname].vtype == 'array':
                    child = current_node.children[0]
                    while len(child.children) > 0:
                        child = child.children[0]
                    pos = int(child.leaf[0])

                    if vname in metodo.scopeVars:
                        if (metodo.scopeVars[vname].len is None
                            or metodo.scopeVars[vname].len <= pos):
                            raise Exception(f"Atribuição de indíce fora de alcance da variavel \'{vname}\': {pos}.")
            
            # prossegue a montagem
            for child in current_node.children:            
                self.table_step(child)
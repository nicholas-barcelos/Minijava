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
        self.stab = None
        self.calls = None
        self.currClass = None
        self.currMethod = None

    def make_table(self,current_node):
        self.stab = dict()
        self.calls = dict()
        self.currClass = None
        self.currMethod = None
        self.table_step(current_node)
        self.verify_calls()

    def verify_calls(self):
        for classe in self.calls.keys():
            for metodo in self.calls[classe].keys():
                for chamada in self.calls[classe][metodo]:
                    mparams = self.stab[classe][metodo].params
                    i = 0
                    for sm in mparams.values():
                        if chamada[i] is not None:
                            if chamada[i] != sm.vtype:
                                raise Exception(
                                    f"Erro de semântica: Variável na chamada do "
                                    f"método \'{metodo}\' de \'{classe}\',"
                                    f"\'{chamada[i]}\' não é \'{sm.vtype}\'."
                                )
                        i += 1
                    # print("metodo params:",mparams)
                    # print("chamada ",chamada)

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
                    raise Exception(f"Erro de semântica: Atribuição de variavel \'{vname}\' inexistente.")
                elif vname not in metodo.scopeVars:
                    raise Exception(f"Erro de semântica: Atribuição de variavel \'{vname}\' inexistente.")
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
                    raise Exception(f"Erro de semântica: Atribuição de variavel \'{vname}\' inexistente.")
                elif vname not in metodo.scopeVars:
                    raise Exception(f"Erro de semântica: Atribuição de variavel \'{vname}\' inexistente.")
                elif metodo.scopeVars[vname].vtype == 'array':
                    child = current_node.children[0]
                    while len(child.children) > 0:
                        child = child.children[0]
                    pos = int(child.leaf[0])

                    if vname in metodo.scopeVars:
                        if (metodo.scopeVars[vname].len is None
                            or metodo.scopeVars[vname].len <= pos):
                            raise Exception(f"Erro de semântica: Atribuição de indíce fora de alcance da variavel \'{vname}\': {pos}.")
            
            # Verifica chamada de método
            elif(current_node.type == 'pexp' 
                and len(current_node.leaf) > 3
                and current_node.leaf[0] == "."
                ):
                cname = ""
                mname = ""
                # new Classe().metodo()
                if len(current_node.children[0].leaf) > 1:
                    cname = current_node.children[0].leaf[1].lower()
                    mname = current_node.leaf[1].lower()
                # this.metodo()
                else:
                    cname = self.currClass
                    mname = self.currMethod

                # print(
                #     f"pexp:\n"
                #     f"  children:{current_node.children}\n"
                #     f"  leaf:{current_node.leaf}\n"
                #     f"  cname:{cname}\n"
                #     f"  mname:{mname}\n"
                # )

                # verifica o tipo dos operadores desde que não sejam variáveis
                optexps = current_node.children[1]
                argtypes = []
                val = None
                tp = None
                if len(optexps.children) > 0:
                    exp = optexps.children[0].children[0]
                    while len(exp.children) > 0:
                        exp = exp.children[0]
                    try:
                        val = int(exp.leaf[0])
                        tp = "int"
                    except ValueError:
                        val = exp.leaf[0]
                        if val.lower() == "true" or val.lower() == "false":
                            val = "boolean"
                        else:
                            tp = None
                    argtypes.append(tp)

                    # continua operando sobre loopvirgulaexp
                    loopv = optexps.children[0].children[1]
                    while len(loopv.children) > 1:
                        loopvexp = loopv.children[0]
                        while len(loopvexp.children) > 0:
                            loopvexp = loopvexp.children[0]
                        loopv = loopv.children[1]

                        try:
                            val = int(loopvexp.leaf[0])
                            tp = "int"
                        except ValueError:
                            val = loopvexp.leaf[0]
                            if val.lower() == "true" or val.lower() == "false":
                                tp = "boolean"
                            else:
                                tp = None
                        argtypes.append(tp)

                # Adiciona o array de tipos da chamada
                if cname in self.calls:
                    classe = self.calls[cname]
                    if mname in classe:
                        self.calls[cname][mname].append(argtypes)
                    else:
                        classe[mname] = []
                else:
                    self.calls[cname] = dict()
                    self.calls[cname][mname] = []
                    self.calls[cname][mname].append(argtypes)
                # print("argtypes",argtypes)

            # prossegue a montagem
            for child in current_node.children:            
                self.table_step(child)
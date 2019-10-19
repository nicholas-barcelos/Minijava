def p_statement_assign(self,p):
    'statement : NAME EQUALS expression'
    # names[p[1]] = p[3]
    p[0] = nd.Node("assign",[p[1],p[3]],p[2])

#------------------------------------------------------------

def p_statement_expr(self,p):
    'statement : expression'
    # print(p[1])
    p[0] = nd.Node("expression",[p[1]])

#------------------------------------------------------------

def p_expression_binop(self,p):
    '''expression : expression PLUS expression
                    | expression MINUS expression
                    | expression TIMES expression
                    | expression DIVIDE expression'''
    # if p[2] == '+'  : p[0] = p[1] + p[3]
    # elif p[2] == '-': p[0] = p[1] - p[3]
    # elif p[2] == '*': p[0] = p[1] * p[3]
    # elif p[2] == '/': p[0] = p[1] / p[3]
    p[0] = nd.Node("binop", [p[1],p[3]],[p[2]]) 

#------------------------------------------------------------

def p_expression_uminus(self,p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

#------------------------------------------------------------

def p_expression_group(self,p):
    'expression : LPAREN expression RPAREN'
    # p[0] = p[2]
    p[0] = nd.Node("group", [p[2]],[p[1],p[3]])

#------------------------------------------------------------

def p_expression_number(self,p):
    'expression : NUMBER'
    p[0] = p[1]

#------------------------------------------------------------

def p_expression_name(self,p):
    'expression : NAME'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0
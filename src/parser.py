import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

import lib.ply.lex as lex
import lib.ply.yacc as yacc
import src.node as nd
import os

class Parser:
    # Lexer
    reserved = {
        'boolean' : 'BOOLEAN',
        'class' : 'CLASS',
        'extends' : 'EXTENDS',
        'public' : 'PUBLIC',
        'static' : 'STATIC',
        'void' : 'VOID',
        'main' : 'MAIN',
        'String' : 'STRING',
        'return' : 'RETURN',
        'int' : 'INT',
        'if' : 'IF',
        'else' : 'ELSE',
        'while' : 'WHILE',
        'length' : 'LENGTH',
        'true' : 'TRUE',
        'false' : 'FALSE',
        'this' : 'THIS',
        'new' : 'NEW',
        'null' : 'NULL',
        'System.out.println' : 'SOUT'
    }

    tokens = [
        'ID', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'EQUALS','LPAREN','RPAREN', 
        'LSBRACKET', 'RSBRACKET', 'LCBRACKET', 'RCBRACKET', 'SEMICOLON', 'DOT', 
        'COMMA', 'LTHAN', 'GTHAN','LTHANEQ', 'GTHANEQ', 'NOTEQ', 'AND', 'NOT', 'ASSIGN'
    ] + list(reserved.values())

    # Tokens

    t_PLUS       = r'\+'
    t_MINUS      = r'\-'
    t_TIMES      = r'\*'
    t_EQUALS     = r'\=\='
    t_ASSIGN     = r'\='
    t_LPAREN     = r'\('
    t_RPAREN     = r'\)'
    t_NUMBER     = r'[0-9]+'
    t_LSBRACKET  = r'\['
    t_RSBRACKET  = r'\]'
    t_LCBRACKET  = r'\{'
    t_RCBRACKET  = r'\}'
    t_SEMICOLON  = r';' 
    t_DOT        = r'\.'
    t_COMMA      = r','
    t_LTHAN      = r'\<'
    t_GTHAN      = r'\>'
    t_LTHANEQ    = r'\<\='
    t_GTHANEQ    = r'\>\='
    t_NOTEQ      = r'\!\='
    t_AND        = r'\&\&'
    t_NOT        = r'\!'
    
    # Ignored characters
    t_ignore = " \t"

    def t_ID(self,t):
        r'System.out.println|[a-zA-Z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value,'ID')    # Check for reserved words
        return t

    def t_ccode_comment(self,t):
        r'(/\*(.|\n)*?\*/)|(//.*)'
        pass

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    #------------------------------------------------------------------------------#

    # Parser
    # Precedence rules for the arithmetic operators
    precedence = (
        ('left','PLUS','MINUS'),
        ('left','TIMES'),
        ('right','UMINUS'),
    )

    #------------------------------REGRAS GRAMATICAIS------------------------------#
    
    #--------------PROG--------------#
    def p_prog_main(self, p):
        'prog : main loopclasse'
        p[0] = nd.Node('prog0', [ p[1] ], [ ])
    
    #--------------MAIN--------------#
    def p_main_class(self,p):
        'main : CLASS ID LCBRACKET PUBLIC STATIC VOID MAIN LPAREN STRING LSBRACKET RSBRACKET ID RPAREN LCBRACKET cmd RCBRACKET RCBRACKET'
        p[0] = nd.Node('main', [ p[15] ] , [ p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13], p[14], p[16], p[17] ])
    
    #--------------CLASSE--------------#
    def p_classe_id(self,p):
        'classe : CLASS ID optextends LCBRACKET loopvar loopmetodo RCBRACKET'
        p[0] = nd.Node('classe', [ p[3], p[5], p[6] ] , [ p[1], p[2], p[4], p[7] ] )

    #--------------VAR--------------#
    def p_var_tipo(self, p):
        'var : tipo ID SEMICOLON'
        p[0] = nd.Node('var', [ p[1]], [ p[2], p[3] ])
    
    #--------------METODO--------------#
    def p_metodo_public(self, p):
        'metodo : PUBLIC tipo ID LPAREN optparams RPAREN LCBRACKET loopvar loopcmd RETURN exp SEMICOLON RCBRACKET'
        p[0] = nd.Node('metodo', [ p[2], p[5], p[8], p[9], p[11] ], [ p[1], p[3], p[4], p[6], p[7], p[10], p[12], p[13] ])
    
    #--------------PARAMS--------------#
    def p_params_tipo(self, p):
        'params : tipo ID loopvirgulatipoid'
        p[0] = nd.Node('params', [ p[1], p[3] ], [ p[2] ])

    #--------------TIPO--------------#
    def p_tipo_inta(self, p):
        'tipo : INT LSBRACKET RSBRACKET'
        p[0] = nd.Node('tipointa', [], [ p[1], p[2], p[3] ])

    def p_tipo_bool(self, p):
        'tipo : BOOLEAN'
        p[0] = nd.Node('tipobool', [], [ p[1] ])
    
    def p_tipo_int(self, p):
        'tipo : INT'
        p[0] = nd.Node('tipoint', [], [ p[1] ])

    def p_tipo_id(self, p):
        'tipo : ID'
        p[0] = nd.Node('tipoid', [], [ p[1] ])
    
    #--------------CMD--------------#
    def p_cmd_chave(self, p):
        'cmd : LCBRACKET loopcmd RCBRACKET'
        p[0] = nd.Node('cmdid', [ p[2] ], [ p[1], p[3] ])

    def p_cmd_if(self, p):
        'cmd : IF LPAREN exp RPAREN cmd'
        p[0] = nd.Node('cmdid', [ p[3], p[5] ], [ p[1], p[2], p[4] ])

    def p_cmd_ifelse(self, p):
        'cmd : IF LPAREN exp RPAREN cmd ELSE cmd'
        p[0] = nd.Node('cmdid', [ p[3], p[5], p[7] ], [ p[1], p[2], p[4], p[6] ])

    def p_cmd_while(self, p):
        'cmd : WHILE LPAREN exp RPAREN cmd'
        p[0] = nd.Node('cmdid', [ p[3], p[5] ], [ p[1], p[2], p[4] ])

    def p_cmd_sout(self, p):
        'cmd : SOUT LPAREN exp RPAREN SEMICOLON'
        p[0] = nd.Node('cmdid', [ p[3] ], [ p[1], p[2], p[4], p[5] ])

    def p_cmd_ideq(self, p):
        'cmd : ID ASSIGN exp'
        p[0] = nd.Node('cmdideq', [ p[3] ], [ p[1], p[2] ])
    
    def p_cmd_id(self, p):
        'cmd : ID LSBRACKET exp RSBRACKET ASSIGN exp'
        p[0] = nd.Node('cmdid', [ p[3], p[6] ], [ p[1], p[2], p[4], p[5] ])

    #--------------EXP--------------#
    def p_exp_exp(self, p):
        'exp : exp AND rexp'
        p[0] = nd.Node('expexp', [ p[1], p[3] ], [ p[2] ])

    def p_exp_rexp(self, p):
        'exp : rexp'
        p[0] = nd.Node('exprexp', [ p[1] ], [])

    #--------------REXP--------------#
    def p_rexp_rexp(self, p):
        """rexp : rexp LTHAN aexp
                | rexp GTHAN aexp
                | rexp EQUALS aexp
                | rexp NOTEQ aexp
        """
        p[0] = nd.Node('rexprexp', [ p[1], p[3] ], [ p[2] ])

    def p_resp_aexp(self, p):
        'rexp : aexp'
        p[0] = nd.Node('respaexp', [ p[1] ], [])

    #--------------AEXP--------------#
    def p_aexp_aexp(self, p):
        """aexp : aexp PLUS aexp
                | aexp MINUS aexp
        """
        p[0] = nd.Node('aexpaexp', [ p[1], p[3] ], [ p[2] ])

    def p_aexp_mexp(self, p):
        'aexp : mexp'
        p[0] = nd.Node('aexpmexp', [ p[1] ], [])
    
    #--------------MEXP--------------#
    def p_mexp_mexp(self, p):
        'mexp : mexp TIMES mexp'
        p[0] = nd.Node('mexpmexp', [ p[1], p[3] ], [ p[2] ])

    def p_mexp_sexp(self, p):
        'mexp : sexp'
        p[0] = nd.Node('mexpsexp', [ p[1] ], [])

    #--------------SEXP--------------#
    def p_sexp_not(self, p):
        'sexp : NOT sexp'
        p[0] = nd.Node('sexpnot', [ p[2] ], [ p[1] ])
    
    def p_sexp_minus(self, p):
        'sexp : MINUS sexp %prec UMINUS'
        p[0] = nd.Node('sexpminus', [ p[2] ], [ p[1] ])

    def p_sexp_true(self, p):
        'sexp : TRUE'
        p[0] = nd.Node('sexptrue', [  ], [ p[1] ])

    def p_sexp_false(self, p):
        'sexp : FALSE'
        p[0] = nd.Node('sexpfalse', [  ], [ p[1] ])

    def p_sexp_number(self, p):
        'sexp : NUMBER'
        p[0] = nd.Node('sexpnumber', [  ], [ p[1] ])

    def p_sexp_null(self, p):
        'sexp : NULL'
        p[0] = nd.Node('sexpnull', [  ], [ p[1] ])

    def p_sexp_new(self, p):
        'sexp : NEW INT LSBRACKET exp RSBRACKET'
        p[0] = nd.Node('sexpnew', [ p[4] ], [ p[1], p[2], p[3], p[5] ])

    def p_sexp_dot(self, p):
        'sexp : pexp DOT LENGTH'
        p[0] = nd.Node('sexpdot', [ p[1] ], [ p[2], p[3] ])

    def p_sexp_lsb(self, p):
        'sexp : pexp LSBRACKET exp RSBRACKET'
        p[0] = nd.Node('sexplsb', [ p[1], p[3] ], [ p[2], p[4] ])

    def p_sexp_pexp(self, p):
        'sexp : pexp'
        p[0] = nd.Node('sexppexp', [ p[1] ], [  ])

    #--------------PEXP--------------#
    def p_pexp_id(self, p):
        'pexp : ID'
        p[0] = nd.Node('pexpid', [  ], [ p[1] ])

    def p_pexp_this(self, p):
        'pexp : THIS'
        p[0] = nd.Node('pexpthis', [  ], [ p[1] ])

    def p_pexp_new(self, p):
        'pexp : NEW ID LPAREN RPAREN'
        p[0] = nd.Node('pexpnew', [  ], [ p[1], p[2], p[3], p[4] ])

    def p_pexp_lp(self, p):
        'pexp : LPAREN exp RPAREN'
        p[0] = nd.Node('pexplp', [ p[2] ], [ p[1], p[3] ])

    def p_pexp_pexp(self, p):
        'pexp : pexp DOT ID'
        p[0] = nd.Node('pexppexp', [ p[1] ], [ p[2], p[3] ])

    def p_pexp_pexplp(self, p):
        'pexp : pexp DOT ID LPAREN optexps RPAREN'
        p[0] = nd.Node('pexppexplp', [ p[1] ], [ p[2], p[3] ])

    #--------------EXPS--------------#
    def p_exps_exp(self, p):
        'exps : exp loopvirgulaexp'
        p[0] = nd.Node('expsexp', [ p[1], p[2] ], [])

    #--------------[OPICIONAL]--------------#
    def p_optextends_part(self, p):
        """optextends : EXTENDS ID
                      |
        """
        if(len(p) > 1): # não é produção epsilon
            p[0] = nd.Node('optextends', [], [ p[1], p[2] ])
        else:
            pass

    def p_optparams_part(self, p):
        """optparams : params
                     |
        """
        if(len(p) > 1): # não é produção epsilon
            p[0] = nd.Node('optparams', [ p[1] ], [])
        else:
            pass

    def p_optexps_part(self, p):
        """optexps : exps optexps
                   |
        """
        if(len(p) > 1): # não é produção epsilon
            p[0] = nd.Node('optparams', [ p[1] ], [])
        else:
            pass

    #--------------{LOOP}--------------#
    def p_loopvar_ini(self, p):
        """loopvar : var loopvar 
                   |
        """
        if(len(p) > 1): # não é produção epsilon
            p[0] = nd.Node('loopvar', [ p[1] ], [])
        else:
            pass

    def p_loopmetodo_ini(self, p):
        """loopmetodo : metodo loopmetodo 
                      |
        """
        if(len(p) > 1): # não é produção epsilon
            p[0] = nd.Node('loopmetodo', [ p[1] ], [])
        else:
            pass

    def p_loopclasse_ini(self, p):
        """loopclasse : classe loopclasse
                      |
        """
        if(len(p) > 1): # não é produção epsilon
            p[0] = nd.Node('loopclasse', [ p[1] ], [])
        else:
            pass

    def p_loopcmd_ini(self, p):
        """loopcmd : cmd loopcmd
                   |
        """
        if(len(p) > 1): # não é produção epsilon
            p[0] = nd.Node('loopcmd', [ p[1] ], [])
        else:
            pass

    def p_loopvirgulatipoid_ini(self, p):
        """loopvirgulatipoid : COMMA tipo ID loopvirgulatipoid
                             |
        """
        if(len(p) > 1): # não é produção epsilon
            p[0] = nd.Node('loopvirgulatipoid', [ p[2] ], [ p[1], p[2] ])
        else:
            pass
    
    def p_loopvirgulaexp_ini(self, p):
        """loopvirgulaexp : COMMA exp loopvirgulaexp
                          |
        """
        if(len(p) > 1): # não é produção epsilon
            p[0] = nd.Node('loopvirgulatipoid', [ p[2] ], [ p[1] ])
        else:
            pass
    #------------------------------FIM------------------------------#

    def p_error(self,p):
        print("Syntax error at '%s'" % p.value)

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = {}
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[
                1] + "_" + self.__class__.__name__
        except:
            modname = "parser" + "_" + self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"

        # Build lexer/parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def run(self):
        try:
            f = open("in.txt", "r")
            s = f.read()
            result = yacc.parse(s)
            return result
        except Exception as e:
            print(e)
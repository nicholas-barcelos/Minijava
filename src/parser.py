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
        'System.out.println' : 'SOUT',
        'length' : 'LENGTH',
        'true' : 'TRUE',
        'false' : 'FALSE',
        'this' : 'THIS',
        'new' : 'NEW',
        'null' : 'NULL',
    }

    tokens = list(reserved.values) + [
        'NAME', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
        'LPAREN','RPAREN', 'LSBRACKET', 'RSBRACKET',
        'LCBRACKET', 'RCBRACKET', 'SEMICOLON', 'DOT', 'COMMA', 'LTHAN', 'GTHAN',
        'LTHANEQ', 'GTHANEQ', 'NOTEQ', 'AND', 'NOT'
    ]

    # Tokens

    t_PLUS       = r'\+'
    t_MINUS      = r'\-'
    t_TIMES      = r'\*'
    t_DIVIDE     = r'\/'
    t_EQUALS     = r'\=\='
    t_LPAREN     = r'\('
    t_RPAREN     = r'\)'
    t_ID         = r'[a-zA-Z][a-zA-Z0-9_]*'
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
    t_ignore = r'\f|\t|\r'

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
        ('left','TIMES','DIVIDE'),
        ('right','UMINUS'),
    )

    #------------------------------REGRAS GRAMATICAIS------------------------------#
    def p_prog_main(self, p):
        'prog : main LCBRACKET classe RCBRACKET'
        p[0] = nd.Node('prog0', [p[1], p[3]], [p[2], p[4]])

    def p_main_class(self,p):
        'main : CLASS ID LCBRACKET PUBLIC STATIC VOID MAIN LPAREN STRING LSBRACKET RSBRACKET ID RPAREN LCBRACKET cmd RCBRACKET RCBRACKET'
        p[0] = nd.Node('main', [ p[2], p[12], p[15] ] , [ p[1], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[13], p[14], p[16], p[17] ])

    def p_classe_id(self,p):
        'classe : CLASS ID optextends LCBRACKET loopvar loopmetodo RCBRACKET'
        p[0] = nd.Node('classe', [ p[1], p[2], p[3], p[5], p[6] ] , [ p[4], p[7]] )

    def p_optextends_part(self,p):
        """optextends : EXTENDS ID
                      |
        """
        p[0] = nd.Node('optextends', [p[2]], [p[1]])

    def p_loopvar_ini(self,p):
        """loopvar : var loopvar 
                   |
        """
        p[0] = nd.Node('loopvar', [p[1]], [])

    def p_loopmetodo_ini(self,p):
        """loopmetodo : metodo loopmetodo 
                      |
        """
        p[0] = nd.Node('loopmetodo', [p[1]], [])

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
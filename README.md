# Minijava+

É um subconjunto da linguagem Java para o trabalho de implementação da disciplina de Compiladores 2019.2 - UFF.

## Execução

Para executar, basta rodar o seguinte comando, onde `in.txt` é a entrada do parser:

```
python main.py in.txt
```

Caso tenha graphviz instalado, pode-se executar da seguinte forma:

```
python main.py in.txt -g | dot -T png | display
```

Para instalar o graphviz em distros baseadas em debian

`sudo apt-get install graphviz`

## Implementação

A implementação do parser foi feita utilizando a linguagem Python com o auxílio da biblioteca Python Lex-Yacc ou PLY, desenvolvida com intuito educacional para ensino de compiladores.

YACC usa uma técnica _bottom up_ chamada _LR Parsing_ ou _Shift-Reducing Parsing_.

Nesta biblioteca, cada regra gramatical é definida por uma função em Python que contém a especificação GLC.

## Sintaxe da Linguagem

Segue abaixo a definição original da sintaxe, escrita em EBNF.

```
PROG    -> MAIN {CLASSE}

MAIN    -> class id '{' public static void main '('String '['']'id ')''{' CMD '}' '}'

CLASSE  -> class id [extends id] '{' {VAR} {METODO} '}'

VAR     -> TIPO id ;

METODO  -> public TIPO id '(' [PARAMS] ')' '{' {VAR} {CMD} return EXP ; '}'

PARAMS  -> TIPO id {, TIPO id}

TIPO    -> int '[' ']'
            | boolean
            | int
            | id

CMD     -> '{' {CMD} '}'
            | if '(' EXP ')' CMD
            | if '(' EXP ')' CMD else CMD
            | while '(' EXP ')' CMD
            | System.out.println '(' EXP ')' ;
            | id = EXP ;
            | id'[' EXP ']' = EXP ;

EXP     -> EXP && REXP
            | REXP

REXP    -> REXP < AEXP
            | REXP == AEXP
            | REXP != AEXP
            | AEXP

AEXP    -> AEXP + MEXP
            | AEXP - MEXP
            | MEXP

MEXP    -> MEXP * SEXP
            | SEXP

SEXP    -> ! SEXP
            | -SEXP
            | true
            | false
            | num
            | null
            | new int '[' EXP ']'
            | PEXP . length
            | PEXP '[' EXP ']'
            | PEXP

PEXP    -> id
            | this
            | new id '(' ')'
            | '(' EXP ')'
            | PEXP . id
            | PEXP . id '(' [EXPS] ')'

EXPS    -> EXP {, EXP}
```

Contudo, para implementação desta linguagem, tivemos que adaptar a gramática. A seguir, a gramática reescrita:

```
PROG                -> MAIN LOOPCLASSE

MAIN                -> class id '{' public static void main '('String '['']' id ')''{' CMD '}' '}'

CLASSE              -> class id OPTEXTENDS '{' LOOPVAR LOOPMETODO '}'

VAR                 -> TIPO id ';'

METODO              -> public TIPO id '(' OPTPARAMS ')' '{' LOOPVAR LOOPCMD RETURN EXP ';' '}'

PARAMS              -> TIPO id LOOPVIRGULATIPOID

TIPO                -> int '['']'
                        | boolean
                        | int
                        | id

CMD                 -> '{' LOOPCMD '}'
                        | if '(' EXP ')' CMD
                        | if '(' EXP ')' CMD else CMD
                        | while '(' EXP ')' CMD
                        | System.out.println '(' EXP ')' ;
                        | id '=' EXP ;
                        | id '[' EXP ']' '=' EXP ;

EXP                 -> EXP and REXP
                        | REXP

REXP                -> REXP '<' AEXP
                        | REXP '>' AEXP
                        | REXP '==' AEXP
                        | REXP '!=' AEXP
                        | REXP '<=' AEXP
                        | REXP '=>' AEXP
                        | AEXP

AEXP                -> AEXP '+' AEXP
                        | AEXP '-' AEXP
                        | MEXP

MEXP                -> MEXP '*' MEXP
                        | SEXP

SEXP                -> '!' SEXP
                        | '-' SEXP %prec UMINUS
                        | true
                        | false
                        | NUMBER
                        | null
                        | new int '[' EXP ']'
                        | PEXP . length
                        | PEXP '[' EXP ']'
                        | PEXP

PEXP                -> id
                        | this
                        | new id '('')'
                        | '(' EXP ')'
                        | PEXP . id
                        | PEXP . id '(' OPTEXPS ')'

EXPS                -> EXP LOOPVIRGULAEXP

OPTEXTENDS          -> extends id
                        | ε

OPTPARAMS           -> PARAMS
                        | ε

OPTEXPS             -> EXPS
                        | ε

LOOPVAR             -> var LOOPVAR
                        | ε

LOOPMETODO          -> METODO LOOPMETODO
                        | ε

LOOPCLASSE          -> CLASSE LOOPCLASSE
                        | ε

LOOPCMD             -> CMD LOOPCMD
                        | ε

LOOPVIRGULATIPOID   -> ',' TIPO id LOOPVIRGULATIPOID
                        | ε

LOOPVIRGULAEXP      -> ',' EXP LOOPVIRGULAEXP
                        | ε


```

## Palavras Reservadas

A seguir a lista de palavras reservadas:

```
boolean, class, extends, public, static, void, main, String,
return, int, if, else, while, length, true, false, this,
new, null, System.out.println
```

## TOKENS

A seguir, a lista de tokens e suas expressões regulares:

```
'ID'        : 'System.out.println|[a-zA-Z][a-zA-Z_0-9]*'
'NUMBER'    : '[0-9]+'
'PLUS'      : '\+'
'MINUS'     : '\-'
'TIMES'     : '\*'
'EQUALS'    : '\=\='
'LPAREN'    : '\('
'RPAREN'    : '\)'
'LSBRACKET' : '\['
'RSBRACKET' : '\]'
'LCBRACKET' : '\{'
'RCBRACKET' : '\}'
'SEMICOLON' : ';'
'DOT'       : '\.'
'COMMA'     : ','
'LTHAN'     : '\<'
'GTHAN'     : '\>'
'LTHANEQ'   : '\<\='
'GTHANEQ'   : '\>\='
'NOTEQ'     : '\!\='
'AND'       : '\&\&'
'NOT'       : '\!'
'ASSIGN'    : '\='
```

## Comentários

A linguagem Minijava+ suporta comentários de uma linha, utilizando `\\` e comentários de múltiplas linhas utilizando `\**\`

## Referências
- [Parser](https://www.dabeaz.com/ply/)
- [Gramática](http://www.cead.uff.br/ead/mod/resource/view.php?id=41439)

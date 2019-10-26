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

YACC usa uma técnica _bottom up_ chamada _LALR Parsing_ ou _Shift-Reducing Parsing_. A análise _bottom up_ possui a vantagem de suportar gramáticas mais gerais. Por exemplo, recursão à esquerda e prefixos comuns não são problemáticos.

Já a técnica _Shift-Reducing_ utiliza as ações _shift_ (em que se desloca o ponteiro para a direita) e _reduce_ (em que realiza uma redução, isto é, substituir uma cadeia de caracteres por sua regra gramatical). A tarefa do analisador _Shift-Reduce_ é encontrar a próxima redução a ser realizada em cada passo.

Em nossa implementação, no arquivo `parser.py`, pode-se encontrar duas partes bem específicas do código: o Lexer e o Parser.

### Lexer

Iniciamos por listar as palavras reservadas da linguagem e associá-las ao token correspondente. Em seguida, criamos uma lista tokens que une tanto as palavras não-reservadas quanto as reservadas.

Os tokens de palavras não-reservadas são descritos por meio de expressões regulares. A biblioteca os reconhece por meio de variáveis e métodos iniciados com `t_`. Aqui há considerações a serem feitas:

-  as palavras reservadas podem ser facilmente confundidas com um _identificador_ e, por isso, foi necessário um método para descrever o identificador para que descartássemos uma palavra reservada antes de identificá-la como um token;

- Os blocos de comentários, definidos por `\\` (comentários de uma linha) e `\**\` (comentários de múltiplas linhas) devem ser ignorados durante o parsing, assim como linhas em branco. Um método foi criado para esta descrição e a utilização da variável `t_ignore`;

- O número de linhas do código é contado pela quantidade de `new lines (\n)` encontrados;

- O encontro de erros, isto é, palavras que não pertencem à linguagem especificada são comunicados e dada a continuidade da análise léxica.

### Parser

A seguir iniciamos a implementação do parser com a especificação da precedência dos operadores aritméticos. A biblioteca nos permite isso por meio da tupla `precendence` onde informamos da menor para a maior e o lado da associatividade.

Numa análise posterior identificamos a falta de necessidade desta especificação pois a gramática em si já especificava essa precedência. Entretanto, não tivemos tempo hábil de teste e, por isso, decidimos por manter a especificação de precedência nesta versão.

Continuamos por definir as regras gramaticais. A biblioteca reconhece as definições utilizadas no parser por meio de identificadores iniciados por `p_`.

Cada regra gramatical é definida por uma função que contém a regra em GLC. Cada função desse tipo aceita um argumento `p` que contém a sequência dos valores de cada símbolo gramatical correspondente, como no exemplo a seguir:

```
def p_var_tipo(self, p):
    'var : tipo ID SEMICOLON'
    # ^     ^    ^    ^
    # p[0] p[1] p[2] p[3]
    p[0] = nd.Node('var', [ p[1]], [ p[2], p[3] ])
```

O valor em `p[0]` é utilizado para identificar o valor final da análise.

Para finalizar a descrição do parser, resta explicar que há uma regra especificada para quando há erros de sintaxe e, para isso, utiliza-se o método `p_error`.

### Visão Geral

A main inicia o programa lendo os argumentos de entrada que podem ser o arquivo e a flag `-g` que permite gerar uma visualização da árvore de saída do parser utilizando a biblioteca `graphviz`.

Cria-se, então, uma instância da classe `Parser` que contém a inicialização da bilioteca com a identificação dos arquivos que irão armazenar o log de debug e a tabela de símbolos gerada. E a execução do parser, no método `Parser#run` passando o arquivo de entrada como argumento.

Este, por sua vez, irá fazer a leitura do arquivo e fechá-lo automática (por conta da declaração `with`) e enviar os resultados para o YACC.

Ao finalizar a análise, se verifica se a saída deve ser utilizando o `graphviz` ou apenas a saída textual que o `graphviz` utilizaria.

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

Contudo, foi necessário adaptar a gramática para utilizar BNF, criando regras para as repetições e opcionais.

A necessidade de utilizar uma gramática em BNF é uma limitação da biblioteca utilizada.

A seguir, a gramática reescrita:

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
'ID'        : '[a-zA-Z][a-zA-Z_0-9]*'
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
'BOOLEAN'   : 'boolean'
'CLASS'     : 'class'
'EXTENDS'   : 'extends'
'PUBLIC'    : 'public'
'STATIC'    : 'static'
'VOID'      : 'void'
'MAIN'      : 'main'
'STRING'    : 'String'
'RETURN'    : 'return'
'INT'       : 'int'
'IF'        : 'if'
'ELSE'      : 'else'
'WHILE'     : 'while'
'LENGTH'    : 'length'
'TRUE'      : 'true'
'FALSE'     : 'false'
'THIS'      : 'this'
'NEW'       : 'new'
'NULL'      : 'null'
'SOUT'      : 'System.out.println'
```

## Referências
- [Parser](https://www.dabeaz.com/ply/)
- [Gramática](http://www.cead.uff.br/ead/mod/resource/view.php?id=41439)

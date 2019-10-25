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

Contudo, esta linguagem possui ambiguidades que precisaram ser tratadas. A seguir a gramática reescrita:

```
```

## Referências
- [Parser](https://www.dabeaz.com/ply/)
- [Gramática](http://www.cead.uff.br/ead/mod/resource/view.php?id=41439)

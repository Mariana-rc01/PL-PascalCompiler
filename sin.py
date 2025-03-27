import ply.yacc as yacc
from lex import tokens, literals, reserved

"""
P = {
    Program : Header Content '.'

    Header : PROGRAM identifier ListArgs ';'

    Content : BEGIN ListStatement END

    ListStatement : ListStatement Statement
        | Statement
    
    Statement : identifier '(' ListArgs ')' ';'

    ListArgs : ListArgs ',' Arg
            | Arg

    Arg : string
}
"""

def p_Program(p):
    "Program : Header Content '.'"

def p_Header(p):
    "Header : PROGRAM identifier ';'"

def p_Content(p):
    "Content : BEGIN ListStatement END"

def p_ListStatement(p):
    "ListStatement : ListStatement Statement"

def p_ListStatement_Statement(p):
    "ListStatement : Statement"

def p_Statement(p):
    "Statement : identifier '(' ListArgs ')' ';'"

def p_ListArgs(p):
    "ListArgs : ListArgs ',' Arg"

def p_ListArgs_Arg(p):
    "ListArgs : Arg"

def p_Arg(p):
    "Arg : string"

def p_error(p):
    print('Erro sintático: ', p)
    parser.success = False

# Build the parser
parser = yacc.yacc()

import sys

text = sys.stdin.read()
parser.success = True
result = parser.parse(text)
if parser.success:
    print('Frase válida!')
else:
    print('Frase inválida... Corrija e tente novamente!')

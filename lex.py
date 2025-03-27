import ply.lex as lex

# TODO'S
"""
- Acrescentámos os tokens (for, to, do) e literals (+, -, *, /)
- num_real
- Falta tratar de :=
"""

literals = [';', ',', '(', ')', '.', '+', '-', '*', '/']

reserved = {
    "program" : "PROGRAM",
    "begin" : "BEGIN",
    "end" : "END",
    "for" : "FOR",
    "to" : "TO",
    "do" : "DO"
}

# Tokens
tokens = [
    'identifier',  # Adiciona o token para identificadores
    'string',
    'num_int'
    # 'num_real'
] + list(reserved.values())  # Adiciona as palavras reservadas como tokens

# Regras para tokens
def t_identifier(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Verifica se a palavra está na lista de reservadas
    t.type = reserved.get(t.value.lower(), 'identifier')
    return t

def t_string(t):
    r'\'.*?\''
    t.value = t.value[1:-1]
    return t

t_ignore = " \t\n"

def t_error(t):
    print('Caratér ilegal: ', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

import sys

for linha in sys.stdin:
    lexer.input(linha)
    for tok in lexer:
        print(tok)

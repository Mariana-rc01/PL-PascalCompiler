import ply.lex as lex

# TODO'S
"""
- Tratar dos casos específicos do ':' e '='
"""

literals = [';', ',', '(', ')', '.']

reserved = {
    "program" : "PROGRAM",
    "var" : "VAR",
    "begin" : "BEGIN",
    "end" : "END",
    "for" : "FOR",
    "array" : "ARRAY",
    "integer" : "INTEGER",
    "writeln" : "WRITELN"
}

# Tokens
tokens = [
    'identifier',  # Adiciona o token para identificadores
    'string'
] + list(reserved.values())  # Adiciona as palavras reservadas como tokens

# Regras para tokens
def t_identifier(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Verifica se a palavra está na lista de reservadas
    t.type = reserved.get(t.value.lower(), 'identifier')
    return t

def t_string(t):
    r'\'([^\'])*?\''
    t.value = t.value[1:-1]
    return t

t_ignore = " \t\n"

def t_error(t):
    print('Caratér ilegal: ', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

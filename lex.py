import ply.lex as lex

literals = [';', ',', '(', ')', '.', '+', '-', '*', '/', '[', ']']

reserved = {
    "program" : "PROGRAM",
    "procedure" : "PROCEDURE",
    "function" : "FUNCTION",
    "begin" : "BEGIN",
    "end" : "END",
    "for" : "FOR",
    "to" : "TO",
    "do" : "DO",
    "and": "AND",
    "or" : "OR",
    "if" : "IF",
    "then" : "THEN",
    "else" : "ELSE",
    "downto" : "DOWNTO",
    "mod" : "MOD",
    "div" : "DIV",
    "not" : "NOT",
    "while" : "WHILE",
    "var" : "VAR",
    "array" : "ARRAY",
    "of" : "OF",
    "true" : "TRUE",
    "false" : "FALSE"
}

# Tokens
tokens = [
    'identifier',
    'char',
    'string',
    'num_int',
    'ASSIGN',
    'EQUAL',
    'COLON',
    'GREATER_THAN',
    'LESS_THAN',
    'NOT_EQUAL',
    'GREATER_THAN_EQUAL',
    'LESS_THAN_EQUAL',
    'num_real'
] + list(reserved.values())  # Adiciona as palavras reservadas como tokens

# Regras para tokens
def t_identifier(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Verifica se a palavra está na lista de reservadas
    t.type = reserved.get(t.value.lower(), 'identifier')
    return t

def t_char(t):
    r'\'[^\'\n]\''
    t.value = t.value[1:-1]
    return t

def t_string(t):
    r'\'.*?\''
    t.value = t.value[1:-1]
    return t

def t_num_real(t):
    r'\d+((\.\d+([eE][+-]?\d+)?)|[eE][+-]?\d+)'
    return t

def t_num_int(t):
    r'\d+'
    return t

# Literals

def t_ASSIGN(t):
    r':='
    return t

def t_EQUAL(t):
    r'='
    return t

def t_COLON(t):
    r':'
    return t

def t_GREATER_THAN_EQUAL(t):
    r'>='
    return t

def t_LESS_THAN_EQUAL(t):
    r'<='
    return t

def t_GREATER_THAN(t):
    r'>'
    return t

def t_LESS_THAN(t):
    r'<'
    return t

def t_NOT_EQUAL(t):
    r'<>'
    return t

def t_comment(t):
    r'\(\*(.|\n)*?\*\)|{(.|\n)*?}'
    pass

t_ignore = " \t\n"

def t_error(t):
    print('Caratér ilegal: ', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
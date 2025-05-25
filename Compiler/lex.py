import re
import ply.lex as lex

literals = [';', ',', '(', ')', '.', '+', '-', '*', '/', '[', ']']

# Tokens
tokens = [
    'PROGRAM',
    'PROCEDURE',
    'FUNCTION',
    'BEGIN',
    'END',
    'FOR',
    'TO',
    'DO',
    'AND',
    'OR',
    'IF',
    'THEN',
    'ELSE',
    'DOWNTO',
    'MOD',
    'DIV',
    'NOT',
    'WHILE',
    'VAR',
    'ARRAY',
    'OF',
    'TRUE',
    'FALSE',
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
]

def t_PROGRAM(t):
    r'\bprogram\b'
    t.type = 'PROGRAM'
    return t

def t_PROCEDURE(t):
    r'\bprocedure\b'
    t.type = 'PROCEDURE'
    return t

def t_FUNCTION(t):
    r'\bfunction\b'
    t.type = 'FUNCTION'
    return t

def t_BEGIN(t):
    r'\bbegin\b'
    t.type = 'BEGIN'
    return t

def t_END(t):
    r'\bend\b'
    t.type = 'END'
    return t

def t_FOR(t):
    r'\bfor\b'
    t.type = 'FOR'
    return t

def t_TO(t):
    r'\bto\b'
    t.type = 'TO'
    return t

def t_DOWNTO(t):
    r'\bdownto\b'
    t.type = 'DOWNTO'
    return t

def t_DO(t):
    r'\bdo\b'
    t.type = 'DO'
    return t

def t_AND(t):
    r'\band\b'
    t.type = 'AND'
    return t

def t_OR(t):
    r'\bor\b'
    t.type = 'OR'
    return t

def t_IF(t):
    r'\bif\b'
    t.type = 'IF'
    return t

def t_THEN(t):
    r'\bthen\b'
    t.type = 'THEN'
    return t

def t_ELSE(t):
    r'\belse\b'
    t.type = 'ELSE'
    return t

def t_MOD(t):
    r'\bmod\b'
    t.type = 'MOD'
    return t

def t_DIV(t):
    r'\bdiv\b'
    t.type = 'DIV'
    return t

def t_NOT(t):
    r'\bnot\b'
    t.type = 'NOT'
    return t

def t_WHILE(t):
    r'\bwhile\b'
    t.type = 'WHILE'
    return t

def t_VAR(t):
    r'\bvar\b'
    t.type = 'VAR'
    return t

def t_ARRAY(t):
    r'\barray\b'
    t.type = 'ARRAY'
    return t

def t_OF(t):
    r'\bof\b'
    t.type = 'OF'
    return t

def t_TRUE(t):
    r'\btrue\b'
    t.type = 'TRUE'
    return t

def t_FALSE(t):
    r'\bfalse\b'
    t.type = 'FALSE'
    return t

# Regras para tokens
def t_identifier(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
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
    print('Illegal character: ', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex(reflags=re.IGNORECASE)
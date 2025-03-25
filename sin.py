import ply.yacc as yacc
from cinema_lex import tokens, literals

"""
P = {
    Program : Header Content '.'

    Header : PROGRAM identifier ';'

    Content : Statements

    Statements : BEGIN Lines END
}
"""
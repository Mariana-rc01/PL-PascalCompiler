import ply.yacc as yacc
from lex import tokens, literals, reserved

# Nota
"""
- Nas condições ter atenção a decidir se é lazy ou não.
"""

# TODO'S
"""
- Sinais para os números (done) e transforma diretamente no sintático no número correto (-2 fica como p(0) = 0-2)
- Modular Statements
- Definição para constantes e var
"""

def p_Program(p):
    "Program : Header Content '.'"

def p_Header(p):
    "Header : PROGRAM identifier '(' ListH ')' ';'"

def p_Header_PROGRAM(p):
    "Header : PROGRAM identifier ';'"

def p_ListH(p):
    "ListH : ListH ',' identifier"

def p_ListH_identifier(p):
    "ListH : identifier"

def p_Content(p):
    "Content : CompoundStatement"

def p_CompoundStatement(p):
    "CompoundStatement : BEGIN ListStatement END"

def p_ListStatement(p):
    "ListStatement : ListStatement Statement ';'"

def p_ListStatement_Statement(p):
    "ListStatement : Statement ';'"

def p_Statement(p):
    "Statement : SimpleStatement"

def p_Statement_StructeredStatement(p):
    "Statement : StructeredStatement"

def p_SimpleStatement(p):
    "SimpleStatement : AssignmentStatement"

def p_SimpleStatement_ProcedureStatement(p):
    "SimpleStatement : ProcedureStatement"

def p_AssignmentStatement(p):
    "AssignmentStatement : Variable ASSIGN Expression"

def p_ProcedureStatement(p):
    "ProcedureStatement : identifier '(' ListArgs ')'"

def p_ProcedureStatement_identifier(p):
    "ProcedureStatement : identifier '(' ')'"

def p_ListArgs(p):
    "ListArgs : ListArgs ',' Arg"

def p_ListArgs_Arg(p):
    "ListArgs : Arg"

#def p_Arg(p):
#    "Arg : identifier"

# a Expression engloba o identifier, Variable e string, então dava warning de reduce/reduce
def p_Arg_Expression(p):
    "Arg : Expression"

#def p_Arg_Variable(p):
#    "Arg : Variable"

#def p_Arg_string(p):
#    "Arg : string"

def p_StructeredStatement(p):
    "StructeredStatement : CompoundStatement"

def p_StructeredStatement_ConditionalStatement(p):
    "StructeredStatement : ConditionalStatement"

def p_StructeredStatement_RepetitiveStatement(p):
    "StructeredStatement : RepetitiveStatement"

def p_ConditionalStatement(p):
    "ConditionalStatement : IfStatement"

def p_IfStatement(p):
    "IfStatement : IF Expression THEN Statement"

def p_IfStatement_ELSE(p):
    "IfStatement : IF Expression THEN Statement ELSE Statement"

def p_RepetitiveStatement(p):
    "RepetitiveStatement : WhileStatement"

def p_RepetitiveStatement_ForStatement(p):
    "RepetitiveStatement : ForStatement"

def p_WhileStatement(p):
    "WhileStatement : WHILE Expression DO Statement"

def p_ForStatement(p):
    "ForStatement : FOR identifier ASSIGN Expression TO Expression DO Statement"

def p_ForStatement_FOR(p):
    "ForStatement : FOR identifier ASSIGN Expression DOWNTO Expression DO Statement"

def p_Expression(p):
    "Expression : SimpleExpression RelationalOperator Expression"

def p_Expression_SimpleExpression(p):
    "Expression : SimpleExpression"

def p_RelationalOperator(p):
    "RelationalOperator : EQUAL"

def p_RelationalOperator_GREATER_THAN(p):
    "RelationalOperator : GREATER_THAN"

def p_RelationalOperator_LESS_THAN(p):
    "RelationalOperator : LESS_THAN"

def p_RelationalOperator_NOT_EQUAL(p):
    "RelationalOperator : NOT_EQUAL"

def p_RelationalOperator_GREATER_THAN_EQUAL(p):
    "RelationalOperator : GREATER_THAN_EQUAL"

def p_RelationalOperator_LESS_THAN_EQUAL(p):
    "RelationalOperator : LESS_THAN_EQUAL"

def p_SimpleExpression(p):
    "SimpleExpression : Sign Term SecondPriorityOperator SimpleExpression"

def p_SimpleExpression_List(p):
    "SimpleExpression : Term SecondPriorityOperator SimpleExpression"

def p_SimpleExpression_Term(p):
    "SimpleExpression : Term"

def p_SecondPriorityOperator(p):
    "SecondPriorityOperator : '+'"

def p_SecondPriorityOperator_MINUS(p):
    "SecondPriorityOperator : '-'"

def p_SecondPriorityOperator_OR(p):
    "SecondPriorityOperator : OR"

def p_Sign(p):
    "Sign : '+'"

def p_Sign_MINUS(p):
    "Sign : '-'"

def p_Term(p):
    "Term : Factor FirstPriorityOperator Term"

def p_Term_Factor(p):
    "Term : Factor"

def p_FirstPriorityOperator(p):
    "FirstPriorityOperator : '*'"

def p_FirstPriorityOperator_DIVISION(p):
    "FirstPriorityOperator : '/'"

def p_FirstPriorityOperator_DIV(p):
    "FirstPriorityOperator : DIV"

def p_FirstPriorityOperator_MOD(p):
    "FirstPriorityOperator : MOD"

def p_FirstPriorityOperator_AND(p):
    "FirstPriorityOperator : AND"

def p_Factor(p):
    "Factor : '(' Expression ')'"

def p_Factor_Variable(p):
    "Factor : Variable"

def p_Factor_UnsignedConstant(p):
    "Factor : UnsignedConstant"

def p_Factor_FunctionDesignator(p):
    "Factor : FunctionDesignator"

def p_Factor_NOT(p):
    "Factor : NOT Factor"

def p_FunctionDesignator(p):
    "FunctionDesignator : identifier '(' ListArgs ')'"

def p_FunctionDesignator_identifier(p):
    "FunctionDesignator : identifier '(' ')'"

def p_UnsignedConstant(p):
    "UnsignedConstant : UnsignedNumber"

def p_UnsignedConstant_string(p):
    "UnsignedConstant : string"

def p_Constant(p):
    "Constant : UnsignedNumber"

def p_Constant_Sign(p):
    "Constant : Sign UnsignedNumber"

def p_Constant_string(p):
    "Constant : string"

def p_UnsignedNumber(p):
    "UnsignedNumber : num_int"

def p_UnsignedNumber_num_real(p):
    "UnsignedNumber : num_real"

def p_Variable(p):
    "Variable : identifier"

def p_Variable_identifier(p):
    "Variable : identifier '[' ListExpressions ']'"

def p_ListExpressions(p):
    "ListExpressions : ListExpressions ',' Expression"

def p_ListExpressions_Expression(p):
    "ListExpressions : Expression"

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

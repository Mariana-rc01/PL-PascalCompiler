import ply.yacc as yacc
from lex import tokens, literals, reserved
from astree import ASTNode

# Regra Principal
def p_Program(p):
    "Program : Header Content '.'"
    p[0] = ASTNode("Program", [p[1], p[2]])
    #print("Debug: Program ->")
    #print(p[0])

# Cabeçalho do Programa
def p_Header(p):
    "Header : PROGRAM identifier '(' ListH ')' ';'"
    p[0] = ASTNode("Header", [ASTNode("Identifier", value=p[2]), p[4]])
    
def p_Header_PROGRAM(p):
    "Header : PROGRAM identifier ';'"
    p[0] = ASTNode("Header", [ASTNode("Identifier", [ASTNode(p[2])])])

def p_ListH(p):
    "ListH : ListH ',' identifier"
    # Adiciona o identificador à lista
    # Aqui assume-se que p[1] já é um nó com a lista de identificadores
    p[0] = ASTNode("IdentifierList", p[1].children + [ASTNode("Identifier", value=p[3])])
    
def p_ListH_identifier(p):
    "ListH : identifier"
    p[0] = ASTNode("IdentifierList", [ASTNode("Identifier", value=p[1])])

# Conteúdo do Programa
def p_Content(p):
    "Content : Declarations CompoundStatement"
    p[0] = ASTNode("Content", [p[1], p[2]])

# Declarações
def p_Declarations_variable(p):
    "Declarations : Declarations VariableDeclarationPart"
    p[0] = ASTNode("Declarations", [p[1], p[2]])

def p_Declarations_procedure(p):
    "Declarations : Declarations ProcedureDeclarationPart"
    p[0] = ASTNode("Declarations", [p[1], p[2]])

def p_Declarations_function(p):
    "Declarations : Declarations FunctionDeclarationPart"
    p[0] = ASTNode("Declarations", [p[1], p[2]])

def p_Declarations_empty(p):
    "Declarations : "
    p[0] = ASTNode("Declarations", [])

# Declaração de Variáveis
def p_VariableDeclarationPart(p):
    "VariableDeclarationPart : VAR ListVarsDeclaration"
    p[0] = ASTNode("VarDeclaration", [p[2]])

def p_ListVarsDeclaration(p):
    "ListVarsDeclaration : ListVarsDeclaration ElemVarsDeclaration ';'"
    p[0] = ASTNode("ListVarDeclaration", [p[1], p[2]])

def p_ListVarsDeclaration_ElemVarsDeclaration(p):
    "ListVarsDeclaration : ElemVarsDeclaration ';'"
    p[0] = ASTNode("ListVarDeclaration", [p[1]])

def p_ElemVarsDeclaration_identifier(p):
    "ElemVarsDeclaration : IdentifierList COLON identifier"
    # Aqui, estamos concatenando a lista de identificadores com o tipo
    p[0] = ASTNode("VarElemDeclaration", [p[1], ASTNode("Type", value=p[3])])

def p_ElemVarsDeclaration_array(p):
    "ElemVarsDeclaration : IdentifierList COLON Array"
    p[0] = ASTNode("VarElemDeclaration", [p[1], p[3]])

def p_Array(p):
    "Array : ARRAY '[' Constant '.' '.' Constant ']' OF identifier"
    # Pode ser melhor estruturado, mas de forma simplificada, concatena os elementos
    p[0] = ASTNode("ArrayType", [ASTNode("LowBound", value=p[3]),
                                  ASTNode("HighBound", value=p[6]),
                                  ASTNode("Type", value=p[9])])

def p_IdentifierList(p):
    "IdentifierList : IdentifierList ',' identifier"
    p[0] = ASTNode("IdentifierList", p[1].children + [ASTNode("Identifier", value=p[3])])

def p_IdentifierList_identifier(p):
    "IdentifierList : identifier"
    p[0] = ASTNode("IdentifierList", [ASTNode("Identifier", value=p[1])])

# Declaração de Procedimentos
def p_ProcedureDeclarationPart(p):
    "ProcedureDeclarationPart : PROCEDURE identifier ListParametersDeclaration ';' Content ';'"
    p[0] = ASTNode("ProcedureDeclaration", [ASTNode("Identifier", value=p[2]),
                                             p[3],
                                             p[5]])

# Declaração de Funções
def p_FunctionDeclarationPart(p):
    "FunctionDeclarationPart : FUNCTION identifier ListParametersDeclaration COLON identifier ';' Content ';'"
    p[0] = ASTNode("FunctionDeclaration", [ASTNode("Identifier", value=p[2]),
                                            p[3],
                                            ASTNode("ReturnType", value=p[5]),
                                            p[7]])

def p_ListParametersDeclaration(p):
    "ListParametersDeclaration : '(' ListOfListParameters ')'"
    p[0] = ASTNode("ListParametersDeclaration", value=p[2])

def p_ListOfListParameters(p):
    "ListOfListParameters : ListOfListParameters ';' ListParameters"
    p[0] = ASTNode("ListOfListParameters", [p[1], p[3]])

def p_ListOfListParameters_VAR_R(p):
    "ListOfListParameters : ListOfListParameters ';' VAR ListParameters"
    p[0] = ASTNode("ListOfListParameters", [p[1], p[3]])

def p_ListOfListParameters_single(p):
    "ListOfListParameters : ListParameters"
    p[0] = p[1]

def p_ListOfListParameters_VAR(p):
    "ListOfListParameters : VAR ListParameters"
    p[0] = p[2]

def p_ListParametersDeclaration_empty(p):
    "ListParametersDeclaration : "
    p[0] = ASTNode("Parameters", [])

def p_ListParametersDeclaration_Listempty(p):
    "ListParametersDeclaration : '(' ')'"
    p[0] = ASTNode("Parameters", [])

def p_ListParameters(p):
    "ListParameters : ListParameters ',' ElemParameter"
    p[0] = ASTNode("Parameters", p[1].children + [p[3]])
    #("Debug: ListParameters ->", p[0])

def p_ListParameters_ElemParameter(p):
    "ListParameters : ElemParameter"
    p[0] = ASTNode("Parameters", [p[1]])

def p_ElemParameter(p):
    "ElemParameter : IdentifierList COLON ARRAY OF identifier"
    p[0] = ASTNode("Parameter", [p[1], ASTNode("ArrayType", [ASTNode("Type", value=p[5])])])

def p_ListParameters_ElemParameter_identifier(p):
    "ElemParameter : IdentifierList COLON identifier"
    p[0] = ASTNode("Parameter", [p[1], ASTNode("Type", value=p[3])])
    #print("Debug: ElemParameter ->", p[0])

# Composto de Sentenças
def p_CompoundStatement(p):
    "CompoundStatement : BEGIN ListStatement END"
    p[0] = ASTNode("CompoundStatement", [p[2]])

def p_ListStatement(p):
    "ListStatement : ListStatementAux LastStatement"
    p[0] = ASTNode("ListStatement", [p[1], p[2]])

def p_ListStatementAux(p):
    "ListStatementAux : ListStatementAux Statement ';'"
    p[0] = ASTNode("ListStatementAux", [p[1], p[2]])

def p_ListStatementAux_empty(p):
    "ListStatementAux : "
    p[0] = ASTNode("ListStatementAux", [])

def p_LastStatement(p):
    "LastStatement : Statement"
    p[0] = ASTNode("LastStatement", [p[1]])

def p_LastStatement_empty(p):
    "LastStatement : "
    p[0] = ASTNode("LastStatement", [])

def p_Statement(p):
    "Statement : SimpleStatement"
    p[0] = p[1]

def p_Statement_StructeredStatement(p):
    "Statement : StructeredStatement"
    p[0] = p[1]

# Simples
def p_SimpleStatement(p):
    "SimpleStatement : AssignmentStatement"
    p[0] = p[1]

def p_SimpleStatement_ProcedureStatement(p):
    "SimpleStatement : ProcedureStatement"
    p[0] = p[1]

def p_AssignmentStatement(p):
    "AssignmentStatement : Variable ASSIGN Expression"
    p[0] = ASTNode("Assignment", [p[1], p[3]])

def p_ProcedureStatement(p):
    "ProcedureStatement : identifier '(' ListArgs ')'"
    p[0] = ASTNode("ProcedureCall", [ASTNode("Identifier", value=p[1]), p[3]])

def p_ProcedureStatement_identifier(p):
    "ProcedureStatement : identifier '(' ')'"
    p[0] = ASTNode("ProcedureCall", [ASTNode("Identifier", value=p[1]), ASTNode("Args", [])])

def p_ProcedureStatement_empty(p):
    "ProcedureStatement : identifier"
    p[0] = ASTNode("ProcedureCall", [ASTNode("Identifier", value=p[1]), ASTNode("Args", [])])

def p_ListArgs(p):
    "ListArgs : ListArgs ',' Arg"
    p[0] = ASTNode("Args", p[1].children + [p[3]])

def p_ListArgs_Arg(p):
    "ListArgs : Arg"
    p[0] = ASTNode("Args", [p[1]])

def p_Arg_Expression(p):
    "Arg : Expression"
    p[0] = p[1]

# Estruturados (Ex.: Compound, Condicionais, Repetitivos)
def p_StructeredStatement(p):
    "StructeredStatement : CompoundStatement"
    p[0] = p[1]

def p_StructeredStatement_ConditionalStatement(p):
    "StructeredStatement : ConditionalStatement"
    p[0] = p[1]

def p_StructeredStatement_RepetitiveStatement(p):
    "StructeredStatement : RepetitiveStatement"
    p[0] = p[1]

# Condicional
def p_ConditionalStatement(p):
    "ConditionalStatement : IfStatement"
    p[0] = p[1]

precedence = (
    ('nonassoc', 'IF'),
    ('right', 'ELSE'),
)

def p_IfStatement(p):
    "IfStatement : IF Expression THEN Statement %prec IF"
    p[0] = ASTNode("IfStatement", [p[2], p[4]])

def p_IfStatement_ELSE(p):
    "IfStatement : IF Expression THEN Statement ELSE Statement"
    p[0] = ASTNode("IfStatement", [p[2], p[4], p[6]])

# Repetitivos (While e For)
def p_RepetitiveStatement(p):
    "RepetitiveStatement : WhileStatement"
    p[0] = p[1]

def p_RepetitiveStatement_ForStatement(p):
    "RepetitiveStatement : ForStatement"
    p[0] = p[1]

def p_WhileStatement(p):
    "WhileStatement : WHILE Expression DO Statement"
    p[0] = ASTNode("WhileStatement", [p[2], p[4]])

def p_ForStatement(p):
    "ForStatement : FOR identifier ASSIGN Expression TO Expression DO Statement"
    p[0] = ASTNode("ForStatement", [ASTNode("Identifier", value=p[2]), p[4], p[6], p[8]])

def p_ForStatement_FOR(p):
    "ForStatement : FOR identifier ASSIGN Expression DOWNTO Expression DO Statement"
    p[0] = ASTNode("ForStatement", [ASTNode("Identifier", value=p[2]), p[4], p[6], p[8]])

# Expressões e Operadores
def p_Expression(p):
    "Expression : SimpleExpression RelationalOperator Expression"
    p[0] = ASTNode("Expression", [p[1], ASTNode("Operator", value=p[2]), p[3]])

def p_Expression_SimpleExpression(p):
    "Expression : SimpleExpression"
    p[0] = p[1]

def p_RelationalOperator(p):
    "RelationalOperator : EQUAL"
    p[0] = p[1]

def p_RelationalOperator_GREATER_THAN(p):
    "RelationalOperator : GREATER_THAN"
    p[0] = p[1]

def p_RelationalOperator_LESS_THAN(p):
    "RelationalOperator : LESS_THAN"
    p[0] = p[1]

def p_RelationalOperator_NOT_EQUAL(p):
    "RelationalOperator : NOT_EQUAL"
    p[0] = p[1]

def p_RelationalOperator_GREATER_THAN_EQUAL(p):
    "RelationalOperator : GREATER_THAN_EQUAL"
    p[0] = p[1]

def p_RelationalOperator_LESS_THAN_EQUAL(p):
    "RelationalOperator : LESS_THAN_EQUAL"
    p[0] = p[1]

def p_SimpleExpression(p):
    "SimpleExpression : Sign Term SecondPriorityOperator SimpleExpression"
    p[0] = ASTNode("SimpleExpression", [ASTNode("Sign", value=p[1]), p[2], ASTNode("Operator", value=p[3]), p[4]])

def p_SimpleExpression_List(p):
    "SimpleExpression : Term SecondPriorityOperator SimpleExpression"
    p[0] = ASTNode("SimpleExpression", [p[1], ASTNode("Operator", value=p[2]), p[3]])

def p_SimpleExpression_Term(p):
    "SimpleExpression : Term"
    p[0] = p[1]

def p_SecondPriorityOperator(p):
    "SecondPriorityOperator : '+'"
    p[0] = p[1]

def p_SecondPriorityOperator_MINUS(p):
    "SecondPriorityOperator : '-'"
    p[0] = p[1]

def p_SecondPriorityOperator_OR(p):
    "SecondPriorityOperator : OR"
    p[0] = p[1]

def p_Sign(p):
    "Sign : '+'"
    p[0] = p[1]

def p_Sign_MINUS(p):
    "Sign : '-'"
    p[0] = p[1]

def p_Term(p):
    "Term : Factor FirstPriorityOperator Term"
    p[0] = ASTNode("Term", [p[1], ASTNode("Operator", value=p[2]), p[3]])

def p_Term_Factor(p):
    "Term : Factor"
    p[0] = p[1]

def p_FirstPriorityOperator(p):
    "FirstPriorityOperator : '*'"
    p[0] = p[1]

def p_FirstPriorityOperator_DIVISION(p):
    "FirstPriorityOperator : '/'"
    p[0] = p[1]

def p_FirstPriorityOperator_DIV(p):
    "FirstPriorityOperator : DIV"
    p[0] = p[1]

def p_FirstPriorityOperator_MOD(p):
    "FirstPriorityOperator : MOD"
    p[0] = p[1]

def p_FirstPriorityOperator_AND(p):
    "FirstPriorityOperator : AND"
    p[0] = p[1]

def p_Factor(p):
    "Factor : '(' Expression ')'"
    p[0] = p[2]

def p_Factor_Variable(p):
    "Factor : Variable"
    p[0] = p[1]

def p_Factor_UnsignedConstant(p):
    "Factor : UnsignedConstant"
    p[0] = p[1]

def p_Factor_FunctionDesignator(p):
    "Factor : FunctionDesignator"
    p[0] = p[1]

def p_Factor_NOT(p):
    "Factor : NOT Factor"
    p[0] = ASTNode("Not", [p[2]])

def p_Factor_TRUE(p):
    "Factor : TRUE"
    p[0] = p[1]

def p_Factor_FALSE(p):
    "Factor : FALSE"
    p[0] = p[1]

def p_FunctionDesignator(p):
    "FunctionDesignator : identifier '(' ListArgs ')'"
    p[0] = ASTNode("FunctionCall", [ASTNode("Identifier", value=p[1]), p[3]])

def p_FunctionDesignator_identifier(p):
    "FunctionDesignator : identifier '(' ')'"
    p[0] = ASTNode("FunctionCall", [ASTNode("Identifier", value=p[1]), ASTNode("Args", [])])

# Constantes e Unsigned
def p_UnsignedConstant(p):
    "UnsignedConstant : UnsignedNumber"
    p[0] = ASTNode("UnsignedConstant", value=p[1])

def p_UnsignedConstant_string(p):
    "UnsignedConstant : string"
    p[0] = ASTNode("UnsignedConstant", value=p[1])

def p_UnsignedConstant_char(p):
    "UnsignedConstant : char"
    p[0] = ASTNode("UnsignedConstant", value=p[1])

def p_Constant(p):
    "Constant : num_int"
    p[0] = ASTNode("Constant", value=p[1])

def p_Constant_Sign(p):
    "Constant : Sign num_int"
    p[0] = ASTNode("Constant", [ASTNode("Sign", value=p[1]), ASTNode("Number", value=p[2])])

def p_Constant_char(p):
    "Constant : char"
    p[0] = ASTNode("Constant", value=p[1])

def p_UnsignedNumber(p):
    "UnsignedNumber : num_int"
    p[0] = p[1]

def p_UnsignedNumber_num_real(p):
    "UnsignedNumber : num_real"
    p[0] = p[1]

def p_Variable(p):
    "Variable : identifier"
    p[0] = ASTNode("Variable", value=p[1])

def p_Variable_identifier(p):
    "Variable : identifier '[' ListExpressions ']'"
    p[0] = ASTNode("Variable", [ASTNode("Identifier", value=p[1]), p[3]])

def p_ListExpressions(p):
    "ListExpressions : ListExpressions ',' Expression"
    p[0] = ASTNode("ListExpressions", p[1].children + [p[3]])

def p_ListExpressions_Expression(p):
    "ListExpressions : Expression"
    p[0] = ASTNode("ListExpressions", [p[1]])

def p_error(p):
    print('Erro sintático: ', p)
    parser.success = False

# Constrói o parser
parser = yacc.yacc()

import sys

text = sys.stdin.read()
parser.success = True
result = parser.parse(text)
if parser.success:
    #print('Frase válida!')
    #print("AST Gerada:")
    print(result)
else:
    print('Frase inválida... Corrija e tente novamente!')

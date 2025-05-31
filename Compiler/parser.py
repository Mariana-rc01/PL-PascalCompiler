import ply.yacc as yacc
from Compiler.lex import tokens, literals
from ASTree.astree import ASTNode
from Compiler.semantic import SemanticAnalyzer
from Compiler.codegen import CodeGenerator

# Principal Rule
def p_Program(p):
    "Program : Header Content '.'"
    p[0] = ASTNode("Program", [p[1], p[2]])

# Program Header
def p_Header(p):
    "Header : PROGRAM identifier '(' ListH ')' ';'"
    p[0] = ASTNode("Header", [ASTNode("Identifier", [p[2]]), p[4]])

def p_Header_PROGRAM(p):
    "Header : PROGRAM identifier ';'"
    p[0] = ASTNode("Header", [ASTNode("Identifier", [ASTNode(p[2])])])

def p_ListH(p):
    "ListH : ListH ',' identifier"
    # Adiciona o identificador à lista
    # Aqui assume-se que p[1] já é um nó com a lista de identificadores
    p[0] = ASTNode("IdentifierList", p[1].children + [ASTNode("Identifier", [p[3]])])

def p_ListH_identifier(p):
    "ListH : identifier"
    p[0] = ASTNode("IdentifierList", [ASTNode("Identifier", [p[1]])])

# Program Content
def p_Content(p):
    "Content : Declarations CompoundStatement"
    p[0] = ASTNode("Content", [p[1], p[2]])

# Declarations
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
    #p[0] = ASTNode("Declarations", [])

# Variable Declarations
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
    p[0] = ASTNode("VarElemDeclaration", [p[1], ASTNode("Type", [ASTNode(p[3])])])

def p_ElemVarsDeclaration_array(p):
    "ElemVarsDeclaration : IdentifierList COLON Array"
    p[0] = ASTNode("VarElemDeclaration", [p[1], p[3]])

def p_Array(p):
    "Array : ARRAY '[' Constant '.' '.' Constant ']' OF identifier"
    p[0] =ASTNode("ArrayType", [ASTNode("Bounds", [
                                                   ASTNode("LowBound", [p[3]]),
                                                   ASTNode("HighBound", [p[6]])
                                                  ]),
                                ASTNode("Type", [ASTNode(p[9])])])

def p_IdentifierList(p):
    "IdentifierList : IdentifierList ',' identifier"
    p[0] = ASTNode("IdentifierList", p[1].children + [ASTNode("Identifier", [ASTNode(p[3])])])

def p_IdentifierList_identifier(p):
    "IdentifierList : identifier"
    p[0] = ASTNode("IdentifierList", [ASTNode("Identifier", [ASTNode(p[1])])])

# Procedure Declarations
def p_ProcedureDeclarationPart(p):
    "ProcedureDeclarationPart : PROCEDURE identifier ListParametersDeclaration ';' Content ';'"
    p[0] = ASTNode("ProcedureDeclaration", [ASTNode("Identifier", [p[2]]),
                                             p[3],
                                             p[5]])

# Function Declarations
def p_FunctionDeclarationPart(p):
    "FunctionDeclarationPart : FUNCTION identifier ListParametersDeclaration COLON identifier ';' Content ';'"
    p[0] = ASTNode("FunctionDeclaration", [ASTNode("Identifier", [p[2]]),
                                            p[3],
                                            ASTNode("ReturnType", [p[5]]),
                                            p[7]])

def p_ListParametersDeclaration(p):
    "ListParametersDeclaration : '(' ListOfListParameters ')'"
    p[0] = ASTNode("ListParametersDeclaration", [p[2]])

def p_ListOfListParameters(p):
    "ListOfListParameters : ListOfListParameters ';' ListParameters"
    p[0] = ASTNode("ListOfListParameters", [p[1], p[3]])

def p_ListOfListParameters_VAR_R(p):
    "ListOfListParameters : ListOfListParameters ';' VAR ListParameters"
    p[0] = ASTNode("ListOfListParameters", [p[1], p[4]])

def p_ListOfListParameters_single(p):
    "ListOfListParameters : ListParameters"
    p[0] = p[1]

def p_ListOfListParameters_VAR(p):
    "ListOfListParameters : VAR ListParameters"
    p[0] = p[2]

def p_ListParametersDeclaration_empty(p):
    "ListParametersDeclaration : "
    # p[0] = ASTNode("Parameters", [])

def p_ListParametersDeclaration_Listempty(p):
    "ListParametersDeclaration : '(' ')'"
    # p[0] = ASTNode("Parameters", [])

def p_ListParameters(p):
    "ListParameters : ListParameters ',' ElemParameter"
    p[0] = ASTNode("Parameters", p[1].children + [p[3]])
    #("Debug: ListParameters ->", p[0])

def p_ListParameters_ElemParameter(p):
    "ListParameters : ElemParameter"
    p[0] = ASTNode("Parameters", [p[1]])

def p_ElemParameter(p):
    "ElemParameter : IdentifierList COLON ARRAY OF identifier"
    p[0] = ASTNode("Parameter", [p[1], ASTNode("ArrayType", [ASTNode("Type",  [p[5]])])])

def p_ListParameters_ElemParameter_identifier(p):
    "ElemParameter : IdentifierList COLON identifier"
    p[0] = ASTNode("Parameter", [p[1], ASTNode("Type", [p[3]])])
    #print("Debug: ElemParameter ->", p[0])

# Compound Statement
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
    # p[0] = ASTNode("ListStatementAux", [])

def p_LastStatement(p):
    "LastStatement : Statement"
    p[0] = ASTNode("LastStatement", [p[1]])

def p_LastStatement_empty(p):
    "LastStatement : "
    # p[0] = ASTNode("LastStatement", [])

def p_Statement(p):
    "Statement : SimpleStatement"
    p[0] = ASTNode("Statement", [p[1]])

def p_Statement_StructeredStatement(p):
    "Statement : StructeredStatement"
    p[0] = ASTNode("Statement", [p[1]])

# Simple Statement
def p_SimpleStatement(p):
    "SimpleStatement : AssignmentStatement"
    p[0] = ASTNode("SimpleStatement", [p[1]])

def p_SimpleStatement_ProcedureStatement(p):
    "SimpleStatement : ProcedureStatement"
    p[0] = ASTNode("SimpleStatement", [p[1]])

def p_AssignmentStatement(p):
    "AssignmentStatement : Variable ASSIGN Expression"
    p[0] = ASTNode("Assignment", [p[1], p[3]])

def p_ProcedureStatement(p):
    "ProcedureStatement : identifier '(' ListArgs ')'"
    p[0] = ASTNode("ProcedureCall", [ASTNode("Identifier", [ASTNode(p[1])]), p[3]])

def p_ProcedureStatement_identifier(p):
    "ProcedureStatement : identifier '(' ')'"
    p[0] = ASTNode("ProcedureCall", [ASTNode("Identifier", [ASTNode(p[1])])])

def p_ProcedureStatement_empty(p):
    "ProcedureStatement : identifier"
    p[0] = ASTNode("ProcedureCall", [ASTNode("Identifier", [ASTNode(p[1])])])

def p_ListArgs(p):
    "ListArgs : ListArgs ',' Arg"
    p[0] = ASTNode("ListArgs", p[1].children + [p[3]])

def p_ListArgs_Arg(p):
    "ListArgs : Arg"
    p[0] = ASTNode("ListArgs", [p[1]])

def p_Arg_Expression(p):
    "Arg : Expression"
    p[0] = ASTNode("Arg", [p[1]])

# Structered Statements (Ex.: Compound, Conditional, Repetitive)
def p_StructeredStatement(p):
    "StructeredStatement : CompoundStatement"
    p[0] = ASTNode("StructeredStatement", [p[1]])

def p_StructeredStatement_ConditionalStatement(p):
    "StructeredStatement : ConditionalStatement"
    p[0] = ASTNode("StructeredStatement", [p[1]])

def p_StructeredStatement_RepetitiveStatement(p):
    "StructeredStatement : RepetitiveStatement"
    p[0] = ASTNode("StructeredStatement", [p[1]])

# Condicional
def p_ConditionalStatement(p):
    "ConditionalStatement : IfStatement"
    p[0] = ASTNode("ConditionalStatement", [p[1]])

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
    p[0] = ASTNode("RepetitiveStatement", [p[1]])

def p_RepetitiveStatement_ForStatement(p):
    "RepetitiveStatement : ForStatement"
    p[0] = ASTNode("RepetitiveStatement", [p[1]])

def p_WhileStatement(p):
    "WhileStatement : WHILE Expression DO Statement"
    p[0] = ASTNode("WhileStatement", [p[2], 'Do', p[4]])

def p_ForStatement(p):
    "ForStatement : FOR identifier ASSIGN Expression TO Expression DO Statement"
    p[0] = ASTNode("ForStatement", [ASTNode("Identifier", [ASTNode(p[2])]), 'Assign', p[4], 'To', p[6], 'Do', p[8]])

def p_ForStatement_FOR(p):
    "ForStatement : FOR identifier ASSIGN Expression DOWNTO Expression DO Statement"
    p[0] = ASTNode("ForStatement", [ASTNode("Identifier", [ASTNode(p[2])]), 'Assign', p[4], 'DownTo', p[6], 'Do', p[8]])

# Expressões e Operadores
def p_Expression(p):
    "Expression : SimpleExpression RelationalOperator Expression"
    p[0] = ASTNode("Expression", [p[1], ASTNode("Operator", [p[2]]), p[3]])

def p_Expression_SimpleExpression(p):
    "Expression : SimpleExpression"
    p[0] = ASTNode("Expression", [p[1]])

def p_RelationalOperator(p):
    "RelationalOperator : EQUAL"
    p[0] = ASTNode("RelationalOperator", [p[1]])

def p_RelationalOperator_GREATER_THAN(p):
    "RelationalOperator : GREATER_THAN"
    p[0] = ASTNode("RelationalOperator", [p[1]])

def p_RelationalOperator_LESS_THAN(p):
    "RelationalOperator : LESS_THAN"
    p[0] = ASTNode("RelationalOperator", [p[1]])

def p_RelationalOperator_NOT_EQUAL(p):
    "RelationalOperator : NOT_EQUAL"
    p[0] = ASTNode("RelationalOperator", [p[1]])

def p_RelationalOperator_GREATER_THAN_EQUAL(p):
    "RelationalOperator : GREATER_THAN_EQUAL"
    p[0] = ASTNode("RelationalOperator", [p[1]])

def p_RelationalOperator_LESS_THAN_EQUAL(p):
    "RelationalOperator : LESS_THAN_EQUAL"
    p[0] = ASTNode("RelationalOperator", [p[1]])

def p_SimpleExpression(p):
    "SimpleExpression : Sign Term SecondPriorityOperator SimpleExpression"
    p[0] = ASTNode("SimpleExpression", [ASTNode("Sign", [p[1]]), p[2], ASTNode("Operator", [p[3]]), p[4]])

def p_SimpleExpression_List(p):
    "SimpleExpression : Term SecondPriorityOperator SimpleExpression"
    p[0] = ASTNode("SimpleExpression", [p[1], ASTNode("Operator", [p[2]]), p[3]])

def p_SimpleExpression_Term(p):
    "SimpleExpression : Term"
    p[0] = ASTNode("SimpleExpression", [p[1]])

def p_SecondPriorityOperator(p):
    "SecondPriorityOperator : '+'"
    p[0] = ASTNode("SecondPriorityOperator", [p[1]])

def p_SecondPriorityOperator_MINUS(p):
    "SecondPriorityOperator : '-'"
    p[0] = ASTNode("SecondPriorityOperator", [p[1]])

def p_SecondPriorityOperator_OR(p):
    "SecondPriorityOperator : OR"
    p[0] = ASTNode("SecondPriorityOperator", [p[1]])

def p_Sign(p):
    "Sign : '+'"
    p[0] = p[1]

def p_Sign_MINUS(p):
    "Sign : '-'"
    p[0] = p[1]

def p_Term(p):
    "Term : Factor FirstPriorityOperator Term"
    p[0] = ASTNode("Term", [p[1], ASTNode("Operator", [p[2]]), p[3]])

def p_Term_Factor(p):
    "Term : Factor"
    p[0] = ASTNode("Term", [p[1]])

def p_FirstPriorityOperator(p):
    "FirstPriorityOperator : '*'"
    p[0] = ASTNode("FirstPriorityOperator", [p[1]])

def p_FirstPriorityOperator_DIVISION(p):
    "FirstPriorityOperator : '/'"
    p[0] = ASTNode("FirstPriorityOperator", [p[1]])

def p_FirstPriorityOperator_DIV(p):
    "FirstPriorityOperator : DIV"
    p[0] = ASTNode("FirstPriorityOperator", [p[1]])

def p_FirstPriorityOperator_MOD(p):
    "FirstPriorityOperator : MOD"
    p[0] = ASTNode("FirstPriorityOperator", [p[1]])

def p_FirstPriorityOperator_AND(p):
    "FirstPriorityOperator : AND"
    p[0] = ASTNode("FirstPriorityOperator", [p[1]])

def p_Factor(p):
    "Factor : '(' Expression ')'"
    p[0] = ASTNode("Factor", [p[2]])

def p_Factor_Variable(p):
    "Factor : Variable"
    p[0] = ASTNode("Factor", [p[1]])

def p_Factor_UnsignedConstant(p):
    "Factor : UnsignedConstant"
    p[0] = ASTNode("Factor", [p[1]])

def p_Factor_FunctionDesignator(p):
    "Factor : FunctionDesignator"
    p[0] = ASTNode("Factor", [p[1]])

def p_Factor_NOT(p):
    "Factor : NOT Factor"
    p[0] = ASTNode("Factor", ["Not", p[2]])

def p_Factor_TRUE(p):
    "Factor : TRUE"
    p[0] = ASTNode("Factor", [p[1]])

def p_Factor_FALSE(p):
    "Factor : FALSE"
    p[0] = ASTNode("Factor", [p[1]])

def p_FunctionDesignator(p):
    "FunctionDesignator : identifier '(' ListArgs ')'"
    p[0] = ASTNode("FunctionCall", [ASTNode("Identifier", [ASTNode(p[1])]), p[3]])

def p_FunctionDesignator_identifier(p):
    "FunctionDesignator : identifier '(' ')'"
    p[0] = ASTNode("FunctionCall", [ASTNode("Identifier", [ASTNode(p[1])]), ASTNode("Args", [])])

# Constants and Unsigned
def p_UnsignedConstant(p):
    "UnsignedConstant : UnsignedNumber"
    p[0] = ASTNode("UnsignedConstant", [p[1]])

def p_UnsignedConstant_string(p):
    "UnsignedConstant : string"
    p[0] = ASTNode("UnsignedConstant", [ASTNode("String", [p[1]])])

def p_UnsignedConstant_char(p):
    "UnsignedConstant : char"
    p[0] = ASTNode("UnsignedConstant", [ASTNode("Char", [p[1]])])

def p_Constant(p):
    "Constant : num_int"
    p[0] = ASTNode("Constant", [ASTNode("Num_Int", [p[1]])])

def p_Constant_Sign(p):
    "Constant : Sign num_int"
    p[0] = ASTNode("Constant", [ASTNode("Sign", [p[1]]), ASTNode("Number", [p[2]])])

def p_Constant_char(p):
    "Constant : char"
    p[0] = ASTNode("Constant", [ASTNode(p[1])])

def p_UnsignedNumber(p):
    "UnsignedNumber : num_int"
    p[0] = ASTNode("Num_Int", [p[1]])

def p_UnsignedNumber_num_real(p):
    "UnsignedNumber : num_real"
    p[0] = ASTNode("Num_Real", [p[1]])

def p_Variable(p):
    "Variable : identifier"
    p[0] = ASTNode("Variable", [ASTNode("Identifier", [p[1]])])

def p_Variable_identifier(p):
    "Variable : identifier '[' ListExpressions ']'"
    p[0] = ASTNode("Variable", [ASTNode("Identifier", [ASTNode(p[1])]), p[3]])

def p_ListExpressions(p):
    "ListExpressions : ListExpressions ',' Expression"
    p[0] = ASTNode("ListExpressions", p[1].children + [p[3]])

def p_ListExpressions_Expression(p):
    "ListExpressions : Expression"
    p[0] = ASTNode("ListExpressions", [p[1]])

def p_error(p):
    print('Syntax error: ', p)
    parser.success = False

# Builds the parser
parser = yacc.yacc()

import sys

def parse_input(text):
    parser.success = True
    result = parser.parse(text)
    return result if parser.success else None

if __name__ == '__main__':
    import sys
    text = sys.stdin.read()
    ast = parse_input(text)
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)

    if analyzer.errors:
        print("Semantic analysis errors:")
        for err in analyzer.errors:
            print("-", err)
    else:
        generator = CodeGenerator()
        code = generator.generate(ast)
        print("== Generated code ==")
        print(code)

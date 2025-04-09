# sin.py

import ply.yacc as yacc
from lex import tokens, literals, reserved
from ast_nodes import Program, Header, VarDeclaration, Assignment, BinaryOp, Literal, Variable
# Note que outras classes de AST (como IfStatement, WhileStatement, etc.) podem ser definidas em ast_nodes.py

def p_Program(p):
    "Program : Header Content '.'"
    header = p[1]
    # p[2] retorna uma tupla (declarations, compound_statement)
    declarations, compound_statement = p[2]
    p[0] = Program(header, declarations, compound_statement)
    print(f"Debug: Program -> {p[0]}")

def p_Header(p):
    "Header : PROGRAM identifier '(' ListH ')' ';'"
    p[0] = Header(p[1], p[2], p[4])
    #print(f"Debug: Header -> {p[0]}")

def p_Header_PROGRAM(p):
    "Header : PROGRAM identifier ';'"
    p[0] = Header(p[1], p[2])
    #print(f"Debug: Header_PROGRAM -> {p[0]}")

def p_ListH(p):
    "ListH : ListH ',' identifier"
    p[0] = p[1] + [p[3]]
    #print(f"Debug: ListH -> {p[0]}")

def p_ListH_identifier(p):
    "ListH : identifier"
    p[0] = [p[1]]
    #print(f"Debug: ListH_identifier -> {p[0]}")

def p_Content(p):
    "Content : Declarations CompoundStatement"
    # p[1] deve ser uma lista de declarações; p[2] uma lista de comandos
    p[0] = (p[1], p[2])
    #print(f"Debug: Content -> Declarations: {p[1]}, Statements: {p[2]}")

def p_Declarations(p):
    "Declarations : Declarations VariableDeclarationPart"
    p[0] = p[1] + p[2]
    #print(f"Debug: Declarations -> {p[0]}")

def p_Declarations_empty(p):
    "Declarations : "
    p[0] = []
    #print(f"Debug: Declarations empty -> {p[0]}")

def p_VariableDeclarationPart(p):
    "VariableDeclarationPart : VAR ListVarsDeclaration"
    p[0] = p[2]
    #print(f"Debug: VariableDeclarationPart -> {p[0]}")

def p_ListVarsDeclaration(p):
    "ListVarsDeclaration : ListVarsDeclaration ElemVarsDeclaration ';'"
    p[0] = p[1] + p[2]
    #print(f"Debug: ListVarsDeclaration -> {p[0]}")

def p_ListVarsDeclaration_ElemVarsDeclaration(p):
    "ListVarsDeclaration : ElemVarsDeclaration ';'"
    p[0] = p[1]
    #print(f"Debug: ListVarsDeclaration (elem) -> {p[0]}")

def p_ElemVarsDeclaration(p):
    "ElemVarsDeclaration : IdentifierList COLON identifier"
    # Aqui, p[1] é a lista de identificadores e p[3] o tipo
    # Cria uma declaração de variável para cada identificador
    decls = [VarDeclaration(p[1], p[3])]
    p[0] = decls
    #print(f"Debug: ElemVarsDeclaration -> {p[0]}")

def p_IdentifierList(p):
    "IdentifierList : IdentifierList ',' identifier"
    p[0] = p[1] + [p[3]]
    #print(f"Debug: IdentifierList -> {p[0]}")

def p_IdentifierList_identifier(p):
    "IdentifierList : identifier"
    p[0] = [p[1]]

def p_CompoundStatement(p):
    "CompoundStatement : BEGIN ListStatement END"
    p[0] = p[2]
    #print(f"Debug: CompoundStatement -> {p[0]}")

def p_ListStatement(p):
    "ListStatement : ListStatementAux LastStatement"
    p[0] = p[1] + p[2]
    #print(f"Debug: ListStatement -> {p[0]}")

def p_ListStatementAux(p):
    "ListStatementAux : ListStatementAux Statement ';'"
    p[0] = p[1] + [p[2]]
    #print(f"Debug: ListStatementAux -> {p[0]}")

def p_ListStatementAux_empty(p):
    "ListStatementAux : "
    p[0] = []

def p_LastStatement(p):
    "LastStatement : Statement"
    p[0] = [p[1]]
    #print(f"Debug: LastStatement -> {p[0]}")

def p_LastStatement_empty(p):
    "LastStatement : "
    p[0] = []
    #print(f"Debug: LastStatement empty -> {p[0]}")

def p_Statement(p):
    "Statement : SimpleStatement"
    p[0] = p[1]
    #print(f"Debug: Statement -> {p[0]}")

def p_Statement_StructeredStatement(p):
    "Statement : StructeredStatement"
    p[0] = p[1]
    #print(f"Debug: Statement_StructeredStatement -> {p[0]}")

def p_SimpleStatement(p):
    "SimpleStatement : AssignmentStatement"
    p[0] = p[1]
    #print(f"Debug: SimpleStatement -> {p[0]}")

def p_SimpleStatement_ProcedureStatement(p):
    "SimpleStatement : ProcedureStatement"
    p[0] = p[1]
    #print(f"Debug: SimpleStatement_ProcedureStatement -> {p[0]}")

def p_AssignmentStatement(p):
    "AssignmentStatement : Variable ASSIGN Expression"
    # Cria um nó de atribuição com a variável (nó) e a expressão
    p[0] = Assignment(p[1], p[3])
    #print(f"Debug: AssignmentStatement -> {p[0]}")

def p_ProcedureStatement(p):
    "ProcedureStatement : identifier '(' ListArgs ')'"
    # Para procedimentos, aqui retornamos uma tupla simples
    p[0] = (p[1], p[3])
    #print(f"Debug: ProcedureStatement -> {p[0]}")

def p_ProcedureStatement_identifier(p):
    "ProcedureStatement : identifier '(' ')'"
    p[0] = (p[1], [])
    #print(f"Debug: ProcedureStatement_identifier -> {p[0]}")

def p_ListArgs(p):
    "ListArgs : ListArgs ',' Arg"
    p[0] = p[1] + [p[3]]
    #print(f"Debug: ListArgs -> {p[0]}")

def p_ListArgs_Arg(p):
    "ListArgs : Arg"
    p[0] = [p[1]]
    #print(f"Debug: ListArgs_Arg -> {p[0]}")

def p_Arg_Expression(p):
    "Arg : Expression"
    p[0] = p[1]
    #print(f"Debug: Arg_Expression -> {p[0]}")

def p_StructeredStatement(p):
    "StructeredStatement : CompoundStatement"
    p[0] = p[1]
    #print(f"Debug: StructeredStatement -> {p[0]}")

def p_StructeredStatement_ConditionalStatement(p):
    "StructeredStatement : ConditionalStatement"
    p[0] = p[1]
    #print(f"Debug: StructeredStatement_ConditionalStatement -> {p[0]}")

def p_StructeredStatement_RepetitiveStatement(p):
    "StructeredStatement : RepetitiveStatement"
    p[0] = p[1]
    #print(f"Debug: StructeredStatement_RepetitiveStatement -> {p[0]}")

def p_ConditionalStatement(p):
    "ConditionalStatement : IfStatement"
    p[0] = p[1]
    #print(f"Debug: ConditionalStatement -> {p[0]}")

precedence = (
    ('nonassoc', 'IF'),
    ('right', 'ELSE'),
)

def p_IfStatement(p):
    "IfStatement : IF Expression THEN Statement %prec IF"
    # Aqui, retornamos uma tupla – pode-se criar uma classe IfStatement no futuro
    p[0] = (p[2], p[4])
    #print(f"Debug: IfStatement -> {p[0]}")

def p_IfStatement_ELSE(p):
    "IfStatement : IF Expression THEN Statement ELSE Statement"
    p[0] = (p[2], p[4], p[6])
    #print(f"Debug: IfStatement_ELSE -> {p[0]}")

def p_RepetitiveStatement(p):
    "RepetitiveStatement : WhileStatement"
    p[0] = p[1]
    #print(f"Debug: RepetitiveStatement -> {p[0]}")

def p_RepetitiveStatement_ForStatement(p):
    "RepetitiveStatement : ForStatement"
    p[0] = p[1]
    #print(f"Debug: RepetitiveStatement_ForStatement -> {p[0]}")

def p_WhileStatement(p):
    "WhileStatement : WHILE Expression DO Statement"
    p[0] = (p[2], p[4])
    #print(f"Debug: WhileStatement -> {p[0]}")

def p_ForStatement(p):
    "ForStatement : FOR identifier ASSIGN Expression TO Expression DO Statement"
    p[0] = (p[2], p[4], p[6], p[8])
    #print(f"Debug: ForStatement -> {p[0]}")

def p_ForStatement_FOR(p):
    "ForStatement : FOR identifier ASSIGN Expression DOWNTO Expression DO Statement"
    p[0] = (p[2], p[4], p[6], p[8])
    #print(f"Debug: ForStatement_FOR -> {p[0]}")

def p_Expression(p):
    "Expression : SimpleExpression RelationalOperator Expression"
    p[0] = BinaryOp(p[1], p[2], p[3])
    #print(f"Debug: Expression -> {p[0]}")

def p_Expression_SimpleExpression(p):
    "Expression : SimpleExpression"
    p[0] = p[1]
    #print(f"Debug: Expression_SimpleExpression -> {p[0]}")

def p_RelationalOperator(p):
    "RelationalOperator : EQUAL"
    p[0] = p[1]
    #print(f"Debug: RelationalOperator -> {p[0]}")

def p_RelationalOperator_GREATER_THAN(p):
    "RelationalOperator : GREATER_THAN"
    p[0] = p[1]
    #print(f"Debug: RelationalOperator_GREATER_THAN -> {p[0]}")

def p_RelationalOperator_LESS_THAN(p):
    "RelationalOperator : LESS_THAN"
    p[0] = p[1]
    #print(f"Debug: RelationalOperator_LESS_THAN -> {p[0]}")

def p_RelationalOperator_NOT_EQUAL(p):
    "RelationalOperator : NOT_EQUAL"
    p[0] = p[1]
    #print(f"Debug: RelationalOperator_NOT_EQUAL -> {p[0]}")

def p_RelationalOperator_GREATER_THAN_EQUAL(p):
    "RelationalOperator : GREATER_THAN_EQUAL"
    p[0] = p[1]
    #print(f"Debug: RelationalOperator_GREATER_THAN_EQUAL -> {p[0]}")

def p_RelationalOperator_LESS_THAN_EQUAL(p):
    "RelationalOperator : LESS_THAN_EQUAL"
    p[0] = p[1]
    #print(f"Debug: RelationalOperator_LESS_THAN_EQUAL -> {p[0]}")

def p_SimpleExpression(p):
    "SimpleExpression : Sign Term SecondPriorityOperator SimpleExpression"
    p[0] = BinaryOp(p[1], p[3], p[4])
    # Para expressões como + Term ... o nó Sign (p[1]) pode ser tratado como um Literal ou nó unário.
    #print(f"Debug: SimpleExpression -> {p[0]}")

def p_SimpleExpression_List(p):
    "SimpleExpression : Term SecondPriorityOperator SimpleExpression"
    p[0] = BinaryOp(p[1], p[2], p[3])
    #print(f"Debug: SimpleExpression_List -> {p[0]}")

def p_SimpleExpression_Term(p):
    "SimpleExpression : Term"
    p[0] = p[1]
    #print(f"Debug: SimpleExpression_Term -> {p[0]}")

def p_SecondPriorityOperator(p):
    "SecondPriorityOperator : '+'"
    p[0] = p[1]
    #print(f"Debug: SecondPriorityOperator -> {p[0]}")

def p_SecondPriorityOperator_MINUS(p):
    "SecondPriorityOperator : '-'"
    p[0] = p[1]
    #print(f"Debug: SecondPriorityOperator_MINUS -> {p[0]}")

def p_SecondPriorityOperator_OR(p):
    "SecondPriorityOperator : OR"
    p[0] = p[1]
    #print(f"Debug: SecondPriorityOperator_OR -> {p[0]}")

def p_Sign(p):
    "Sign : '+'"
    # Aqui o sinal é tratado como um Literal
    p[0] = Literal('+', "sign")
    #print(f"Debug: Sign -> {p[0]}")

def p_Sign_MINUS(p):
    "Sign : '-'"
    p[0] = Literal('-', "sign")
    #print(f"Debug: Sign_MINUS -> {p[0]}")

def p_Term(p):
    "Term : Factor FirstPriorityOperator Term"
    p[0] = BinaryOp(p[1], p[2], p[3])
    #print(f"Debug: Term -> {p[0]}")

def p_Term_Factor(p):
    "Term : Factor"
    p[0] = p[1]
    #print(f"Debug: Term_Factor -> {p[0]}")

def p_FirstPriorityOperator(p):
    "FirstPriorityOperator : '*'"
    p[0] = p[1]
    #print(f"Debug: FirstPriorityOperator -> {p[0]}")

def p_FirstPriorityOperator_DIVISION(p):
    "FirstPriorityOperator : '/'"
    p[0] = p[1]
    #print(f"Debug: FirstPriorityOperator_DIVISION -> {p[0]}")

def p_FirstPriorityOperator_DIV(p):
    "FirstPriorityOperator : DIV"
    p[0] = p[1]
    #print(f"Debug: FirstPriorityOperator_DIV -> {p[0]}")

def p_FirstPriorityOperator_MOD(p):
    "FirstPriorityOperator : MOD"
    p[0] = p[1]
    #print(f"Debug: FirstPriorityOperator_MOD -> {p[0]}")

def p_FirstPriorityOperator_AND(p):
    "FirstPriorityOperator : AND"
    p[0] = p[1]
    #print(f"Debug: FirstPriorityOperator_AND -> {p[0]}")

def p_Factor(p):
    "Factor : '(' Expression ')'"
    p[0] = p[2]
    #print(f"Debug: Factor -> {p[0]}")

def p_Factor_Variable(p):
    "Factor : Variable"
    p[0] = p[1]
    #print(f"Debug: Factor_Variable -> {p[0]}")

def p_Factor_UnsignedConstant(p):
    "Factor : UnsignedConstant"
    p[0] = p[1]
    #print(f"Debug: Factor_UnsignedConstant -> {p[0]}")

def p_Factor_FunctionDesignator(p):
    "Factor : FunctionDesignator"
    p[0] = p[1]
    #print(f"Debug: Factor_FunctionDesignator -> {p[0]}")

def p_Factor_NOT(p):
    "Factor : NOT Factor"
    # Aqui, pode-se criar um nó UnOp (operador unário) se desejar
    p[0] = ('NOT', p[2])
    #print(f"Debug: Factor_NOT -> {p[0]}")

def p_FunctionDesignator(p):
    "FunctionDesignator : identifier '(' ListArgs ')'"
    p[0] = (p[1], p[3])
    #print(f"Debug: FunctionDesignator -> {p[0]}")

def p_FunctionDesignator_identifier(p):
    "FunctionDesignator : identifier '(' ')'"
    p[0] = (p[1], [])
    #print(f"Debug: FunctionDesignator_identifier -> {p[0]}")

def p_UnsignedConstant(p):
    "UnsignedConstant : UnsignedNumber"
    p[0] = p[1]
    #print(f"Debug: UnsignedConstant -> {p[0]}")

def p_UnsignedConstant_string(p):
    "UnsignedConstant : string"
    # Cria um literal do tipo string
    p[0] = Literal(p[1], "string")
    #print(f"Debug: UnsignedConstant_string -> {p[0]}")

def p_Constant(p):
    "Constant : UnsignedNumber"
    p[0] = p[1]
    #print(f"Debug: Constant -> {p[0]}")

def p_Constant_Sign(p):
    "Constant : Sign UnsignedNumber"
    p[0] = BinaryOp(p[1], '', p[2])
    #print(f"Debug: Constant_Sign -> {p[0]}")

def p_Constant_string(p):
    "Constant : string"
    p[0] = Literal(p[1], "string")
    #print(f"Debug: Constant_string -> {p[0]}")

def p_UnsignedNumber(p):
    "UnsignedNumber : num_int"
    # Converte para inteiro e cria um literal
    p[0] = Literal(int(p[1]), "integer")
    #print(f"Debug: UnsignedNumber -> {p[0]}")

def p_UnsignedNumber_num_real(p):
    "UnsignedNumber : num_real"
    # Converte para real e cria um literal
    p[0] = Literal(float(p[1]), "real")
    #print(f"Debug: UnsignedNumber_num_real -> {p[0]}")

def p_Variable(p):
    "Variable : identifier"
    # Cria um nó de variável
    p[0] = Variable(p[1])
    #print(f"Debug: Variable -> {p[0]}")

def p_Variable_identifier(p):
    "Variable : identifier '[' ListExpressions ']'"
    # Cria um nó de variável com índices (para arrays, por exemplo)
    p[0] = Variable(p[1], p[3])
    #print(f"Debug: Variable_identifier -> {p[0]}")

def p_ListExpressions(p):
    "ListExpressions : ListExpressions ',' Expression"
    p[0] = p[1] + [p[3]]
    #print(f"Debug: ListExpressions -> {p[0]}")

def p_ListExpressions_Expression(p):
    "ListExpressions : Expression"
    p[0] = [p[1]]
    #print(f"Debug: ListExpressions_Expression -> {p[0]}")

def p_error(p):
    print('Erro sintático: ', p)
    parser.success = False

# Build the parser
parser = yacc.yacc()

if __name__ == '__main__':
    import sys
    text = sys.stdin.read()
    parser.success = True
    result = parser.parse(text)
    if parser.success:
        print('Frase válida!')
        # O result é a raiz da AST; aqui você pode executar a análise semântica
        from semantic_analyzer import SemanticAnalyzer
        analyzer = SemanticAnalyzer()
        analyzer.visit(result)
        if analyzer.errors:
            print("Erros semânticos encontrados:")
            for err in analyzer.errors:
                print(err)
        else:
            print("Análise semântica concluída sem erros!")
    else:
        print('Frase inválida... Corrija e tente novamente!')

# ast_nodes.py

class ASTNode:
    def accept(self, visitor):
        method_name = 'visit_' + self.__class__.__name__
        visitor_method = getattr(visitor, method_name, visitor.generic_visit)
        return visitor_method(self)

class Program(ASTNode):
    def __init__(self, header, declarations, compound_statement):
        self.header = header
        self.declarations = declarations  # lista de declarações (ex.: declarações de variáveis)
        self.compound_statement = compound_statement  # corpo do programa

    def __repr__(self):
        return f"Program({self.header}, {self.declarations}, {self.compound_statement})"

class Header(ASTNode):
    def __init__(self, program_token, identifier, params=None):
        self.program_token = program_token  # ex.: 'PROGRAM'
        self.identifier = identifier
        self.params = params or []  # Parâmetros do programa, se houver

    def __repr__(self):
        return f"Header({self.program_token}, {self.identifier}, {self.params})"

class VarDeclaration(ASTNode):
    def __init__(self, identifier_list, var_type):
        self.identifier_list = identifier_list  # lista de nomes (strings)
        self.var_type = var_type  # ex.: 'integer', 'real', etc.

    def __repr__(self):
        return f"VarDeclaration({self.identifier_list}, {self.var_type})"

class Assignment(ASTNode):
    def __init__(self, variable, expression):
        self.variable = variable  # pode ser apenas o nome (string) ou um nó Variable
        self.expression = expression  # expressão a ser atribuída

    def __repr__(self):
        return f"Assignment({self.variable}, {self.expression})"

class BinaryOp(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator  # ex.: '+', '-', etc.
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.left}, '{self.operator}', {self.right})"

class Literal(ASTNode):
    def __init__(self, value, literal_type):
        self.value = value
        self.literal_type = literal_type  # ex.: 'integer', 'real', 'string'

    def __repr__(self):
        return f"Literal({self.value}, {self.literal_type})"

class Variable(ASTNode):
    def __init__(self, name, indices=None):
        self.name = name
        self.indices = indices or []  # Para vetores ou matrizes

    def __repr__(self):
        return f"Variable({self.name}, {self.indices})"

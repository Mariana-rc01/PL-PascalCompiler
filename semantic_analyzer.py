# semantic_analyzer.py

from ast_nodes import Program, Header, VarDeclaration, Assignment, BinaryOp, Literal, Variable
from visitor import NodeVisitor

class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        # Tabela de símbolos para armazenar informações de variáveis e seus tipos
        self.symbols = {}
        self.errors = []

    def visit_Program(self, node: Program):
        self.visit(node.header)
        for decl in node.declarations:
            self.visit(decl)
        self.visit(node.compound_statement)

    def visit_Header(self, node: Header):
        if node.identifier in self.symbols:
            self.errors.append(f"Erro: Programa '{node.identifier}' já foi declarado.")
        else:
            self.symbols[node.identifier] = {'kind': 'program'}
        for param in node.params:
            if param in self.symbols:
                self.errors.append(f"Erro: Parâmetro '{param}' já declarado.")
            else:
                self.symbols[param] = {'kind': 'parameter'}

    def visit_VarDeclaration(self, node: VarDeclaration):
        for var in node.identifier_list:
            if var in self.symbols:
                self.errors.append(f"Erro: Variável '{var}' já declarada.")
            else:
                self.symbols[var] = {'kind': 'variable', 'type': node.var_type}

    def visit_Assignment(self, node: Assignment):
        # Verifica se a variável foi declarada
        var_name = node.variable.name if isinstance(node.variable, Variable) else node.variable
        if var_name not in self.symbols:
            self.errors.append(f"Erro: Variável '{var_name}' não declarada.")
            var_type = None
        else:
            var_type = self.symbols[var_name].get('type')
        expr_type = self.visit(node.expression)
        if var_type and expr_type and var_type != expr_type:
            self.errors.append(
                f"Erro de tipo: Atribuição incompatível em '{var_name}'. Esperado '{var_type}', obtido '{expr_type}'."
            )
        return var_type

    def visit_BinaryOp(self, node: BinaryOp):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type != right_type:
            self.errors.append(
                f"Erro de tipo: Operação '{node.operator}' com tipos incompatíveis: {left_type} e {right_type}."
            )
            return None
        return left_type

    def visit_Literal(self, node: Literal):
        return node.literal_type

    def visit_Variable(self, node: Variable):
        var_name = node.name
        if var_name not in self.symbols:
            self.errors.append(f"Erro: Variável '{var_name}' não declarada.")
            return None
        return self.symbols[var_name].get('type')

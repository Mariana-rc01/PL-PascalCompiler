from ASTree.astree import ASTNode

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = []
        self.current_scope = {}
        self.errors = []

    def analyze(self, ast_node):
        self.symbol_table.append(self.current_scope)
        self._visit(ast_node)
        return self.errors

    def _visit(self, node):
        method_name = f'_visit_{node.nodetype}'
        if hasattr(self, method_name):
            getattr(self, method_name)(node)
        else:
            for child in node.children:
                if isinstance(child, ASTNode):
                    self._visit(child)

    def _visit_VarElemDeclaration(self, node):
        identifier_list = node.children[0]
        var_type_node = node.children[1]
        var_type = var_type_node.children[0].nodetype

        for identifier_node in identifier_list.children:
            var_name = identifier_node.children[0].nodetype
            if var_name in self.current_scope:
                self.errors.append(f"Variable '{var_name}' already declared.")
            else:
                self.current_scope[var_name] = var_type

    def _visit_Assignment(self, node):
        var_type = self._get_expression_type(node.children[0])
        expr_type = self._get_expression_type(node.children[1])
        if var_type and expr_type and var_type != expr_type:
            self.errors.append(f"Incompatible type: '{var_type}' vs '{expr_type}'.")

    def _visit_ProcedureCall(self, node):
        for arg in node.children[1].children:
            self._get_expression_type(arg)

    def _visit_IfStatement(self, node):
        condition_node = node.children[0]
        condition_type = self._get_expression_type(condition_node)
        if condition_type != 'boolean':
            self.errors.append(f"IF Condition must be boolean, found: '{condition_type}'.")

    def _visit_ForStatement(self, node):
        control_var = node.children[0].value
        if self.current_scope.get(control_var) != 'integer':
            self.errors.append(f"Control variable '{control_var}' must be an integer.")

        start_type = self._get_expression_type(node.children[2])
        end_type = self._get_expression_type(node.children[4])
        if start_type != 'integer' or end_type != 'integer':
            self.errors.append("Boundaries do FOR must be integers.")

    def _get_expression_type(self, node):

        if node.nodetype in ('Arg', 'Expression', 'SimpleExpression', 'Term', 'Factor'):
            if len(node.children) == 1:
                return self._get_expression_type(node.children[0])
            elif node.nodetype == 'SimpleExpression' and len(node.children) == 3:
                print(f"SimpleExpression: {node.children[0].nodetype} {node.children[1]} {node.children[2].nodetype}")
                return self._get_expression_type(
                    ASTNode(nodetype='Operator', value=node.children[1], children=[node.children[0], node.children[2]])
                )

        if node.nodetype == 'Variable':
            identifier_node = node.children[0]
            if isinstance(identifier_node, ASTNode):
                var_name = identifier_node.children[0]
            else:
                var_name = identifier_node


            var_type = self.current_scope.get(var_name, None)
            if var_type is None:
                self.errors.append(f"Variable '{var_name}' is not declared.")
            return var_type

        elif node.nodetype == 'Num_Int':
            return 'integer'

        elif node.nodetype in ('TRUE', 'FALSE'):
            return 'boolean'

        elif node.nodetype == 'String':
            return 'string'

        elif node.nodetype == 'Operator':
            operator = node.value
            left_type = self._get_expression_type(node.children[0])
            right_type = self._get_expression_type(node.children[1]) if len(node.children) > 1 else None

            if operator in ('+', '-', '*', '/'):
                if left_type == 'integer' and right_type == 'integer':
                    return 'integer'
                else:
                    self.errors.append(f"Operação '{operator}' requer inteiros.")
            elif operator in ('>', '<', '==', '!='):
                return 'boolean'

        return None


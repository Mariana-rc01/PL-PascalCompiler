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
        var_type = var_type_node.children[0].nodetype.lower()

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
        then_block = node.children[1]
        else_block = node.children[2] if len(node.children) > 2 else None

        condition_type = self._get_expression_type(condition_node)
        if condition_type != 'boolean':
            self.errors.append(f"IF Condition must be boolean, found: '{condition_type}'.")

        if isinstance(then_block, ASTNode):
            self._visit(then_block)

        if else_block and isinstance(else_block, ASTNode):
            self._visit(else_block)

    def _visit_block(self, block):
        if isinstance(block, list):
            for stmt in block:
                if isinstance(stmt, ASTNode):
                    self._visit(stmt)
        elif isinstance(block, ASTNode):
            self._visit(block)

    def _visit_ForStatement(self, node):
        control_var_node = node.children[0].children[0]
        control_var_name = control_var_node.nodetype

        declared_type = self.current_scope.get(control_var_name)
        if declared_type is None:
            self.errors.append(f"Control variable '{control_var_name}' is not declared.")
        elif declared_type != 'integer':
            self.errors.append(f"Control variable '{control_var_name}' must be an integer.")

        start_expr = node.children[2]
        direction = node.children[3]  # TO ou DOWNTO
        end_expr = node.children[4]
        # do = node.children[5]
        loop_body = node.children[6]

        start_value = self._evaluate_constant(start_expr)
        end_value = self._evaluate_constant(end_expr)

        if start_value is not None and end_value is not None:
            if direction == 'TO' and start_value > end_value:
                self.errors.append("FOR loop will never execute: start > end with 'TO'.")
            elif direction == 'DOWNTO' and start_value < end_value:
                self.errors.append("FOR loop will never execute: start < end with 'DOWNTO'.")

        self._visit(loop_body)

    def _visit_WhileStatement(self, node):
        # node.children = [condição, corpo]
        condition_node = node.children[0]
        body_node = node.children[2]

        condition_type = self._get_expression_type(condition_node)
        if condition_type != 'boolean':
            self.errors.append(f"WHILE condition must be boolean, found: '{condition_type}'.")

        self._visit(body_node)

    def _evaluate_constant(self, node):
        if node.nodetype == 'Num_Int':
            return int(node.value)
        return None

    def _get_expression_type(self, node):

        if node in ('true', 'false'):
            return 'boolean'

        if node.nodetype == 'Expression' and len(node.children) == 3:
            left = node.children[0]
            operator_node = node.children[1]
            right = node.children[2]

            if operator_node.nodetype == 'Operator' and operator_node.children:
                inner_op_node = operator_node.children[0]
                if inner_op_node.nodetype == 'RelationalOperator':
                    left_type = self._get_expression_type(left)
                    right_type = self._get_expression_type(right)

                    if left_type == 'integer' and right_type == 'integer':
                        return 'boolean'
                    else:
                        self.errors.append("Relational operators require integer operands.")
                        return None

        if node.nodetype == 'Factor':
            print(f"Factor: {node}")
            if len(node.children) == 1:
                return self._get_expression_type(node.children[0])
            elif any(child.nodetype == 'Expression' for child in node.children):
                for child in node.children:
                    if child.nodetype == 'Expression':
                        return self._get_expression_type(child)


        if node.nodetype in ('Arg', 'SimpleExpression', 'Expression', 'Term', 'Factor', 'UnsignedConstant'):
            if len(node.children) == 1:
                return self._get_expression_type(node.children[0])
            elif node.nodetype == 'SimpleExpression' and len(node.children) == 3:
                return self._get_expression_type(
                    ASTNode(nodetype='Operator', value=node.children[1], children=[node.children[0], node.children[2]])
                )

        if node.nodetype == 'Variable':
            identifier_node = node.children[0]

            if isinstance(identifier_node, ASTNode) and identifier_node.nodetype == 'Identifier':
                var_name = identifier_node.children[0]
            elif isinstance(identifier_node, str):
                var_name = identifier_node
            else:
                self.errors.append(f"Unexpected structure in Variable node: {identifier_node}")
                return None

            var_type = self.current_scope.get(var_name)
            if var_type is None:
                self.errors.append(f"Variable '{var_name}' is not declared.")
            return var_type.lower() if var_type else None

        elif node.nodetype == 'Num_Int':
            return 'integer'
        elif node.nodetype == 'String':
            return 'string'

        elif node.nodetype == 'Operator':
            operator = node.value
            print(f"Operator: {operator}")
            left_type = self._get_expression_type(node.children[0])
            right_type = self._get_expression_type(node.children[1]) if len(node.children) > 1 else None

            if operator in ('+', '-', '*', '/', 'div', 'mod'):
                if left_type == 'integer' and right_type == 'integer':
                    return 'integer'
                else:
                    self.errors.append(f"Operation '{operator}' requires integer operands.")
            elif operator in ('=', '<>', '<', '>', '<=', '>='):
                if left_type == right_type:
                    return 'boolean'
                else:
                    self.errors.append(f"Comparison '{operator}' requires matching operand types.")
            elif operator in ('and', 'or'):
                if left_type == 'boolean' and right_type == 'boolean':
                    return 'boolean'
                else:
                    self.errors.append(f"Logical operator '{operator}' requires boolean operands.")
            elif operator == 'not':
                if left_type == 'boolean':
                    return 'boolean'
                else:
                    self.errors.append("Operator 'not' requires a boolean operand.")


        return None


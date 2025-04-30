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

    def _visit_FunctionDeclaration(self, node):
        func_name = node.children[0].children[0]
        params_node = node.children[1]
        return_type_node = node.children[2].children[0]
        body_node = node.children[3]

        if func_name in self.symbol_table[0]:
            self.errors.append(f"Function '{func_name}' already declared.")
            return

        local_scope = {}
        self.symbol_table.append(local_scope)
        self.current_scope = local_scope

        param_list = self._process_parameters(params_node)
        return_type = return_type_node.lower()

        self.symbol_table[0][func_name] = {
            'type': 'function',
            'params': param_list,
            'return_type': return_type
        }

        for param_name, param_type in param_list:
            self._declare_parameter(param_name, param_type)

        self.current_scope[func_name] = return_type

        self._visit(body_node)

        self.symbol_table.pop()
        self.current_scope = self.symbol_table[-1]

    def _visit_ProcedureDeclaration(self, node):
        proc_name = node.children[0].children[0]
        params_node = node.children[1]
        body_node = node.children[2]

        if proc_name in self.symbol_table[0]:
            self.errors.append(f"Procedure '{proc_name}' already declared.")
            return

        local_scope = {}
        self.symbol_table.append(local_scope)
        self.current_scope = local_scope

        param_list = self._process_parameters(params_node)

        self.symbol_table[0][proc_name] = {
            'type': 'procedure',
            'params': param_list
        }

        for param_name, param_type in param_list:
            self._declare_parameter(param_name, param_type)

        self._visit(body_node)

        self.symbol_table.pop()
        self.current_scope = self.symbol_table[-1]

    def _visit_VarElemDeclaration(self, node):
        identifier_list = node.children[0]
        var_type_node = node.children[1]

        if var_type_node.nodetype == 'ArrayType':
            index_range_node = var_type_node.children[0]
            low_node = index_range_node.children[0]
            high_node = index_range_node.children[1]

            low_value, low_type = self._evaluate_constant(low_node)
            high_value, high_type = self._evaluate_constant(high_node)

            if low_type != high_type:
                self.errors.append(f"Array bounds must have the same type: found '{low_type}' and '{high_type}'.")

            if low_value is None or high_value is None:
                self.errors.append("Array bounds must be constant expressions.")

            base_type_node = var_type_node.children[1]
            base_type = base_type_node.children[0].nodetype.lower()

            for identifier_node in identifier_list.children:
                var_name = str(identifier_node.children[0]).strip()
                if var_name in self.current_scope:
                    self.errors.append(f"Variable '{var_name}' already declared.")
                else:
                    self.current_scope[var_name] = {
                        'type': 'array',
                        'element_type': base_type,
                        'LowBound': low_value,
                        'HighBound': high_value
                    }
        else:
            var_type = var_type_node.children[0].nodetype.lower()
            for identifier_node in identifier_list.children:
                var_name = identifier_node.children[0].nodetype
                if var_name in self.current_scope:
                    self.errors.append(f"Variable '{var_name}' already declared.")
                else:
                    if var_type == 'string':
                        self.current_scope[var_name] = {
                            'type': 'array',
                            'element_type': 'char',
                            'LowBound': 0,
                            'HighBound': 255
                        }
                    else: self.current_scope[var_name] = var_type

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

        if start_expr.nodetype == 'Num_Int':
            start_value = int(start_expr.value)
        else: start_value = None
        if end_expr.nodetype == 'Num_Int':
            end_value = int(end_expr.value)
        else: end_value = None

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
        if node.children[0].nodetype == 'Constant':
            constant = node.children[0]

            # Constant -> Num_Int
            if len(constant.children) == 1 and constant.children[0].nodetype == 'Num_Int':
                return int(constant.children[0].children[0]), 'integer'

            # Constant -> Sign Num_Int
            elif len(constant.children) == 2 and constant.children[0].nodetype == 'Sign' and constant.children[1].nodetype == 'Number':
                sign = constant.children[0].children[0]
                number = int(constant.children[1].children[0])
                return (-number if sign == '-' else number), 'integer'

            # Constant -> char
            elif len(constant.children) == 1 and constant.children[0].nodetype == 'char':
                return constant.children[0].children[0], 'char'

        return None, None

    def _get_expression_type(self, node):
        if isinstance(node, str) and node in ('true', 'false'):
            return 'boolean'

        if isinstance(node, str):
            return 'char'

        if node.nodetype in ('Num_Int',):
            return 'integer'
        if node.nodetype == 'String':
            return 'string'
        if node.nodetype == 'Boolean':
            return 'boolean'

        if node.nodetype == 'Variable':
            identifier_node = node.children[0]
            indices_node = node.children[1] if len(node.children) > 1 else None

            if isinstance(identifier_node, ASTNode) and identifier_node.nodetype == 'Identifier':
                var_name = str(identifier_node.children[0]).strip()
                var_info = self.current_scope.get(var_name)

                if isinstance(var_info, dict) and var_info.get('type') == 'array':
                    if indices_node is None:
                        if var_info.get('element_type') == 'char':
                            return 'string'
                        self.errors.append(f"Array '{var_name}' requires an index.")
                        return None
                    if indices_node.nodetype != 'ListExpressions':
                        self.errors.append(f"Invalid index expression for array '{var_name}'.")
                        return None

                    if len(indices_node.children) != 1:
                        self.errors.append(f"Array '{var_name}' expects one index, got {len(indices_node.children)}.")
                        return None

                    index_expr = indices_node.children[0]
                    index_type = self._get_expression_type(index_expr)
                    if index_type != 'integer' and index_type != 'char':
                        self.errors.append(f"Array index for '{var_name}' must be integer, found: '{index_type}'.")
                        return None

                    return var_info.get('element_type')

                if var_info is None:
                    self.errors.append(f"Variable '{var_name}' is not declared.")
                    return None

                return var_info.lower() if isinstance(var_info, str) else None

        if node.nodetype in ('Expression', 'SimpleExpression', 'Term', 'Factor') and len(node.children) == 3:
            left = node.children[0]
            operator = node.children[1]
            right = node.children[2]

            if isinstance(operator, ASTNode) and operator.nodetype == 'Operator' and operator.children:
                operator_node = operator.children[0]
                operator_value = operator_node.children[0] if operator_node.children else None

                left_type = self._get_expression_type(left)
                right_type = self._get_expression_type(right)

                if operator_value in ('+', '-', '*', '/', 'div', 'mod'):
                    if left_type == 'integer' and right_type == 'integer':
                        return 'integer'
                    self.errors.append(f"Operation '{operator_value}' requires integer operands.")
                    return None
                elif operator_value in ('=', '<>', '<', '>', '<=', '>='):
                    if left_type == right_type:
                        return 'boolean'
                    self.errors.append(f"Comparison '{operator_value}' requires matching operand types.")
                    return None
                elif operator_value in ('and', 'or'):
                    if left_type == 'boolean' and right_type == 'boolean':
                        return 'boolean'
                    self.errors.append(f"Logical operator '{operator_value}' requires boolean operands.")
                    return None

        if node.nodetype == 'Factor' and len(node.children) == 2:
            if node.children[0].nodetype == 'Not':
                operand_type = self._get_expression_type(node.children[1])
                if operand_type == 'boolean':
                    return 'boolean'
                self.errors.append("Operator 'not' requires a boolean operand.")
                return None

        if len(node.children) == 1:
            return self._get_expression_type(node.children[0])

        # Fallback
        return None

    def _process_parameters(self, params_node):
        params = []
        if not isinstance(params_node, ASTNode):
            return params

        list_params = params_node.children[0] if params_node.children else None
        if not isinstance(list_params, ASTNode):
            return params

        def process_parameter_group(param_group):
            if param_group.nodetype == "Parameters":
                for param in param_group.children:
                    id_list = param.children[0].children
                    type_node = param.children[1]
                    param_type = self._parse_type_node(type_node)
                    for id_node in id_list:
                        param_name = str(id_node.children[0]).strip()
                        params.append((param_name, param_type))
            elif param_group.nodetype == "Parameter":
                id_list = param_group.children[0].children
                type_node = param_group.children[1]
                param_type = self._parse_type_node(type_node)
                for id_node in id_list:
                    param_name = str(id_node.children[0]).strip()
                    params.append((param_name, param_type))

        for child in list_params.children:
            if isinstance(child, ASTNode):
                process_parameter_group(child)

        return params

    def _parse_type_node(self, type_node):
        if not isinstance(type_node, ASTNode) or not type_node.children:
            self.errors.append("Invalid type node in parameter declaration.")
            return None
        if type_node.nodetype == "ArrayType":
            if type_node.children and len(type_node.children) >= 2:
                base_type_node = type_node.children[1]
                if base_type_node.children:
                    base_type = base_type_node.children[0].nodetype.lower()
                    return {'type': 'array',
                            'element_type': base_type}
            self.errors.append("Malformed array type.")
            return None

        base_child = type_node.children[0]
        if hasattr(base_child, 'value'):
            base_type = base_child.value.lower()
        else:
            base_type = base_child.lower()

        if base_type == "string":
            return {'type': 'array',
                    'element_type': 'char',
                    'LowBound': 0,
                    'HighBound': 255}
        return base_type

    def _declare_parameter(self, name, param_type):
        if name in self.current_scope:
            self.errors.append(f"Parameter '{name}' already declared.")
            return
        self.current_scope[name] = param_type



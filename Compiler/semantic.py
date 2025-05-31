from ASTree.astree import ASTNode

class SemanticAnalyzer:
    def __init__(self):
        # Initialize symbol table, current scope, and error list
        self.symbol_table = []
        self.current_scope = {}
        self.errors = []

    def analyze(self, ast_node):
        self.symbol_table = [{}]
        self.current_scope = self.symbol_table[0]
        self.errors = []
        self._initialize_builtins()

        if ast_node.nodetype != 'Program':
            self.errors.append("Root node must be of type 'Program'.")
        else:
            self._visit(ast_node)

        return self.errors

    def _initialize_builtins(self):
        self.symbol_table[0].update({
            'writeln': {
                'type': 'procedure',
                'variadic': True
            },
            'readln': {
                'type': 'procedure',
                'variadic': True
            },
            'write': {
                'type': 'procedure',
                'variadic': True
            }
        })

    def _visit(self, node):
        # Dynamically dispatch to a specific visit method based on node type
        method_name = f'_visit_{node.nodetype}'
        if hasattr(self, method_name):
            getattr(self, method_name)(node)
        else:
            # If no specific method, visit child nodes recursively
            for child in node.children:
                if isinstance(child, ASTNode):
                    self._visit(child)

    def _visit_FunctionDeclaration(self, node):
        # Extract function name, parameters, return type, and body
        func_name = node.children[0].children[0]
        params_node = node.children[1]
        return_type_node = node.children[2].children[0]
        body_node = node.children[3]

        # Check for re-declaration
        if func_name in self.symbol_table[0]:
            self.errors.append(f"Function '{func_name}' already declared.")
            return

        # Create new local scope for the function
        local_scope = {}
        self.symbol_table.append(local_scope)
        self.current_scope = local_scope

        # Process parameters and add function to global scope
        param_list = self._process_parameters(params_node)
        return_type = return_type_node.lower()
        self.symbol_table[0][func_name] = {
            'type': 'function',
            'params': param_list,
            'return_type': return_type
        }

        # Declare each parameter in the local scope
        for param_name, param_type in param_list:
            self._declare_parameter(param_name, param_type)

        self.current_scope[func_name] = return_type

        # Analyze the function body
        self._visit(body_node)

        # Restore previous scope
        self.symbol_table.pop()
        self.current_scope = self.symbol_table[-1]

    def normalize_identifier(name):
        return name.lower()

    def _visit_Program(self, node):
        declarations = node.children[1] if len(node.children) > 1 else None
        subprograms  = node.children[2] if len(node.children) > 2 else None
        main_block   = node.children[3] if len(node.children) > 3 else None

        if declarations:
            self._visit(declarations)

        if subprograms:
            self._visit(subprograms)

        if main_block:
            self._visit(main_block)

    def _visit_FunctionCall(self, node):
        func_name = str(node.children[0].children[0]).strip()
        args_node = node.children[1] if len(node.children) > 1 else None
        received_args = args_node.children if args_node else []

        func_info = self.symbol_table[0].get(func_name)
        if func_info is None:
            self.errors.append(f"Function '{func_name}' not declared.")
            return

        expected_params = func_info.get('params', [])
        if len(received_args) != len(expected_params):
            self.errors.append(
                f"Function '{func_name}' expects {len(expected_params)} argument(s), "
                f"but got {len(received_args)}."
            )
            return

        for i, (arg_node, (expected_name, expected_type)) in enumerate(zip(received_args, expected_params)):
            arg_type = self._get_expression_type(arg_node)

            if isinstance(expected_type, dict) and expected_type.get('type') == 'array' and expected_type.get('element_type') == 'char':
                expected_type_str = 'string'
            else:
                expected_type_str = expected_type

            if arg_type == 'string' and expected_type_str == 'string':
                continue

            if arg_type != expected_type_str:
                self.errors.append(
                    f"Type mismatch for argument {i + 1} in call to '{func_name}': "
                    f"expected '{expected_type_str}', got '{arg_type}'."
                )


    def _visit_ProcedureDeclaration(self, node):
        # Similar to function, but without return type
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
            if base_type_node.children and base_type_node.children[0] is not None:
                base_type_child = base_type_node.children[0]
                if base_type_child is not None:
                    base_type = (base_type_child.value.lower() if hasattr(base_type_child, 'value') and base_type_child.value is not None 
                                else (base_type_child.nodetype.lower() if hasattr(base_type_child, 'nodetype') else None))
                    if base_type is None:
                        self.errors.append("Invalid base type in array declaration.")
                        return
                else:
                    self.errors.append("Invalid base type in array declaration.")
                    return
            else:
                self.errors.append("Invalid base type in array declaration.")
                return

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
            if var_type_node and var_type_node.children and var_type_node.children[0] is not None:
                type_node = var_type_node.children[0]
                if hasattr(type_node, 'value') and type_node.value is not None:
                    var_type = type_node.value.lower()
                elif hasattr(type_node, 'nodetype') and type_node.nodetype is not None:
                    var_type = type_node.nodetype.lower()
                else:
                    self.errors.append("Unrecognized type node in variable declaration.")
                    return
            else:
                self.errors.append("Invalid or missing type in variable declaration.")
                return

            for identifier_node in identifier_list.children:
                var_name = str(identifier_node.children[0]).strip()
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
                    else:
                        self.current_scope[var_name] = var_type

    def _visit_Assignment(self, node):
        var_type = self._get_expression_type(node.children[0])
        expr_type = self._get_expression_type(node.children[1])

        if var_type and expr_type:
            if var_type == expr_type:
                return
            elif var_type == 'real' and expr_type == 'integer':
                return
            else:
                self.errors.append(f"Incompatible type: '{var_type}' vs '{expr_type}'.")

    def _visit_ProcedureCall(self, node):
        proc_name = str(node.children[0].children[0]).strip()
        args_node = node.children[1] if len(node.children) > 1 else None
        received_args = args_node.children if args_node else []

        proc_info = self.symbol_table[0].get(proc_name)

        if proc_name.lower() == 'readln' or proc_name.lower() == "writeln" or proc_name.lower() == "write" or proc_name.lower() == "read":
            proc_info = self.symbol_table[0].get(proc_name.lower())

        if proc_info is None:
            self.errors.append(f"Procedure or function '{proc_name}' not declared.")
            return

        if proc_info.get('variadic'):
            if proc_name.lower() == 'readln':
                for i, arg_node in enumerate(received_args):
                    expr_node = arg_node.children[0].children[0].children[0].children[0].children[0] if arg_node.nodetype == 'Arg' else arg_node
                    if expr_node.nodetype != 'Variable':
                        self.errors.append(f"Argument {i+1} in 'readln' must be a variable.")
                    else:
                        var_type = self._get_expression_type(expr_node)
                        if var_type is None:
                            self.errors.append(f"Undeclared variable in argument {i+1} of 'readln'.")
            elif proc_name.lower() == 'writeln':
                for i, arg_node in enumerate(received_args):
                    arg_type = self._get_expression_type(arg_node)
                    if arg_type is None:
                        self.errors.append(f"Unrecognized type in argument {i+1} of 'writeln'.")
            return

        expected_params = proc_info.get('params', [])
        if len(received_args) != len(expected_params):
            self.errors.append(
                f"Procedure/function '{proc_name}' expects {len(expected_params)} argument(s), "
                f"but got {len(received_args)}."
            )
            return

        for i, (arg_node, (expected_name, expected_type)) in enumerate(zip(received_args, expected_params)):
            arg_type = self._get_expression_type(arg_node)

            if isinstance(expected_type, dict):
                expected_type_str = expected_type.get('element_type', 'unknown')
            else:
                expected_type_str = expected_type


            if arg_type != expected_type_str:
                self.errors.append(
                    f"Type mismatch for argument {i + 1} in call to '{proc_name}': "
                    f"expected '{expected_type_str}', got '{arg_type}'."
                )

    def _visit_IfStatement(self, node):
        # Validate that condition is boolean
        condition_node = node.children[0]
        then_block = node.children[1]
        else_block = node.children[2] if len(node.children) > 2 else None

        condition_type = self._get_expression_type(condition_node)
        if condition_type != 'boolean':
            self.errors.append(f"IF Condition must be boolean, found: '{condition_type}'.")

        self._visit(then_block)
        if else_block:
            self._visit(else_block)

    def _visit_block(self, block):
        # Visit a sequence of statements
        if isinstance(block, list):
            for stmt in block:
                if isinstance(stmt, ASTNode):
                    self._visit(stmt)
        elif isinstance(block, ASTNode):
            self._visit(block)

    def _visit_ForStatement(self, node):
        # Analyze for-loop and validate loop bounds
        control_var_node = node.children[0].children[0]
        control_var_name = control_var_node.nodetype

        declared_type = self.current_scope.get(control_var_name)
        if declared_type is None:
            self.errors.append(f"Control variable '{control_var_name}' is not declared.")
        elif declared_type != 'integer':
            self.errors.append(f"Control variable '{control_var_name}' must be an integer.")

        start_expr = node.children[2]
        direction = node.children[3]  # TO or DOWNTO
        end_expr = node.children[4]
        loop_body = node.children[6]

        # Check if loop makes logical sense with constant bounds
        start_value = int(start_expr.value) if start_expr.nodetype == 'Num_Int' else None
        end_value = int(end_expr.value) if end_expr.nodetype == 'Num_Int' else None

        if start_value is not None and end_value is not None:
            if direction == 'TO' and start_value > end_value:
                self.errors.append("FOR loop will never execute: start > end with 'TO'.")
            elif direction == 'DOWNTO' and start_value < end_value:
                self.errors.append("FOR loop will never execute: start < end with 'DOWNTO'.")

        self._visit(loop_body)

    def _visit_WhileStatement(self, node):
        # Ensure condition is boolean in while loop
        condition_node = node.children[0]
        body_node = node.children[2]

        condition_type = self._get_expression_type(condition_node)
        if condition_type != 'boolean':
            self.errors.append(f"WHILE condition must be boolean, found: '{condition_type}'.")

        self._visit(body_node)

    def _evaluate_constant(self, node):
        # Tries to evaluate a constant value and determine its type
        if node.children[0].nodetype == 'Constant':
            constant = node.children[0]
            if len(constant.children) == 1 and constant.children[0].nodetype == 'Num_Int':
                return int(constant.children[0].children[0]), 'integer'
            elif len(constant.children) == 2 and constant.children[0].nodetype == 'Sign':
                sign = constant.children[0].children[0]
                number = int(constant.children[1].children[0])
                return (-number if sign == '-' else number), 'integer'
            elif len(constant.children) == 1 and constant.children[0].nodetype == 'char':
                return constant.children[0].children[0], 'char'
        return None, None

    def _get_expression_type(self, node):
        # Determine the resulting type of an expression
        if isinstance(node, str):
            if node in ('true', 'false'):
                return 'boolean'
            return 'char'

        if node.nodetype == 'Num_Int':
            return 'integer'
        if node.nodetype == 'Num_Real':
            return 'real'
        if node.nodetype == 'String':
            return 'string'
        if node.nodetype == 'Boolean':
            return 'boolean'

        # Variable reference and indexing
        if node.nodetype == 'Variable':
            identifier_node = node.children[0]
            indices_node = node.children[1] if len(node.children) > 1 else None

            if identifier_node.nodetype == 'Identifier':
                var_name = str(identifier_node.children[0]).strip()
                var_info = self.current_scope.get(var_name)

                if var_info is None:
                    self.errors.append(f"Variable '{var_name}' is not declared.")
                    return None

                if isinstance(var_info, dict) and var_info.get('type') == 'array':
                    if indices_node is None:
                        if var_info.get('element_type') == 'char':
                            return 'string'
                        elif var_info.get('element_type') == 'integer':
                            return 'integer'
                        else:
                            return None

                    if indices_node.nodetype != 'ListExpressions':
                        self.errors.append(f"Invalid index expression for array '{var_name}'.")
                        return None

                    if len(indices_node.children) != 1:
                        self.errors.append(f"Array '{var_name}' expects one index.")
                        return None

                    index_type = self._get_expression_type(indices_node.children[0])
                    if index_type not in ('integer', 'char'):
                        self.errors.append(f"Index for array '{var_name}' must be integer or char.")
                        return None

                    return var_info.get('element_type')

                if isinstance(var_info, str):
                    return var_info.lower()

                return None

        if node.nodetype == 'FunctionCall':
            self._visit_FunctionCall(node)
            func_name = str(node.children[0].children[0]).strip()
            func_info = self.symbol_table[0].get(func_name)
            return func_info.get('return_type') if func_info else None

        # Binary expressions
        if node.nodetype in ('Expression', 'SimpleExpression', 'Term', 'Factor') and len(node.children) == 3:
            left_type = self._get_expression_type(node.children[0])
            operator = node.children[1].children[0].children[0]
            right_type = self._get_expression_type(node.children[2])

            if operator in ('+', '-', '*', '/'):
                if operator == '/':
                    if left_type in ('integer', 'real') and right_type in ('integer', 'real'):
                        return 'real'
                if left_type == right_type and left_type in ('integer', 'real'):
                    return left_type
                elif {left_type, right_type} <= {'integer', 'real'}:
                    return 'real'
                self.errors.append(f"Arithmetic operator '{operator}' requires operands of type integer or real.")
                return None

            if operator in ('div', 'mod'):
                if left_type == right_type == 'integer':
                    return 'integer'
                self.errors.append(f"Operator '{operator}' requires integer operands.")
                return None

            if operator in ('=', '<>', '<', '>', '<=', '>='):
                numeric_types = {'integer', 'real'}
                if left_type == right_type:
                    return 'boolean'
                elif left_type in numeric_types and right_type in numeric_types:
                    return 'boolean'
                else:
                    self.errors.append(f"Comparison '{operator}' requires operands of compatible numeric types or the same type.")
                    return None

            if operator in ('and', 'or'):
                if left_type == right_type == 'boolean':
                    return 'boolean'
                self.errors.append(f"Logical operator '{operator}' requires boolean operands.")
                return None


        # Unary expression (e.g., not)
        if node.nodetype == 'Factor' and len(node.children) == 2:
            if node.children[0].nodetype == 'Not':
                operand_type = self._get_expression_type(node.children[1])
                if operand_type == 'boolean':
                    return 'boolean'
                self.errors.append("Operator 'not' requires a boolean operand.")
                return None

        # Recursively resolve single-child expressions
        if len(node.children) == 1:
            return self._get_expression_type(node.children[0])

        return None


    def _process_parameters(self, params_node):
        # Extract and format parameters into a list of tuples
        params = []
        if not isinstance(params_node, ASTNode):
            return params

        list_params = params_node.children[0] if params_node.children else None
        if not isinstance(list_params, ASTNode):
            return params

        def process_parameter_group(param_group):
            if param_group.nodetype in ["Parameters", "Parameter"]:
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
        # Convert AST type node to internal type representation
        if not isinstance(type_node, ASTNode) or not type_node.children:
            self.errors.append("Invalid type node in parameter declaration.")
            return None
        if type_node.nodetype == "ArrayType":
            if len(type_node.children) == 2 and type_node.children[0].nodetype == "Bounds":
                type_child = type_node.children[1]
                base_type_node = type_child.children[0]
                base_type = base_type_node.value
                return {'type': 'array', 'element_type': base_type}
            # array of type (array aberto)
            elif len(type_node.children) == 1 and type_node.children[0].nodetype == "Type":
                base_type_node = type_node.children[0].children[0]
                return {'type': 'array', 'element_type': base_type_node}
            self.errors.append("Malformed array type.")
            return None

        base_child = type_node.children[0]
        base_type = base_child.value.lower() if hasattr(base_child, 'value') else base_child.lower()
        if base_type == "string":
            return {'type': 'array', 'element_type': 'char', 'LowBound': 0, 'HighBound': 255}
        return base_type

    def _declare_parameter(self, name, param_type):
        # Add a parameter to the current scope
        if name in self.current_scope:
            self.errors.append(f"Parameter '{name}' already declared.")
        else:
            self.current_scope[name] = param_type

from ASTree.astree import ASTNode

class CodeGenerator:
    def __init__(self):
        self.output = []
        self.var_counter = 0 # Track the address to use for the next variable
        self.var_map = {} # Map each variable to its memory address
        self.var_type_map = {} # Map each variable to its type
        self.array_lower_bound_map = {} # Map the lower bound index of each array
        self.label_count = 0
        self.loop_label_count = 0
        self.current_identation = 2
        self.output_functions = []
        self.function_map = {}  # Map the return type of each function
        self.is_function_scope = False  # Indicates if we are inside a function
        self.function_var_map = {}  # Map local variables of each function
        self.function_var_counter = 0  # Address of local variables in the function
        self.function_var_type_map = {}  # Map the type of each local variable in the function
        self.debug_mode = False  # Flag to enable debug mode

    def print_debug_info(self):
        print("=== Debug Information ===")
        print("Variable Map:", self.var_map)
        print("Variable Type Map:", self.var_type_map)
        print("Array Lower Bound Map:", self.array_lower_bound_map)
        print("Function Map:", self.function_map)
        print("Function Variable Map:", self.function_var_map)
        print("Function Variable Type Map:", self.function_var_type_map)
        print("==========================")

    def generate(self, ast_root, debug_mode=False):
        if debug_mode:
            self.debug_mode = True
        self.output.append("START\n")
        self._visit(ast_root)
        self.output.append("\nSTOP")
        return "\n".join(self.output + self.output_functions)

    def _get_variable_address(self, identifier_node):
        name = identifier_node.children[0]
        return self.var_map.get(name, None) # If the variable does not exist, return None to validate where it is called

    def _get_variable_address_function(self, identifier_node):
        name = identifier_node.children[0]
        return self.function_var_map.get(name, None)

    def _get_operator(self, node):
        op = str(node).strip().lower()
        return {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
            'div': 'DIV',
            'mod': 'MOD',
            '=': 'EQUAL',
            '<>': 'NEQ',
            '<': 'INF',
            '>': 'SUP',
            '<=': 'INFEQ',
            '>=': 'SUPEQ',
            'and': 'AND',
            'or': 'OR',
            'not': 'NOT'
        }.get(op, f"UNKNOWN_OP({op})")

    def _visit(self, node):
        if node is None:
            return

        if self.debug_mode:
            print(f"== Visiting node: {node.nodetype} ==")

        visit_method = getattr(self, f"_visit_{node.nodetype.lower()}", None)
        if visit_method:
            visit_method(node)
        else:
            # If the node type does not have a specific method, visit its children
            self._visit_children(node)

    def _visit_children(self, node):
        for child in node.children:
            if isinstance(child, ASTNode):
                self._visit(child)

    def _visit_program(self, node):
        self._visit_children(node)

    def _visit_header(self, node):
        pass # We don't need the header information

    def _visit_content(self, node):
        self._visit_children(node)

    def _visit_declarations(self, node):
        self.output.append(" " * self.current_identation + "// Variable declarations")
        self._visit_children(node)

    def _visit_vardeclaration(self, node):
        for child in node.children:
            if child.nodetype == "ListVarDeclaration":
                self._visit(child)

    def _visit_listvardeclaration(self, node):
        for child in node.children:
            if child.nodetype == "VarElemDeclaration" or child.nodetype == "ListVarDeclaration":
                self._visit(child)

    def _visit_varelemdeclaration(self, node):
        if node.children[1].nodetype == "ArrayType":
            lower_bound = int(str(node.children[1].children[0].children[0].children[0].children[0].children[0]).strip())
            upper_bound = int(str(node.children[1].children[0].children[1].children[0].children[0].children[0]).strip())

            var_name = str(node.children[0].children[0].children[0]).strip()
            print(f"[DEBUG] Variable name: {var_name}")
            self.var_map[var_name] = self.var_counter # Add the variable to the map with the current address
            self.array_lower_bound_map[var_name] = lower_bound
            self.var_type_map[var_name] = node.children[1].children[0].nodetype
            self.output.append(" " * self.current_identation + f"PUSHI {upper_bound - lower_bound + 1}")
            self.output.append(" " * self.current_identation + f"ALLOCN // allocate array {var_name}")
            if not self.is_function_scope:  # If we are not inside a function
                self.output.append(" " * self.current_identation + f"STOREG {self.var_counter} // declare array {var_name}")
            else:  # If we are inside a function, add to the function variable map
                self.output.append(" " * self.current_identation + f"STOREL {self.function_var_counter} // declare array {var_name} in function scope")
            self.output.append("") # Add a new line for better readability
            self.var_counter += 1  # Increment the counter for the next variable
        elif node.children[1].children[0].nodetype == "string":
            var_name = str(node.children[0].children[0].children[0]).strip()
            self.var_map[var_name] = self.var_counter
            self.var_type_map[var_name] = "string"
            self.output.append(" " * self.current_identation + f"PUSHS \"\" // initialize string {var_name}")
            if not self.is_function_scope:  # If we are not inside a function
                self.output.append(" " * self.current_identation + f"STOREG {self.var_counter} // declare string {var_name}")
            else:  # If we are inside a function, add to the function variable map
                self.output.append(" " * self.current_identation + f"STOREL {self.function_var_counter} // declare string {var_name} in function scope")
            self.output.append("") # Add a new line for better readability
            self.var_counter += 1  # Increment the counter for the next variable
        else:
            for child in node.children:
                if child.nodetype == "IdentifierList":
                    self._visit(child)
                elif child.nodetype == "Type":
                    pass # We don't need the type information of the variables, if needed, we have to create a new visit for that

    def _visit_identifierlist(self, node):
        for child in node.children:
            if child.nodetype == "Identifier": # It has to be handled here because this is where we know it's a variable
                var_name = str(child.children[0]).strip()
                if not self.is_function_scope:  # If we are not inside a function
                    self.var_map[var_name] = self.var_counter # Add the variable to the map with the current address
                    self.var_type_map[var_name] = "integer"
                    self.output.append(" " * self.current_identation +  f"PUSHI 0 //initialize {var_name}")  # Initialize the variable with 0
                    self.output.append(" " * self.current_identation +  f"STOREG {self.var_counter} //declare {var_name}")  # Add the variable to the output
                    self.output.append("") # Add a new line for better readability
                    self.var_counter += 1  # Increment the counter for the next variable
                else:  # If we are inside a function, add to the function variable map
                    if var_name not in self.function_var_map:
                        self.function_var_map[var_name] = self.function_var_counter  # Add the variable to the map with the current address
                        self.function_var_type_map[var_name] = "integer"
                        self.output.append(" " * self.current_identation + f"PUSHI 0 //initialize {var_name} in function scope")
                        self.output.append(" " * self.current_identation + f"STOREL {self.function_var_counter} //declare {var_name} in function scope")
                        self.output.append("")  # Add a new line for better readability
                        self.function_var_counter += 1  # Increment the counter for the next function variable


    def _visit_compoundstatement(self, node):
        self.output.append(" " * self.current_identation + "// Start of compound statement (BEGIN ... END)")
        self._visit_children(node)

    def _visit_liststatement(self, node):
        self._visit_children(node)

    def _visit_liststatementaux(self, node):
        self._visit_children(node)

    def _visit_statement(self, node):
        self._visit_children(node)

    def _visit_procedurecall(self, node):
        identifier = node.children[0]  # First child is the identifier (Write, ReadLn, etc.)
        if identifier.nodetype == "Identifier": # It has to be handled here because this is where we know it's a function
            procedure_name = str(identifier.children[0]).strip().lower()
            if procedure_name == "write":
                self._visit_procedurewrite(node)
            elif procedure_name == "readln":
                self._visit_procedurereadln(node)
            elif procedure_name == "writeln":
                self._visit_procedurewriteln(node)

    def _visit_procedurewrite(self, node):
        self._visit_children(node)  # Visit children (such as the argument)
        self.output.append(" " * self.current_identation + "WRITES")

    def _visit_procedurereadln(self, node):
        self._visit_children(node)  # Visit children (such as the argument)
        var_name = str(node.children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0]).strip()

        if len(node.children[1].children[0].children[0].children[0].children[0].children[0].children[0].children) > 1: # If it is an array, must adjust for lower bound and get the index
            position_name = node.children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[0]
            if not self.is_function_scope:
                self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[var_name]}")
            else:  # If we are inside a function, add to the function variable map
                self.output.append(" " * self.current_identation + f"PUSHL {self.function_var_map[var_name]}")
            if not self.is_function_scope:  # If we are not inside a function
                self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[position_name]}")
            else:  # If we are inside a function, add to the function variable map
                self.output.append(" " * self.current_identation + f"PUSHL {self.function_var_map[position_name]}")
            self.output.append(" " * self.current_identation + f"// Adapt array index to lower bound")
            if not (self.array_lower_bound_map.get(var_name) is None):
                self.output.append(" " * self.current_identation + f"PUSHI {self.array_lower_bound_map[var_name]}")
            else:
                self.output.append(" " * self.current_identation + f"PUSHI 0")
            self.output.append(" " * self.current_identation + f"SUB")
            self.output.append(" " * self.current_identation + "READ")
            self.output.append(" " * self.current_identation + "ATOI")
            self.output.append(" " * self.current_identation + f"STOREN")
        else:
            self.output.append(" " * self.current_identation + "READ")
            if not (self.var_type_map.get(var_name) == "string"):
                self.output.append(" " * self.current_identation + "ATOI")

            if not self.is_function_scope:  # If we are not inside a function
                self.output.append(" " * self.current_identation + f"STOREG {self.var_map[var_name]}")
            else:  # If we are inside a function, add to the function variable map
                self.output.append(" " * self.current_identation + f"STOREL {self.function_var_map[var_name]}")

    def _visit_procedurewriteln(self, node):
        if len(node.children) > 1:
            arg_node = node.children[1]
            for child in arg_node.children:
                self._visit(child)
                if self._is_string(child):
                    self.output.append(" " * self.current_identation + "WRITES")
                else:
                    self.output.append(" " * self.current_identation + "WRITEI")
        self.output.append(" " * self.current_identation + "WRITELN")

    def _is_string(self, node):
        if node.children[0].children[0].children[0].children[0].children[0].nodetype == "UnsignedConstant":
            return node.children[0].children[0].children[0].children[0].children[0].children[0].nodetype == "String"
        return False

    def _visit_structeredstatement(self, node):
        self._visit_children(node)

    def _visit_conditionalstatement(self, node):
        self._visit_children(node)

    def _visit_ifstatement(self, node):
        condition_node = node.children[0]
        then_block = node.children[1]
        else_block = node.children[2] if len(node.children) > 2 else None

        else_label = f"ELSE{self.label_count}"
        end_label = f"END{self.label_count}"
        self.label_count += 1

        self._visit(condition_node)
        self.output.append(" " * self.current_identation + f"JZ {else_label}")

        self.current_identation += 2

        self._visit(then_block)
        self.output.append(" " * self.current_identation + f"JUMP {end_label}")
        self.output.append(" " * self.current_identation + f"{else_label}:")

        self.current_identation -= 2

        if else_block:
            self._visit(else_block)
        self.output.append(" " * self.current_identation + f"{end_label}:")

    def _visit_simplestatement(self, node):
        self._visit_children(node)

    def _visit_operator(self, node):
        self._visit_children(node)

    def _visit_relationaloperator(self, node):
        op = node.children[0]
        if op == "<>":
            self.output.append(" " * self.current_identation + "NEQ")
        elif op == "<":
            self.output.append(" " * self.current_identation + "INF")
        elif op == "<=":
            self.output.append(" " * self.current_identation + "INFEQ")
        elif op == ">":
            self.output.append(" " * self.current_identation + "SUP")
        elif op == ">=":
            self.output.append(" " * self.current_identation + "SUPEQ")

    def _visit_firstpriorityoperator(self, node):
        op = str(node.children[0]).strip().lower()
        if op == "*":
            self.output.append(" " * self.current_identation + "MUL")
        elif op == "/":
            self.output.append(" " * self.current_identation + "DIV")
        elif op == "div":
            self.output.append(" " * self.current_identation + "DIV")
        elif op == "mod":
            self.output.append(" " * self.current_identation + "MOD")
        elif op == "and":
            self.output.append(" " * self.current_identation + "AND")

    def _visit_secondpriorityoperator(self, node):
        if node.children[0] == "+":
            self.output.append(" " * self.current_identation + "ADD")
        elif node.children[0] == "-":
            self.output.append(" " * self.current_identation + "SUB")

    def _visit_else(self, node):
        self._visit_children(node)

    def _visit_expression(self, node):
        if len(node.children) == 1:
            self._visit(node.children[0])
        else:
            self._visit(node.children[0])
            self._visit(node.children[2])
            self.output.append(" " * self.current_identation + self._get_operator(node.children[1].children[0].children[0]))

    def _visit_simpleexpression(self, node):
        if len(node.children) == 1:
            self._visit(node.children[0])
        else:
            self._visit(node.children[0])
            self._visit(node.children[2])
            self.output.append(" " * self.current_identation + self._get_operator(node.children[1].children[0].children[0]))

    def _visit_assignment(self, node):
        destination = node.children[0].children[0].children[0]

        # Check if the destination is the same name as a function, if so, it's a return
        is_function_destination = False
        # Check if the destination is a function
        if destination in self.function_map:
            is_function_destination = True

        if len(node.children[1].children[0].children) > 2:
            source = None
            self._visit(node.children[1].children[0])
        elif len(node.children[1].children[0].children[0].children) > 1:
            source = None
            self._visit_children(node.children[1].children[0])
        elif node.children[1].children[0].children[0].children[0].children[0] == "true" or node.children[1].children[0].children[0].children[0].children[0] == "false":
            source = node.children[1].children[0].children[0].children[0].children[0]
        else:
            source = node.children[1].children[0].children[0].children[0].children[0].children[0].children[0]

        is_function_source = False
        if str(source).strip() in self.function_map:
            is_function_source = True

        self.output.append(" " * self.current_identation + f"// Assignment: {destination} := {source}")
        if source is None:
            pass
        elif is_function_destination:  # If it's a function return, it must be handled differently
            if self.function_map[destination] == "integer":
                if not self.is_function_scope:  # If we are not inside a function
                    self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[source]}")
                else:  # If we are inside a function, add to the function variable map
                    self.output.append(" " * self.current_identation + f"PUSHL {self.function_var_map[source]}")
            elif self.function_map[destination] == "string":
                self.output.append(" " * self.current_identation + f"PUSHS {self.var_map[source]}")
        elif node.children[1].children[0].children[0].children[0].children[0] == "true" or node.children[1].children[0].children[0].children[0].children[0] == "false":
            if source == "true":
                self.output.append(" " * self.current_identation + "PUSHI 1")
            if source == "false":
                self.output.append(" " * self.current_identation + "PUSHI 0")
        elif node.children[1].children[0].children[0].children[0].children[0].children[0].nodetype == "Num_Int":
            self.output.append(" " * self.current_identation + f"PUSHI {source}")  # Get the value of the number
        else:
            if is_function_source:
                for param in node.children[1].children[0].children[0].children[0].children[0].children[1].children:
                    parameter = str(param.children[0].children[0].children[0].children[0].children[0].children[0].children[0])
                    self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[parameter]}")
                    self.output.append(" " * self.current_identation + f"PUSHA {str(source).strip()}")
                    self.output.append(" " * self.current_identation + f"CALL")
            else:
                if not self.is_function_scope:
                    self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[source]}")  # Get the value of the variable
                else:  # If we are inside a function, add to the function variable map
                    self.output.append(" " * self.current_identation + f"PUSHL {self.function_var_map[source]}")  # Get the value of the local variable

        if not is_function_destination:
            if not self.is_function_scope:  # If we are inside a function, add to the function variable map
                self.output.append(" " * self.current_identation + f"STOREG {self.var_map[destination]}")  # Store the value in the destination variable
            else:  # If we are not inside a function
                self.output.append(" " * self.current_identation + f"STOREL {self.function_var_map[destination]}")  # Store the value in the local destination variable

    def _visit_term(self, node):
        if len(node.children) == 1:
            self._visit(node.children[0])
        else:
            self._visit(node.children[0])
            self._visit(node.children[2])
            self.output.append(" " * self.current_identation + self._get_operator(node.children[1].children[0].children[0]))

    def _visit_factor(self, node):
        self._visit_children(node)

    def _visit_functioncall(self, node):
        identifier = node.children[0]
        if identifier.nodetype == "Identifier":  # It has to be handled here because this is where we know it's a function
            function_name = str(identifier.children[0]).strip().lower()
            if function_name == "length":
                self.output.append(" " * self.current_identation + "// Function call: Length")
                self._visit(node.children[1])  # Visit the function arguments
                self.output.append(" " * self.current_identation + "STRLEN")

    def _visit_unsignedconstant(self, node):
        for child in node.children:
            if child.nodetype == "String":
                self.output.append(" " * self.current_identation + f'PUSHS "{child.children[0]}"')
            elif child.nodetype == "Num_Int":
                self.output.append(" " * self.current_identation + f"PUSHI {child.children[0]}")
            elif child.nodetype == "Char":
                self.output.append(" " * self.current_identation + f"PUSHS \"{(str(node.children[0].children[0]))}\"")
                self.output.append(" " * self.current_identation + "CHRCODE")

    def _visit_variable(self, node):
        if len(node.children) > 1: # If it is an array, must adjust for lower bound and get the index
            position_name = str(node.children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[0]).strip()
            var_name = str(node.children[0].children[0]).strip()

            if not self.is_function_scope:
                self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[var_name]}")
                self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[position_name]}")
            else:  # If we are inside a function, add to the function variable map
                self.output.append(" " * self.current_identation + f"PUSHL {self.function_var_map[var_name]}")
                self.output.append(" " * self.current_identation + f"PUSHL {self.function_var_map[position_name]}")
            self.output.append(" " * self.current_identation + f"// Adapt array index to lower bound")
            if not (self.array_lower_bound_map.get(var_name) is None):
                self.output.append(" " * self.current_identation + f"PUSHI {self.array_lower_bound_map[var_name]}")
            else:
                self.output.append(" " * self.current_identation + f"PUSHI 1")
            self.output.append(" " * self.current_identation + f"SUB")
            if self.var_type_map.get(var_name) == "string":
                self.output.append(" " * self.current_identation + "CHARAT")
            else:
                self.output.append(" " * self.current_identation + "LOADN")
        else:
            for child in node.children:
                if child.nodetype == "Identifier":
                    if not self.is_function_scope:  # If we are not inside a function
                        variable_address = self._get_variable_address(child)
                        if variable_address is not None:
                            self.output.append(" " * self.current_identation + f"PUSHG {variable_address}")
                    else:  # If we are inside a function, add to the function variable map
                        variable_address = self._get_variable_address_function(child)
                        if variable_address is not None:
                            self.output.append(" " * self.current_identation + f"PUSHL {variable_address}")

    def _visit_repetitivestatement(self, node):
        self._visit_children(node)

    def _visit_forstatement(self, node):
        iterator_name = node.children[0].children[0].nodetype
        if node.children[2].children[0].children[0].children[0].children[0].nodetype == "FunctionCall":
            start_value = node.children[2].children[0].children[0].children[0].children[0]
        else:
            start_value = int(node.children[2].children[0].children[0].children[0].children[0].children[0].children[0])
        end_variable_name = node.children[4].children[0].children[0].children[0].children[0].children[0].children[0]
        if node.children[4].children[0].children[0].children[0].children[0].nodetype == "UnsignedConstant":
            end_variable_name = int(end_variable_name)

        self.output.append(" " * self.current_identation + "// For statement")
        init_label = f"LOOP{self.loop_label_count}"
        end_label = f"ENDLOOP{self.loop_label_count}"
        self.loop_label_count += 1

        if isinstance(start_value, int):
            self.output.append(" " * self.current_identation + f"PUSHI {start_value}")
        else:
            self._visit(start_value)  # If it is a variable, visit the node to get the value

        if not self.is_function_scope:  # If we are not inside a function
            self.output.append(" " * self.current_identation + f"STOREG {self.var_map[iterator_name]}")
        else:  # If we are inside a function, add to the function variable map
            self.output.append(" " * self.current_identation + f"STOREL {self.function_var_map[iterator_name]}")
        self.output.append(" " * self.current_identation + f"{init_label}:")
        self.current_identation += 2

        if not self.is_function_scope:  # If we are not inside a function
            self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[iterator_name]}")
        else:  # If we are inside a function, add to the function variable map
            self.output.append(" " * self.current_identation + f"PUSHL {self.function_var_map[iterator_name]}")

        if isinstance(end_variable_name, int):
            self.output.append(" " * self.current_identation + f"PUSHI {end_variable_name}")
        else:
            if not self.is_function_scope:  # If we are not inside a function
                self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[end_variable_name]}")
            else:  # If we are inside a function, add to the function variable map
                self.output.append(" " * self.current_identation + f"PUSHL {self.function_var_map[end_variable_name]}")
        if node.children[3] == "DownTo":
            self.output.append(" " * self.current_identation + f"SUPEQ")
        else:
            self.output.append(" " * self.current_identation + f"INFEQ")
        self.output.append(" " * self.current_identation + f"JZ {end_label}")
        self.output.append(" " * self.current_identation + f"// For statement body")
        self._visit(node.children[6]) # Visit the loop body
        self.output.append(" " * self.current_identation + f"// End of for statement body")
        self.output.append("")
        self.output.append(" " * self.current_identation + f"// Increment iterator")
        if not self.is_function_scope:  # If we are not inside a function
            self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[iterator_name]}")
        else:  # If we are inside a function, add to the function variable map
            self.output.append(" " * self.current_identation + f"PUSHL {self.function_var_map[iterator_name]}")
        self.output.append(" " * self.current_identation + f"PUSHI 1")
        if node.children[3] == "DownTo":
            self.output.append(" " * self.current_identation + f"SUB")
        else:
            self.output.append(" " * self.current_identation + f"ADD")
        if not self.is_function_scope:  # If we are not inside a function
            self.output.append(" " * self.current_identation + f"STOREG {self.var_map[iterator_name]}")
        else:  # If we are inside a function, add to the function variable map
            self.output.append(" " * self.current_identation + f"STOREL {self.function_var_map[iterator_name]}")

        self.output.append(" " * self.current_identation + f"JUMP {init_label}")
        self.current_identation -= 2

        self.output.append(" " * self.current_identation + f"{end_label}:")
        self.output.append(" " * self.current_identation + "// End of for statement")
        self.output.append("")

    def _visit_whilestatement(self, node):
        start_label = f"WHILE{self.loop_label_count}"
        end_label = f"ENDWHILE{self.loop_label_count}"
        self.loop_label_count += 1

        self.output.append(" " * self.current_identation + f"{start_label}:")

        self.current_identation += 2
        self._visit(node.children[0])  # While condition
        self.output.append(" " * self.current_identation + f"JZ {end_label}")
        self.output.append(" " * self.current_identation + f"// While statement body")
        self._visit(node.children[2])
        self.output.append(" " * self.current_identation + f"JUMP {start_label}")
        self.current_identation -= 2

        self.output.append(" " * self.current_identation + f"{end_label}:")

    def _visit_functiondeclaration(self, node):
        function_name = str(node.children[0].children[0]).strip()
        self.output_functions.append("")
        self.output_functions.append(f"{function_name}:")

        self.function_var_counter = 0
        self.function_var_map = {}

        self.current_identation += 2
        parameters = node.children[1].children[0].children
        parameters_length = len(parameters)

        if parameters_length > 0:
            # add the parameters to the function variable map
            for i, param in enumerate(parameters):
                param_name = str(param.children[0].children[0].children[0]).strip()

                # Calculate the corresponding negative index
                param_index = i - parameters_length  # This gives -3, -2, -1 for 3 parameters

                self.function_var_map[param_name] = self.function_var_counter
                self.function_var_type_map[param_name] = (param.children[1].children[0].strip().lower() if len(param.children) > 1 else "void")

                self.output_functions.append(" " * self.current_identation + f"PUSHL {param_index} // parameter {param_name}")
                self.output_functions.append(" " * self.current_identation + f"STOREL {self.function_var_counter} // store parameter {param_name} in function scope")

                self.function_var_counter += 1

        self.output_functions.append(" " * self.current_identation + "// Function body")
        self.function_map[function_name] = (node.children[2].children[0]).strip().lower() if len(node.children) > 2 else "void"
        self.is_function_scope = True
        self._visit_children(node.children[3])

        indent_str = " " * self.current_identation
        new_output = []
        lines_to_move = []

        i = 0
        while i < len(self.output):
            line = self.output[i]

            if line.startswith(indent_str):
                # Start collecting group of lines (with indentation and blank lines around)
                # Check if there are blank lines before
                if i > 0 and self.output[i-1].strip() == '':
                    lines_to_move.append(self.output[i-1])
                    new_output = new_output[:-1]  # Remove the blank line that has already been added

                # Collect the lines with indentation and the following blank lines
                while i < len(self.output) and (self.output[i].startswith(indent_str) or self.output[i].strip() == ''):
                    lines_to_move.append(self.output[i])
                    i += 1
                # Do not increment i here because it has already been incremented in the inner while
                continue
            else:
                new_output.append(line)
                i += 1

        self.output = new_output
        self.output_functions.extend(lines_to_move)

        self.is_function_scope = False
        self.output_functions.append(" " * self.current_identation + "// End of function body")
        self.output_functions.append(" " * self.current_identation + "RETURN")
        self.current_identation -= 2
        self.output_functions.append("")

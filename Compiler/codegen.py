from ASTree.astree import ASTNode

class CodeGenerator:
    def __init__(self):
        self.output = []
        self.var_counter = 0 # Perceber qual o endereço a utilizar para a próxima variável
        self.var_map = {} # Mapear o sitio da memória para cada variável
        self.var_type_map = {} # Mapear o tipo de cada variável
        self.array_lower_bound_map = {} # Mapear o indice inferior de cada array
        self.label_count = 0
        self.loop_label_count = 0
        self.current_identation = 2

    def generate(self, ast_root):
        self.output.append("START\n")
        self._visit(ast_root)
        self.output.append("\nSTOP")
        return "\n".join(self.output)

    def _get_variable_address(self, identifier_node):
        """Determina o endereço da variável baseado no nome do identificador."""
        name = identifier_node.children[0]
        return self.var_map.get(name, None) # Caso a variável não exista, retorna None para validar onde é chamada

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
        """Visita um nó e chama o método adequado de acordo com seu tipo."""
        if node is None:
            return

        print(f"== Visiting node: {node.nodetype} ==")

        # Verifica se existe um método específico para o tipo de nó
        visit_method = getattr(self, f"_visit_{node.nodetype.lower()}", None)
        if visit_method:
            visit_method(node)
        else:
            # Caso o tipo de nó não tenha um método específico, percorre seus filhos
            self._visit_children(node)

    def _visit_children(self, node):
        """Visita todos os filhos de um nó."""
        for child in node.children:
            if isinstance(child, ASTNode):
                self._visit(child)

    def _visit_program(self, node):
        """Lida com o nó 'Program'."""
        print("[DEBUG] Visiting program")
        self._visit_children(node)

    def _visit_header(self, node):
        """Lida com o nó 'Header'."""
        print("[DEBUG] Visiting header, ignoring")
        pass # Não precisamos da informação do cabeçalho

    def _visit_content(self, node):
        """Lida com o nó 'Content'."""
        print("[DEBUG] Visiting content")
        self._visit_children(node)

    def _visit_declarations(self, node):
        """Lida com o nó 'Declarations'."""
        print("[DEBUG] Visiting declarations")
        self.output.append(" " * self.current_identation + "// Variable declarations")
        self._visit_children(node)

    def _visit_vardeclaration(self, node):
        """Lida com a declaração de variáveis."""
        print("[DEBUG] Visiting variable declaration")
        for child in node.children:
            if child.nodetype == "ListVarDeclaration":
                self._visit(child)

    def _visit_listvardeclaration(self, node):
        """Lida com a lista de declarações de variáveis."""
        print("[DEBUG] Visiting list variable declaration")
        for child in node.children:
            if child.nodetype == "VarElemDeclaration" or child.nodetype == "ListVarDeclaration":
                self._visit(child)

    def _visit_varelemdeclaration(self, node):
        """Lida com cada elemento da declaração de variável."""
        print("[DEBUG] Visiting variable element declaration")

        print(f"[DEBUG] Node childrenNNNNNNNNNNNNNNNNNNNNNNNN: {node}")

        if node.children[1].nodetype == "ArrayType":
            lower_bound = int(str(node.children[1].children[0].children[0].children[0].children[0].children[0]).strip())
            upper_bound = int(str(node.children[1].children[0].children[1].children[0].children[0].children[0]).strip())

            var_name = str(node.children[0].children[0].children[0]).strip()
            print(f"[DEBUG] Variable name: {var_name}")
            self.var_map[var_name] = self.var_counter # Adiciona a variável ao mapa com o endereço atual
            self.array_lower_bound_map[var_name] = lower_bound
            self.var_type_map[var_name] = node.children[1].children[0].nodetype
            self.output.append(" " * self.current_identation + f"PUSHI {upper_bound - lower_bound + 1}")
            self.output.append(" " * self.current_identation + f"ALLOCN // allocate array {var_name}")
            self.output.append(" " * self.current_identation + f"STOREG {self.var_counter} // declare array {var_name}")
            self.output.append("") # Adiciona uma nova linha para melhor legibilidade
            self.var_counter += 1  # Incrementa o contador para a próxima variável
        elif node.children[1].children[0].nodetype == "string":
            var_name = str(node.children[0].children[0].children[0]).strip()
            self.var_map[var_name] = self.var_counter
            self.var_type_map[var_name] = "string"
            self.output.append(" " * self.current_identation + f"PUSHS \"\" // initialize string {var_name}")
            self.output.append(" " * self.current_identation + f"STOREG {self.var_counter} // declare string {var_name}")
            self.output.append("") # Adiciona uma nova linha para melhor legibilidade
            self.var_counter += 1  # Incrementa o contador para a próxima variável

        else:
            for child in node.children:
                if child.nodetype == "IdentifierList":
                    self._visit(child)
                elif child.nodetype == "Type":
                    pass # Não precisamos da informação do tipo das variáveis, for preciso, temos de criar um visit novo para isso

    def _visit_identifierlist(self, node):
        """Lida com a lista de identificadores."""
        print("[DEBUG] Visiting identifier list")
        for child in node.children:
            if child.nodetype == "Identifier": # Tem de ser tratador aqui porque é onde sabemos que é uma variável
                var_name = str(child.children[0]).strip()
                self.var_map[var_name] = self.var_counter # Adiciona a variável ao mapa com o endereço atual
                self.var_type_map[var_name] = "integer"
                self.output.append(" " * self.current_identation +  f"PUSHI 0 //initialize {var_name}")  # Inicializa a variável com 0
                self.output.append(" " * self.current_identation +  f"STOREG {self.var_counter} //declare {var_name}")  # Adiciona a variável à saída
                self.output.append("") # Adiciona uma nova linha para melhor legibilidade
                self.var_counter += 1  # Incrementa o contador para a próxima variável

    def _visit_compoundstatement(self, node):
        """Lida com o nó 'CompoundStatement'."""
        print("[DEBUG] Visiting compound statement")
        self.output.append(" " * self.current_identation + "// Start of compound statement (BEGIN ... END)")
        self._visit_children(node)

    def _visit_liststatement(self, node):
        print("[DEBUG] Visiting list statement")
        self._visit_children(node)

    def _visit_liststatementaux(self, node):
        print("[DEBUG] Visiting list statement auxiliary")
        self._visit_children(node)

    def _visit_statement(self, node):
        """Lida com o nó 'Statement'."""
        print("[DEBUG] Visiting statement")
        self._visit_children(node)

    def _visit_procedurecall(self, node):
        """Lida com a chamada de procedimento (ex: Write, ReadLn)."""
        identifier = node.children[0]  # Primeiro filho é o identificador (Write, ReadLn, etc.)
        if identifier.nodetype == "Identifier": # Tem de ser tratado aqui porque é onde sabemos que é uma função
            procedure_name = str(identifier.children[0]).strip().lower()
            if procedure_name == "write":
                self._visit_procedurewrite(node)
            elif procedure_name == "readln":
                self._visit_procedurereadln(node)
            elif procedure_name == "writeln":
                self._visit_procedurewriteln(node)

    def _visit_procedurewrite(self, node):
        """Lida com a chamada de 'Write'."""
        self._visit_children(node)  # Visita os filhos (como o argumento)
        self.output.append(" " * self.current_identation + "WRITES")

    def _visit_procedurereadln(self, node):
        """Lida com a chamada de 'ReadLn'."""
        print("[DEBUG] Visiting procedure input")
        self._visit_children(node)  # Visita os filhos (como o argumento)
        var_name = str(node.children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0]).strip()

        if len(node.children[1].children[0].children[0].children[0].children[0].children[0].children[0].children) > 1: # Se for um array, tem de fazer a diferença para o lower bound e ir buscar o indice
            position_name = node.children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[0]
            self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[var_name]}")
            self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[position_name]}")
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
            self.output.append(" " * self.current_identation + f"STOREG {self.var_map[var_name]}")

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
        print("[DEBUG] Checking if node is a string")
        if node.children[0].children[0].children[0].children[0].children[0].nodetype == "UnsignedConstant":
            return node.children[0].children[0].children[0].children[0].children[0].children[0].nodetype == "String"
        return False

    def _visit_structeredstatement(self, node):
        print("[DEBUG] Visiting structured statement")
        self._visit_children(node)

    def _visit_conditionalstatement(self, node):
        print("[DEBUG] Visiting conditional statement")
        self._visit_children(node)

    def _visit_ifstatement(self, node):
        print("[DEBUG] Visiting if statement")
        condition_node = node.children[0]
        then_block = node.children[1]
        else_block = node.children[2] if len(node.children) > 2 else None

        print("=" * 20)
        print(f"Condition: {condition_node}")
        print(f"Then block: {then_block}")
        print(f"Else block: {else_block}")
        print("=" * 20)

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
        print("[DEBUG] Visiting simple statement")
        self._visit_children(node)

    def _visit_operator(self, node):
        print("[DEBUG] Visiting operator")
        self._visit_children(node)

    def _visit_relationaloperator(self, node):
        print("[DEBUG] Visiting relational operator")
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
        print("[DEBUG] Visiting first priority operator")
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
        print("[DEBUG] Visiting second priority operator")
        if node.children[0] == "+":
            self.output.append(" " * self.current_identation + "ADD")
        elif node.children[0] == "-":
            self.output.append(" " * self.current_identation + "SUB")

    def _visit_else(self, node):
        """Lida com o bloco do 'else'."""
        self._visit_children(node)

    def _visit_expression(self, node):
        print("[DEBUG] Visiting expression")
        if len(node.children) == 1:
            self._visit(node.children[0])
        else:
            self._visit(node.children[0])
            self._visit(node.children[2])
            self.output.append(" " * self.current_identation + self._get_operator(node.children[1].children[0].children[0]))

    def _visit_simpleexpression(self, node):
        print("[DEBUG] Visiting simple expression")
        if len(node.children) == 1:
            self._visit(node.children[0])
        else:
            self._visit(node.children[0])
            self._visit(node.children[2])
            self.output.append(" " * self.current_identation + self._get_operator(node.children[1].children[0].children[0]))

    def _visit_assignment(self, node):
        print("[DEBUG] Visiting assignment")
        destination = node.children[0].children[0].children[0]

        print(f"[DEBUG] Expression children ÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇÇç: {node}")

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

        print(f"[DEBUG] Destination: {destination}")
        print(f"[DEBUG] Source: {source}")
        self.output.append(" " * self.current_identation + f"// Assignment: {destination} := {source}")
        if source is None:
            pass
        elif node.children[1].children[0].children[0].children[0].children[0] == "true" or node.children[1].children[0].children[0].children[0].children[0] == "false":
            if source == "true":
                self.output.append(" " * self.current_identation + "PUSHI 1")
            if source == "false":
                self.output.append(" " * self.current_identation + "PUSHI 0")
        elif node.children[1].children[0].children[0].children[0].children[0].children[0].nodetype == "Num_Int":
            self.output.append(" " * self.current_identation + f"PUSHI {source}")  # Pega no valor do número
        else:
            self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[source]}")  # Pega no valor da variável
        self.output.append(" " * self.current_identation + f"STOREG {self.var_map[destination]}")  # Armazena o valor na variável de destino

    def _visit_term(self, node):
        print("[DEBUG] Visiting term")
        if len(node.children) == 1:
            self._visit(node.children[0])
        else:
            self._visit(node.children[0])
            self._visit(node.children[2])
            self.output.append(" " * self.current_identation + self._get_operator(node.children[1].children[0].children[0]))

    def _visit_factor(self, node):
        """Lida com o nó 'Factor'."""
        self._visit_children(node)

    def _visit_functioncall(self, node):
        """Lida com a chamada de função."""
        print("[DEBUG] Visiting function call")
        identifier = node.children[0]
        if identifier.nodetype == "Identifier":  # Tem de ser tratado aqui porque é onde sabemos que é uma função
            function_name = str(identifier.children[0]).strip().lower()
            if function_name == "length":
                self.output.append(" " * self.current_identation + "// Function call: Length")
                self._visit(node.children[1])  # Visita os argumentos da função
                self.output.append(" " * self.current_identation + "STRLEN")

    def _visit_unsignedconstant(self, node):
        """Lida com o nó 'UnsignedConstant' (para strings)."""
        for child in node.children:
            if child.nodetype == "String":
                self.output.append(" " * self.current_identation + f'PUSHS "{child.children[0]}"')
            elif child.nodetype == "Num_Int":
                self.output.append(" " * self.current_identation + f"PUSHI {child.children[0]}")
            elif child.nodetype == "Char":
                self.output.append(" " * self.current_identation + f"PUSHS \"{(str(node.children[0].children[0]))}\"")
                self.output.append(" " * self.current_identation + "CHRCODE")

    def _visit_variable(self, node):
        """Lida com o nó 'Variable' (para variáveis como num1, num2, etc.)."""
        # [TODO] Verificar se é uma variável ou um array
        print("[DEBUG] Visiting variable")

        if len(node.children) > 1: # Se for um array, tem de fazer a diferença para o lower bound e ir buscar o indice
            print(f"[DEBUG] OHHHHHHHHHHHHHHHHHHHHHHHHHH: {node.children[0]}")
            position_name = str(node.children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[0]).strip()
            var_name = str(node.children[0].children[0]).strip()
            print(f"[DEBUG] Position name: {position_name}")
            print(f"[DEBUG] Variable name: {var_name}")
            self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[var_name]}")
            self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[position_name]}")
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
                    print(f"Map: {self.var_map}")
                    variable_address = self._get_variable_address(child)
                    if variable_address is not None:
                        self.output.append(" " * self.current_identation + f"PUSHG {variable_address}")

    def _visit_repetitivestatement(self, node):
        """Lida com o nó 'RepetitiveStatement'."""
        print("[DEBUG] Visiting repetitive statement")
        self._visit_children(node)

    def _visit_forstatement(self, node):
        """Lida com o nó 'ForStatement'."""
        print("[DEBUG] Visiting for statement")

        iterator_name = node.children[0].children[0].nodetype
        print(f"[DEBUG] Iterator: {iterator_name}")
        if node.children[2].children[0].children[0].children[0].children[0].nodetype == "FunctionCall":
            start_value = node.children[2].children[0].children[0].children[0].children[0]
            print(f"[DEBUG] Start value is a function call: {start_value}")
        else:
            start_value = int(node.children[2].children[0].children[0].children[0].children[0].children[0].children[0])
        print(f"[DEBUG] Start value: {start_value}")
        end_variable_name = node.children[4].children[0].children[0].children[0].children[0].children[0].children[0]
        if node.children[4].children[0].children[0].children[0].children[0].nodetype == "UnsignedConstant":
            end_variable_name = int(end_variable_name)
        print(f"[DEBUG] End variable name: {end_variable_name}")

        self.output.append(" " * self.current_identation + "// For statement")
        init_label = f"LOOP{self.loop_label_count}"
        end_label = f"ENDLOOP{self.loop_label_count}"
        self.loop_label_count += 1

        if isinstance(start_value, int):
            self.output.append(" " * self.current_identation + f"PUSHI {start_value}")
        else:
            self._visit(start_value)  # Se for uma variável, visita o nó para obter o valor
        self.output.append(" " * self.current_identation + f"STOREG {self.var_map[iterator_name]}")
        self.output.append(" " * self.current_identation + f"{init_label}:")
        self.current_identation += 2

        self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[iterator_name]}")

        if isinstance(end_variable_name, int):
            self.output.append(" " * self.current_identation + f"PUSHI {end_variable_name}")
        else:
            self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[end_variable_name]}")
        if node.children[3] == "DownTo":
            self.output.append(" " * self.current_identation + f"SUPEQ")
        else:
            self.output.append(" " * self.current_identation + f"INFEQ")
        self.output.append(" " * self.current_identation + f"JZ {end_label}")
        self.output.append(" " * self.current_identation + f"// For statement body")
        self._visit(node.children[6]) # Visita o corpo do loop
        self.output.append(" " * self.current_identation + f"// End of for statement body")
        self.output.append("")
        self.output.append(" " * self.current_identation + f"// Increment iterator")
        self.output.append(" " * self.current_identation + f"PUSHG {self.var_map[iterator_name]}")
        self.output.append(" " * self.current_identation + f"PUSHI 1")
        if node.children[3] == "DownTo":
            self.output.append(" " * self.current_identation + f"SUB")
        else:
            self.output.append(" " * self.current_identation + f"ADD")
        self.output.append(" " * self.current_identation + f"STOREG {self.var_map[iterator_name]}")

        self.output.append(" " * self.current_identation + f"JUMP {init_label}")
        self.current_identation -= 2

        self.output.append(" " * self.current_identation + f"{end_label}:")
        self.output.append(" " * self.current_identation + "// End of for statement")
        self.output.append("")

    def _visit_whilestatement(self, node):
        """Lida com o nó 'WhileStatement'."""
        print("[DEBUG] Visiting while statement")

        start_label = f"WHILE{self.loop_label_count}"
        end_label = f"ENDWHILE{self.loop_label_count}"
        self.loop_label_count += 1

        self.output.append(" " * self.current_identation + f"{start_label}:")

        self.current_identation += 2
        self._visit(node.children[0])  # Condição do while
        self.output.append(" " * self.current_identation + f"JZ {end_label}")
        self.output.append(" " * self.current_identation + f"// While statement body")
        self._visit(node.children[2])
        self.output.append(" " * self.current_identation + f"JUMP {start_label}")
        self.current_identation -= 2

        self.output.append(" " * self.current_identation + f"{end_label}:")

from ASTree.astree import ASTNode

class CodeGenerator:
    def __init__(self):
        self.output = []
        self.var_counter = 0 # Perceber qual o endereço a utilizar para a próxima variável
        self.var_map = {} # Mapear o sitio da memória para cada variável
        self.label_count = 0
        self.current_identation = 2

    def generate(self, ast_root):
        self.output.append("START\n")
        self._visit(ast_root)
        self.output.append("\nSTOP")
        return "\n".join(self.output)

    def _generate_label(self, base):
        self.label_count += 1
        return f"{base}{self.label_count}"

    def _get_variable_address(self, identifier_node):
        """Determina o endereço da variável baseado no nome do identificador."""
        name = identifier_node.children[0]
        return self.var_map.get(name, None) # Caso a variável não exista, retorna None para validar onde é chamada

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
            if child.nodetype == "VarElemDeclaration":
                self._visit(child)

    def _visit_varelemdeclaration(self, node):
        """Lida com cada elemento da declaração de variável."""
        print("[DEBUG] Visiting variable element declaration")
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
                self.output.append(" " * self.current_identation +  f"PUSHI 0 //initialize {var_name}")  # Inicializa a variável com 0
                self.output.append(" " * self.current_identation +  f"STOREG {self.var_counter} //declare {var_name}")  # Adiciona a variável à saída
                self.output.append("\n") # Adiciona uma nova linha para melhor legibilidade
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
        self.output.append(" " * self.current_identation + "READ")
        self.output.append(" " * self.current_identation + "ATOI")
        self.output.append(" " * self.current_identation + f"STOREG {self.var_map[var_name]}")  # Armazena o valor lido no endereço da variável

    def _visit_procedurewriteln(self, node):
        if len(node.children) > 1:
            arg_node = node.children[1]
            self._visit(arg_node)
            if self._is_string(arg_node):
                self.output.append(" " * self.current_identation + "WRITES")
            else:
                self.output.append(" " * self.current_identation + "WRITEI")
        self.output.append(" " * self.current_identation + "WRITELN")

    def _is_string(self, node):
        if node.children[0].children[0].children[0].children[0].children[0].children[0].nodetype == "UnsignedConstant":
            return node.children[0].children[0].children[0].children[0].children[0].children[0].children[0].nodetype == "String"
        return False

    def _visit_ifstatement(self, node): # FIQUEI AQUI, PRECISO DE CORRIGIR O ELSE
        condition_node = node.children[0]
        then_block = node.children[1]
        else_block = node.children[2] if len(node.children) > 2 else None

        else_label = self._generate_label("ELSE")
        end_label = self._generate_label("ENDIF")

        self._visit(condition_node)
        self.output.append(" " * self.current_identation + f"JZ {else_label}")

        self._visit(then_block)
        self.output.append(" " * self.current_identation + f"JUMP {end_label}")
        self.output.append(" " * self.current_identation + f"{else_label}:")
        if else_block:
            self._visit(else_block)
        self.output.append(" " * self.current_identation + f"{end_label}:")

    def _visit_else(self, node):
        """Lida com o bloco do 'else'."""
        self._visit_children(node)  # Executa os filhos (como o bloco 'else')

    def _visit_expression(self, node):
        """Lida com o nó 'Expression'."""
        self._visit_children(node)

    def _visit_term(self, node):
        """Lida com o nó 'Term'."""
        self._visit_children(node)

    def _visit_factor(self, node):
        """Lida com o nó 'Factor'."""
        self._visit_children(node)

    def _visit_unsignedconstant(self, node):
        """Lida com o nó 'UnsignedConstant' (para strings)."""
        for child in node.children:
            if child.nodetype == "String":
                self.output.append(" " * self.current_identation + f'PUSHS "{child.children[0]}"')

    def _visit_variable(self, node):
        """Lida com o nó 'Variable' (para variáveis como num1, num2, etc.)."""
        for child in node.children:
            if child.nodetype == "Identifier":
                variable_address = self._get_variable_address(child)
                if variable_address is not None:
                    self.output.append(" " * self.current_identation + f"PUSHG {variable_address}")

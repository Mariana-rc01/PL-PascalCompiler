from ASTree.astree import ASTNode

class CodeGenerator:
    def __init__(self):
        self.output = []

    def generate(self, ast_root):
        self.output.append("START\n")
        self._visit(ast_root)
        self.output.append("\nSTOP")
        return "\n".join(self.output)

    def _visit(self, node):
        if node is None:
            return
        if node.nodetype == "String":
            self.output.append(f'  PUSHS "{node.children[0]}"')
            self.output.append("  WRITES")
        elif node.nodetype == "ProcedureCall":
            self._visit(node.children[1])  # ListArgs
            self.output.append("  WRITELN")
        else:
            for child in node.children:
                if isinstance(child, ASTNode):
                    self._visit(child)

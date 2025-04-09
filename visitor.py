# visitor.py

from ast_nodes import ASTNode

class NodeVisitor:
    def visit(self, node):
        if node is None:
            return
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # Se node for uma tupla ou lista, visita cada elemento
        if isinstance(node, (list, tuple)):
            for item in node:
                self.visit(item)
            return
        # Se for um objeto com __dict__, itera sobre seus atributos
        if hasattr(node, '__dict__'):
            for attr in vars(node).values():
                self.visit(attr)

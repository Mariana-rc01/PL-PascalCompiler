class ASTNode:
    def __init__(self, nodetype, children=None, value=None):
        """
        nodetype: string defining the type (e.g., 'Program', 'Assignment', 'IfStatement', etc.)
        children: list of ASTNode or terminal nodes
        value: associated value (e.g., identifier name or constant value)
        """
        self.nodetype = nodetype
        self.children = children if children is not None else []
        self.value = value

    def __str__(self, level=0):
        indent = "  " * level
        rep = f"{indent}{self.nodetype}"
        if self.value is not None:
            rep += f": {self.value}"
        rep += "\n"
        for child in self.children:
            # If the child is a string or number, convert to string; if it's a node, call __str__
            if isinstance(child, ASTNode):
                rep += child.__str__(level + 1)
            else:
                rep += "  " * (level + 1) + str(child) + "\n"
        return rep

if __name__ == '__main__':
    # Example usage and debugging of the AST
    node = ASTNode("Program", [
        ASTNode("Header", value="MyProgram"),
        ASTNode("Content", [
            ASTNode("VariableDeclaration", value="x: integer"),
            ASTNode("Assignment", [
                ASTNode("Variable", value="x"),
                ASTNode("Expression", value="5")
            ])
        ])
    ])
    print(node)

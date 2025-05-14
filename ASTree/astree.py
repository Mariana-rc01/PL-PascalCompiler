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
            if child is None:
                continue
            # If the child is a string or number, convert to string; if it's a node, call __str__
            if isinstance(child, ASTNode):
                rep += child.__str__(level + 1)
            else:
                rep += "  " * (level + 1) + str(child) + "\n"
        return rep

    def __eq__(self, other):
        if not isinstance(other, ASTNode):
            return False
        if self.nodetype != other.nodetype:
            return False

        if isinstance(self.value, str) and isinstance(other.value, str):
            if self.value != other.value:
                return False

        elif isinstance(self.value, ASTNode) and isinstance(other.value, ASTNode):
            if self.value != other.value:
                return False

        if len(self.children) != len(other.children):
            return False
        for i, (a, b) in enumerate(zip(self.children, other.children)):
            if isinstance(a, ASTNode) and isinstance(b, ASTNode):
                if a != b:
                    return False
            elif a != b:
                return False
        return True

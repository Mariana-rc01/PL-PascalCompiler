import sys
import tkinter as tk
from ASTree.astree import ASTNode

def parse_ast(text):
    """
    Converts a textual representation of an AST (with indentation)
    into a tree of ASTNode objects.

    Each line should have the format:
       <indentation><nodetype>[: <value>]

    Example:
       Program: .
         Header: program header (simplified)
           Identifier: SomaArray
         Content
           Declarations
             ...
    """
    lines = [line.rstrip() for line in text.splitlines() if line.strip() != ""]

    def parse_nodes(index, current_indent):
        nodes = []
        while index < len(lines):
            line = lines[index]
            indent = len(line) - len(line.lstrip(' '))
            if indent < current_indent:
                return nodes, index
            node_text = line.strip()
            if ':' in node_text:
                parts = node_text.split(':', 1)
                nodetype = parts[0].strip()
                value = parts[1].strip()
            else:
                nodetype = node_text
                value = None
            node = ASTNode(nodetype, value=value)
            index += 1
            if index < len(lines):
                next_indent = len(lines[index]) - len(lines[index].lstrip(' '))
                if next_indent > indent:
                    children, index = parse_nodes(index, next_indent)
                    node.children = children
            nodes.append(node)
        return nodes, index

    nodes, _ = parse_nodes(0, 0)
    return nodes[0] if nodes else None

class TreeDrawer:
    def __init__(self, root_node, vertical_offset=70):
        self.root_node = root_node
        self.x_spacing = 60      # horizontal spacing
        self.y_spacing = 100     # vertical spacing
        self.vertical_offset = vertical_offset
        self.leaf_width = 60     # minimum width for leaf nodes
        self.nodes_positions = {}

    def _calc_positions(self, node, depth=0, x=0):
        """
        Recursively calculates the positions of the nodes.
        Returns the x position and the total width occupied by the node.
        """
        if not node.children:
            self.nodes_positions[node] = (x, depth * self.y_spacing)
            return x, self.leaf_width  # fixed width for leaf nodes

        current_x = x
        total_width = 0
        children_positions = []
        for child in node.children:
            if isinstance(child, ASTNode):
                child_x, child_width = self._calc_positions(child, depth + 1, current_x)
                children_positions.append(child_x)
                current_x += child_width + self.x_spacing
                total_width += child_width + self.x_spacing
            else:
                # If the child is a simple terminal
                self.nodes_positions[child] = (current_x, (depth + 1) * self.y_spacing)
                children_positions.append(current_x)
                child_width = self.leaf_width
                current_x += child_width + self.x_spacing
                total_width += child_width + self.x_spacing

        total_width -= self.x_spacing
        parent_x = (children_positions[0] + children_positions[-1]) // 2
        self.nodes_positions[node] = (parent_x, depth * self.y_spacing)
        return parent_x, total_width

    def _center_positions(self, canvas_width):
        """
        Adjusts the positions to center the tree on the canvas and applies the vertical offset.
        """
        xs = [pos[0] for pos in self.nodes_positions.values()]
        if not xs:
            return
        min_x = min(xs)
        max_x = max(xs)
        tree_width = max_x - min_x
        offset = (canvas_width - tree_width) // 2 - min_x
        for node, (x, y) in self.nodes_positions.items():
            self.nodes_positions[node] = (x + offset, y + self.vertical_offset)

    def _draw_node(self, canvas, node):
        """
        Draws the node (with nodetype and value, if any) and connects it to its children.
        """
        if node not in self.nodes_positions:
            return
        x, y = self.nodes_positions[node]
        text = node.nodetype if node.value is None else f"{node.nodetype}: {node.value}"
        canvas.create_text(x, y, text=text, font=("Arial", 10))
        for child in node.children:
            if isinstance(child, ASTNode):
                if child not in self.nodes_positions:
                    continue
                child_x, child_y = self.nodes_positions[child]
                canvas.create_line(x, y, child_x, child_y)
                self._draw_node(canvas, child)
            else:
                if child in self.nodes_positions:
                    child_x, child_y = self.nodes_positions[child]
                    canvas.create_line(x, y, child_x, child_y)
                    canvas.create_text(child_x, child_y, text=str(child), font=("Arial", 8))

    def draw(self):
        self._calc_positions(self.root_node)
        window = tk.Tk()
        window.title("Syntax Tree (AST)")
        # Maximize the window (using '-zoomed' works on most Linux systems)
        window.attributes('-zoomed', True)
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Create a frame with scrollbars
        frame = tk.Frame(window)
        frame.pack(fill="both", expand=True)
        hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas = tk.Canvas(frame, width=screen_width, height=screen_height, bg="white",
                           xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        canvas.pack(side=tk.LEFT, fill="both", expand=True)
        hbar.config(command=canvas.xview)
        vbar.config(command=canvas.yview)

        self._center_positions(screen_width)
        self._draw_node(canvas, self.root_node)
        canvas.config(scrollregion=canvas.bbox("all"))
        window.mainloop()

if __name__ == '__main__':
    input_text = sys.stdin.read().strip()
    if input_text:
        root = parse_ast(input_text)
    else:
        print("No input has been detected.")
    if root is None:
        print("No tree was found in the input.")
        sys.exit(1)
    drawer = TreeDrawer(root, vertical_offset=70)
    drawer.draw()

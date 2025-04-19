from flask import Flask, render_template, request
from ASTree.astree import ASTNode
from Compiler.parser import parse_input

app = Flask(__name__)

def build_tree_json(node):
    if node is None:
        return None
    name = f"{node.nodetype}"
    if node.value is not None:
        name += f": {node.value}"
    children = []
    for child in node.children:
        if isinstance(child, ASTNode):
            children.append(build_tree_json(child))
        else:
            children.append({"name": str(child)})
    return {"name": name, "children": children}

def clean_code_input(code):
    return ''.join(c for c in code if c.isprintable() or c in '\n\t')

@app.route('/', methods=['GET', 'POST'])
def index():
    tree_data = None
    code_input = ""
    error = None

    if request.method == 'POST':
        code_input = request.form['code']
        code_input = clean_code_input(code_input)
        code_input = code_input.strip()
        code_input = code_input.replace('\r\n', '\n')

        try:
            ast_root = parse_input(code_input)
            if ast_root is not None:
                tree_data = build_tree_json(ast_root)
            else:
                error = "Syntax error. Please check your code."
        except Exception as e:
            error = f"An error occurred: {str(e)}"

    return render_template('index.html', tree_data=tree_data, code=code_input, error=error)

if __name__ == '__main__':
    app.run()

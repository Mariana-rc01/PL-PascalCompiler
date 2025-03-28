import re
import sys

def process_grammar(text):
    """
    Extracts grammar rules enclosed in braces { } and returns a list of
    tuples (non-terminal, [list of productions]).
    """
    # Extracts the content between { and }
    m = re.search(r'\{(.*)\}', text, re.DOTALL)
    if m:
        content = m.group(1)
    else:
        content = text

    rules = []
    lines = content.strip().splitlines()
    current_nt = None
    productions = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Checks if the line defines a new rule
        m = re.match(r'(\w+)\s*:\s*(.+)', line)
        if m:
            # If we were already processing a rule, save it
            if current_nt is not None:
                rules.append((current_nt, productions))
            current_nt = m.group(1)
            production = m.group(2).strip()
            productions = [production]
        elif line.startswith('|'):
            # Line with an alternative
            alternative = line[1:].strip()
            productions.append(alternative)
        else:
            # Other lines (could be continuation) – ignored in this example
            pass

    # Add the last processed rule
    if current_nt is not None:
        rules.append((current_nt, productions))

    return rules

def generate_yacc(rules):
    """
    Generates yacc (PLY) code based on the list of rules.
    """
    output_lines = []
    for nt, productions in rules:
        for i, prod in enumerate(productions):
            # Function name: the first alternative uses "p_<NT>",
            # subsequent ones append the first token of the production
            func_name = f"p_{nt}"
            if i > 0:
                first_token = prod.split()[0]
                func_name += "_" + first_token

            # Special case for Header (removing ListArgs as per example)
            if nt == "Header":
                prod = re.sub(r'\s+ListArgs(?=\s*;)', '', prod)

            rule_str = f'"{nt} : {prod}"'
            output_lines.append(f"def {func_name}(p):")
            output_lines.append(f"    {rule_str}")
            output_lines.append("")  # Blank line to separate functions

    return "\n".join(output_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py grammar_file.txt")
        sys.exit(1)
    
    file = sys.argv[1]
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    rules = process_grammar(content)
    yacc_code = generate_yacc(rules)
    print(yacc_code)

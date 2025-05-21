from Compiler.lex import lexer

def tokenize(code):
    lexer.input(code)
    return [(tok.type, tok.value) for tok in lexer]

def test_program_simple_header():
    code = """
        program HelloWorld;
        begin
        end.
    """
    tokens = tokenize(code)
    expected = [
        ('PROGRAM', 'program'),
        ('identifier', 'HelloWorld'),
        (';', ';'),
        ('BEGIN', 'begin'),
        ('END', 'end'),
        ('.', '.')
    ]
    assert tokens == expected

def test_program_with_parameters():
    code = """
        program HelloWorld(a, b, c);
        begin
        end.
    """
    tokens = tokenize(code)
    expected = [
        ('PROGRAM', 'program'),
        ('identifier', 'HelloWorld'),
        ('(', '('),
        ('identifier', 'a'),
        (',', ','),
        ('identifier', 'b'),
        (',', ','),
        ('identifier', 'c'),
        (')', ')'),
        (';', ';'),
        ('BEGIN', 'begin'),
        ('END', 'end'),
        ('.', '.')
    ]
    assert tokens == expected

def test_variable_declaration():
    code = """
        program P;
        var
            x, y: integer;
        begin
        end.
    """
    tokens = tokenize(code)
    expected = [
        ('PROGRAM', 'program'),
        ('identifier', 'P'),
        (';', ';'),
        ('VAR', 'var'),
        ('identifier', 'x'),
        (',', ','),
        ('identifier', 'y'),
        ('COLON', ':'),
        ('identifier', 'integer'),
        (';', ';'),
        ('BEGIN', 'begin'),
        ('END', 'end'),
        ('.', '.')
    ]
    assert tokens == expected

def test_assignment_statement():
    code = """
        program Teste;
        var
            x: integer;
        begin
            x := 5;
        end.
    """
    tokens = tokenize(code)
    expected = [
        ('PROGRAM', 'program'),
        ('identifier', 'Teste'),
        (';', ';'),
        ('VAR', 'var'),
        ('identifier', 'x'),
        ('COLON', ':'),
        ('identifier', 'integer'),
        (';', ';'),
        ('BEGIN', 'begin'),
        ('identifier', 'x'),
        ('ASSIGN', ':='),
        ('num_int', '5'),
        (';', ';'),
        ('END', 'end'),
        ('.', '.')
    ]
    assert tokens == expected

def test_if_else_statement():
    code = """
        program Teste;
        begin
            if 5 < 10 then x := 1 else x := 0
        end.
    """
    tokens = tokenize(code)
    expected = [
        ('PROGRAM', 'program'),
        ('identifier', 'Teste'),
        (';', ';'),
        ('BEGIN', 'begin'),
        ('IF', 'if'),
        ('num_int', '5'),
        ('LESS_THAN', '<'),
        ('num_int', '10'),
        ('THEN', 'then'),
        ('identifier', 'x'),
        ('ASSIGN', ':='),
        ('num_int', '1'),
        ('ELSE', 'else'),
        ('identifier', 'x'),
        ('ASSIGN', ':='),
        ('num_int', '0'),
        ('END', 'end'),
        ('.', '.')
    ]
    assert tokens == expected

def test_while_statement():
    code = """
        program LoopTest;
        begin
            while x < 10 do x := x + 1
        end.
    """
    tokens = tokenize(code)
    expected = [
        ('PROGRAM', 'program'),
        ('identifier', 'LoopTest'),
        (';', ';'),
        ('BEGIN', 'begin'),
        ('WHILE', 'while'),
        ('identifier', 'x'),
        ('LESS_THAN', '<'),
        ('num_int', '10'),
        ('DO', 'do'),
        ('identifier', 'x'),
        ('ASSIGN', ':='),
        ('identifier', 'x'),
        ('+', '+'),
        ('num_int', '1'),
        ('END', 'end'),
        ('.', '.')
    ]
    assert tokens == expected

def test_for_loop():
    code = """
        program LoopFor;
        begin
            for i := 1 to 10 do x := x + i
        end.
    """
    tokens = tokenize(code)
    expected = [
        ('PROGRAM', 'program'),
        ('identifier', 'LoopFor'),
        (';', ';'),
        ('BEGIN', 'begin'),
        ('FOR', 'for'),
        ('identifier', 'i'),
        ('ASSIGN', ':='),
        ('num_int', '1'),
        ('TO', 'to'),
        ('num_int', '10'),
        ('DO', 'do'),
        ('identifier', 'x'),
        ('ASSIGN', ':='),
        ('identifier', 'x'),
        ('+', '+'),
        ('identifier', 'i'),
        ('END', 'end'),
        ('.', '.')
    ]
    assert tokens == expected

def test_procedure_declaration():
    code = """
        program MyProgram;
        procedure Show;
        begin
        end;
        begin
        end.
    """
    tokens = tokenize(code)
    expected = [
        ('PROGRAM', 'program'),
        ('identifier', 'MyProgram'),
        (';', ';'),
        ('PROCEDURE', 'procedure'),
        ('identifier', 'Show'),
        (';', ';'),
        ('BEGIN', 'begin'),
        ('END', 'end'),
        (';', ';'),
        ('BEGIN', 'begin'),
        ('END', 'end'),
        ('.', '.')
    ]
    assert tokens == expected

def test_comments():
    code = """
        program WithComments; { Comentário }
        begin
            x := 1;
            (* Comentário em duas linhas
               continua aqui *)
            y := 2
        end.
    """
    tokens = tokenize(code)
    expected = [
        ('PROGRAM', 'program'),
        ('identifier', 'WithComments'),
        (';', ';'),
        ('BEGIN', 'begin'),
        ('identifier', 'x'),
        ('ASSIGN', ':='),
        ('num_int', '1'),
        (';', ';'),
        ('identifier', 'y'),
        ('ASSIGN', ':='),
        ('num_int', '2'),
        ('END', 'end'),
        ('.', '.')
    ]
    assert tokens == expected


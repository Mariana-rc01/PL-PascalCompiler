from Compiler.parser import parser
from Compiler.semantic import SemanticAnalyzer

def test_program_simple_header():
    code = """
        program HelloWorld;
        begin
        end.
    """
    analyzer = SemanticAnalyzer()
    result = parser.parse(code)
    assert analyzer.analyze(result) == []
    assert analyzer.errors == []

def test_program_with_parameters():
    code = """
        program HelloWorld(a, b, c);
        begin
        end.
    """
    analyzer = SemanticAnalyzer()
    result = parser.parse(code)
    assert analyzer.analyze(result) == []
    assert analyzer.errors == []

def test_variable_declaration():
    code = """
        program P;
        var
            x, y: integer;
        begin
        end.
    """
    analyzer = SemanticAnalyzer()
    result = parser.parse(code)
    assert analyzer.analyze(result) == []
    assert analyzer.errors == []

def test_assignment_statement():
    code = """
        program Teste;
        var
            x: integer;
        begin
            x := 5;
        end.
    """
    analyzer = SemanticAnalyzer()
    result = parser.parse(code)
    assert analyzer.analyze(result) == []
    assert analyzer.errors == []

def test_if_else_statement():
    code = """
        program Teste;
        var
            x: integer;
        begin
            if 5 < 10 then x := 1 else x := 0
        end.
    """
    analyzer = SemanticAnalyzer()
    result = parser.parse(code)
    assert analyzer.analyze(result) == []
    assert analyzer.errors == []

def test_while_statement():
    code = """
        program LoopTest;
        var
            i, x: integer;
        begin
            while x < 10 do x := x + 1
        end.
    """
    analyzer = SemanticAnalyzer()
    result = parser.parse(code)
    assert analyzer.analyze(result) == []
    assert analyzer.errors == []

def test_for_loop():
    code = """
        program LoopFor;
        var
            i, x: integer;
        begin
            for i := 1 to 10 do x := x + i
        end.
    """
    analyzer = SemanticAnalyzer()
    result = parser.parse(code)
    assert analyzer.analyze(result) == []
    assert analyzer.errors == []

def test_procedure_declaration():
    code = """
        program MyProgram;
        procedure Show;
        begin
        end;
        begin
        end.
    """
    analyzer = SemanticAnalyzer()
    result = parser.parse(code)
    assert analyzer.analyze(result) == []
    assert analyzer.errors == []

def test_function():
    code = """
        program VerifyHello;
        var
            palavra: string;

        function Hello(s: string): boolean;
        begin
            Hello := s = 'Hello';
        end;

        begin
            writeln('Escreve uma palavra:');
            readln(palavra);
            if Hello(palavra) then
                writeln('Disseste Hello!')
            else
                writeln('Não disseste Hello...');
        end.
    """
    analyzer = SemanticAnalyzer()
    result = parser.parse(code)
    assert analyzer.analyze(result) == []
    assert analyzer.errors == []
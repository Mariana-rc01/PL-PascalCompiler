program SomaDoisNumeros;
var
    a, b, resultado: integer;

function Soma(x, y: integer): integer;
begin
    Soma := x + y;
end;

begin
    writeln('Introduza dois números inteiros:');
    readln(a);
    readln(b);
    resultado := Soma(a, b);
    writeln('A soma é: ', resultado);
end.

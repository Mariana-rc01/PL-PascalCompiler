program ParOuImpar;
var
    numero: integer;

procedure VerificarParOuImpar(n: integer);
begin
    if n mod 2 = 0 then
        writeln(n, ' é par.')
    else
        writeln(n, ' é ímpar.');
end;

begin
    writeln('Introduz um número inteiro:');
    readln(numero);
    VerificarParOuImpar(numero);
end.

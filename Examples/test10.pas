program ShowArray;
var
    numeros: array[1..5] of integer;
    i: integer;

procedure Show(valores: array of integer);
var
    j: integer;
begin
    writeln('Elementos do array:');
    for j := 1 to 5 do
        writeln(valores[j]);
end;

begin
    writeln('Insira 5 numeros:');
    for i := 1 to 5 do
        readln(numeros[i]);

    Show(numeros);
end.

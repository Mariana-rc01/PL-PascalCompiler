program BinarioParaInteiro;

var
    bin: string;
    valor: integer;
    a: real;

function BinToInt(bin: string): integer;
var
    i, valor, potencia: integer;
    a: real;
begin
    valor := 0;
    potencia := 1;
    a := 1.1;
    for i := length(bin) downto 1 do
    begin
        if bin[i] = '1' then
        valor := valor + potencia;
        a := potencia / 2;
        writeln(a);
    end;
    BinToInt := valor;
end;

begin
    writeln('Introduza uma string binária:');
    readln(bin);
    valor := BinToInt(bin);
    writeln('O valor inteiro correspondente é: ', valor);
end.
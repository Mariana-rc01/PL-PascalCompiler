program Maior3;
var
    num1, num2, num3, maior: Integer;
begin
    { Ler 3 números }
    Write('Introduza o primeiro número: ');
    ReadLn(num1);

    Write('Introduza o segundo número: ');
    ReadLn(num2);

    Write('Introduza o terceiro número: ');
    ReadLn(num3);

    { Calcular o maior }
    if num1 > num2 then
        maior := num1;

    { Escrever o resultado }
    WriteLn('O maior é: ', maior)
end.
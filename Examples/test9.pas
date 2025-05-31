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

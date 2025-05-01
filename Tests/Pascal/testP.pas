program VendingMachine;

uses crt;

const
  NUM_ITEMS = 3;

type
  TItem = record
    name: string;
    price: real;
  end;

var
  items: array[1..NUM_ITEMS] of TItem;
  choice: integer;
  money, change: real;

begin
  clrscr;
  
  { Serve para definir os produtos disponíveis, o objetivo é só ver como fazer um comentário }
  items[1].name := 'Água'; items[1].price := 1.00;
  items[2].name := 'Fruta'; items[2].price := 1.50;
  items[3].name := 'Cogumelos'; items[3].price := 2.00;
  
  writeln('--- Máquina de Vendas ---');
  writeln('Escolha um produto:');
  for choice := 1 to NUM_ITEMS do
    writeln(choice, ': ', items[choice].name, ' - €', items[choice].price:0:2);
  
  write('Escreve o número do produto desejado: ');
  readln(choice);
  
  if (choice < 1) or (choice > NUM_ITEMS) then
  begin
    writeln('Opção inválida. Tenta novamente.');
    exit;
  end;
  
  writeln('Escolheste: ', items[choice].name);
  write('Insire o dinheiro (€): ');
  readln(money);
  
  if money < items[choice].price then
  begin
    writeln('Dinheiro insuficiente. Operação cancelada.');
    exit;
  end;
  
  change := money - items[choice].price;
  writeln('Compra realizada com sucesso!');
  if change > 0 then
    writeln('O teu troco: €', change:0:2);
  
  writeln('Obrigado por utilizares a máquina de vendas!');
end.

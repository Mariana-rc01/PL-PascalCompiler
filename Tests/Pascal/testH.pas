program MultiFunctional;
uses crt;

function IsPrime(n: integer): boolean;
var
  i: integer;
begin
  if (n < 2) then
    IsPrime := False
  else
  begin
    IsPrime := True;
    for i := 2 to trunc(sqrt(n)) do
      if (n mod i = 0) then
      begin
        IsPrime := False;
        Break;
      end;
  end;
end;

function Factorial(n: integer): longint;
var
  i: integer;
  resultValue: longint;
begin
  resultValue := 1;
  for i := 2 to n do
    resultValue := resultValue * i;
  Factorial := resultValue;
end;

procedure Calculator;
var
  a, b: real;
  opc: char;
begin
  writeln('Enter two numbers:');
  readln(a, b);
  writeln('Choose an operation (+, -, *, /):');
  readln(opc);
  case opc of
    '+': writeln('Result: ', a + b:0:2);
    '-': writeln('Result: ', a - b:0:2);
    '*': writeln('Result: ', a * b:0:2);
    '/': if b <> 0 then
           writeln('Result: ', a / b:0:2)
         else
           writeln('Error: Division by zero!');
  else
    writeln('Invalid operation!');
  end;
end;

var
  option, num: integer;
begin
  repeat
    clrscr;
    writeln('Menu:');
    writeln('1. Calculator');
    writeln('2. Check if a number is prime');
    writeln('3. Calculate factorial');
    writeln('4. Exit');
    writeln('Choose an option:');
    readln(option);

    case option of
      1: Calculator;
      2: begin
           writeln('Enter a number:');
           readln(num);
           if IsPrime(num) then
             writeln(num, ' is prime.')
           else
             writeln(num, ' is not prime.');
         end;
      3: begin
           writeln('Enter a number:');
           readln(num);
           writeln('Factorial of ', num, ' is ', Factorial(num));
         end;
      4: writeln('Exiting...');
    else
      writeln('Invalid option!');
    end;

    writeln('Press ENTER to continue...');
    readln;
  until option = 4;
end.

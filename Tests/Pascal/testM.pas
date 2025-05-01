program BasicPascalExamples;
uses crt, sysutils;
{*
    This is a multi-line comment.
    This is a multi-line comment.
*}

{ This is a single-line comment. }

type
    months = (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec);
    TSeason = (SUMMER, WINTER, SPRING, FALL);
    color = (pink1, pink2, pink3, pink4, pink5);
    car_color = array[color] of boolean;
    TPerson = record
        name: string;
        age: integer;
    end;

var
    a, b, c: real;
    favoriteSeason: TSeason;
    month: months;
    d: integer = 10;
    e: integer = 1;
    car_body: car_color;
    carColorInput: string;
    carColor: color;
    person: TPerson;
    numbers: array[1..5] of integer;
    f: text;
    i: integer;

label labeel;

function calculateTriangleArea(a, b, c: real): real;
var
    p: real;
begin
    p := (a + b + c) / 2;
    calculateTriangleArea := sqrt(p * (p - a) * (p - b) * (p - c));
end;

procedure PrintGreeting;
begin
    writeln('Hello, World!');
end;

procedure ReadPerson(var p: TPerson);
begin
    writeln('Enter name:');
    readln(p.name);
    writeln('Enter age:');
    readln(p.age);
end;

procedure WriteToFile;
begin
    assign(f, 'teste.txt');
    rewrite(f);
    writeln(f, 'This is a test file.');
    close(f);
end;

begin
    PrintGreeting;

    writeln('Calculate triangle area');
    writeln('Insert a, b and c values:');
    readln(a, b, c);
    writeln('The area of the triangle is: ', calculateTriangleArea(a, b, c):0:4);

    writeln('Which season is your favorite? (e.g., SUMMER, WINTER, etc.)');
    readln(favoriteSeason);
    case favoriteSeason of
        SUMMER:
            for month := Jun to Aug do
                writeln('Summer: ', month);
        WINTER:
            begin
                writeln('Winter: ', Dec);
                writeln('Winter: ', Jan);
                writeln('Winter: ', Feb);
            end;
        SPRING:
            for month := Mar to May do
                writeln('Spring: ', month);
        FALL:
            for month := Sep to Nov do
                writeln('Fall: ', month);
    end;

    writeln('Enter the color of the car (pink1, pink2, pink3, pink4, pink5):');
    readln(carColorInput);
    carColorInput := LowerCase(carColorInput);
    if carColorInput = 'pink1' then
        carColor := pink1
    else if carColorInput = 'pink2' then
        carColor := pink2
    else if carColorInput = 'pink3' then
        carColor := pink3
    else if carColorInput = 'pink4' then
        carColor := pink4
    else if carColorInput = 'pink5' then
        carColor := pink5
    else
    begin
        writeln('Invalid color.');
        exit;
    end;

    car_body[carColor] := true;
    writeln('Car color set to: ', carColorInput);

    writeln('Car colors:');
    for carColor := Low(color) to High(color) do
    begin
        if car_body[carColor] then
            writeln(carColor);
    end;

    if d < 20 then
        writeln('d is less than 20')
    else
        writeln('d is not less than 20');
    writeln('value of d is : ', d);

    labeel: repeat
        if e = 1 then
        begin
            e := e + 1;
            goto labeel;
        end;
        writeln('value of e: ', e);
        e := e + 1;
    until e = 3;

    ReadPerson(person);
    writeln('Person name: ', person.name);
    writeln('Person age: ', person.age);

    writeln('Enter 5 numbers:');
    for i := 1 to 5 do
        readln(numbers[i]);
    writeln('You entered:');
    for i := 1 to 5 do
        writeln(numbers[i]);

    WriteToFile;

    writeln('Press any key to exit...');
    readkey;
end.
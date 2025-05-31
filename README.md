# Relatório de Projeto: Compilador de Pascal

**Data:** 01/06/2025 | **Disciplina:** Processamento de Linguagens | **Curso:** Licenciatura em Engenharia Informática

### Autores

| Número | Nome                              |
|--------|-----------------------------------|
| 104100 | Hélder Ricardo Ribeiro Gomes      |
| 90817  | Mariana Rocha Cristino            |
| 104082 | Pedro Figueiredo Pereira          |
---

## Índice

1. [Introdução](#introdução)
2. [Descrição Geral do Projeto](#descrição-geral-do-projeto)
3. [Objetivos](#objetivos)
4. [Análise Léxica](#análise-léxica)
5. [Análise Sintática](#análise-sintática)
6. [Análise Semântica](#análise-semântica)
7. [Geração de Código](#geração-de-código)
8. [Testes](#testes)
9. [Extras](#extras)
10. [Manual de utilização](#manual-de-utilização)
11. [Conclusões](#conclusões)
12. [Referências](#referências)

---

## Introdução

Este relatório apresenta o desenvolvimento de um compilador para a linguagem Pascal. O objetivo principal é explorar os conceitos fundamentais de compiladores, como análise léxica, análise sintática, análise semântica e geração de código máquina. Esses conceitos são essenciais para compreender o funcionamento interno de linguagens de programação e sistemas de tradução de código.

O projeto foi desenvolvido utilizando Python e ferramentas como **PLY (Python Lex-Yacc)**, que facilitaram a implementação das etapas de análise léxica e sintática. A especificação oficial da linguagem Pascal standard foi utilizada como referência para garantir que o compilador estivesse em conformidade com os padrões da linguagem.

## Descrição Geral do Projeto

O compilador desenvolvido neste projeto foi estruturado em diferentes módulos, cada um responsável por uma etapa específica do processo de compilação. A análise léxica identifica os tokens da linguagem, enquanto a análise sintática constrói a árvore abstrata de sintaxe (AST) com base nas regras gramaticais. A análise semântica verifica a validade do código em termos de tipos e escopos, e a geração de código traduz o programa Pascal para uma representação executável.

Além disso, o projeto inclui uma interface gráfica que permite visualizar a AST gerada, facilitando o entendimento do funcionamento interno do compilador. Um conjunto de testes automatizados foi desenvolvido para validar cada etapa do processo, garantindo a robustez e a confiabilidade do sistema.

## Objetivos

Os principais objetivos deste projeto foram:

1. **Explorar os conceitos fundamentais de compiladores**: Implementar as etapas de análise léxica, sintática, semântica e geração de código, compreendendo os desafios e soluções associados a cada uma delas.
2. **Desenvolver um compilador funcional para Pascal**: Garantir que o compilador seja capaz de processar programas escritos em Pascal e gerar uma saída válida.
3. **Criar uma interface gráfica**: Permitir a visualização da AST para auxiliar na depuração e na aprendizagem da estrutura interna do compilador.
4. **Garantir a qualidade do sistema**: Implementar testes automatizados para validar o funcionamento correto de cada módulo do compilador.

## Análise Léxica

A análise léxica é a etapa inicial do processo de compilação, é responsável por ler o código-fonte e por
convertê-lo numa sequência de *tokens*, que são as unidades léxicas básicas da linguagem. Esta fase
tem como principal objetivo identificar e classificar símbolos como palavras-chave, identificadores,
operadores, delimitadores e literais (como números, caracteres e strings), onde os comentários e
espaços em branco são removidos.

No contexto deste projeto, a análise léxica foi implementada utilizando a ferramenta
**PLY (Python Lex-Yacc)**, que permite definir expressões regulares associadas a funções para
reconhecer os diferentes *tokens* da linguagem de Pascal.


O conjunto de *tokens* definidos reflete os elementos sintáticos de Pascal que foram considerados
relevantes para o compilador. Para a sua definição, consultámos a especificação oficial da linguagem
Pascal (ISO 7185:1990), de modo a garantir a conformidade com os padrões da linguagem e a correta
identificação dos constituintes léxicos. A seguir, apresenta-se a especificação dos *tokens*:

```
tokens = [
    PROGRAM, PROCEDURE, FUNCTION, BEGIN, END, FOR, TO, DO, AND, OR,
    IF, THEN, ELSE, DOWNTO, MOD, DIV, NOT, WHILE, VAR, ARRAY, OF,
    TRUE, FALSE,
    identifier, char, string, num_int, num_real,
    ASSIGN, EQUAL, COLON, GREATER_THAN, LESS_THAN, NOT_EQUAL,
    GREATER_THAN_EQUAL, LESS_THAN_EQUAL
]
```

Além dos *tokens* nomeados, foram definidos também os **símbolos literais**, representados
diretamente pelos seus próprios caracteres:

```
literals = [';', ',', '(', ')', '.', '+', '-', '*', '/', '[', ']']
```

Para cada *token*, foi associada uma expressão regular que permite identificar a ocorrência do mesmo
no código-fonte. Palavras-chave são reconhecidas por expressões regulares específicas e têm a sua
classificação fixada (por exemplo, `program`, `var`, `begin`, etc.). Identificadores são definidos
como sequências de letras, dígitos e _underscore_, desde que comecem por uma letra ou pelo _underscore_.

Exemplos de *tokens* definidos:

```python
def t_PROGRAM(t):
    r'\bprogram\b'
    t.type = 'PROGRAM'
    return t

def t_identifier(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_num_real(t):
    r'\d+((\.\d+([eE][+-]?\d+)?)|[eE][+-]?\d+)'
    return t

def t_ASSIGN(t):
    r':='
    return t
```

Também foram implementadas regras para:

1. Ignorar espaços, _tabs_ e quebras de linha (`t_ignore = " \t\n"`);
2. Ignorar comentários, tanto do tipo `(* ... *)` quanto `{ ... }`, que são descartados sem produzir tokens;
3. Lidar com erros léxicos, onde caracteres ilegais são reportados e o cursor de análise é avançado para
continuar o processo e detetar possivelmente mais erros.

A análise léxica é insensível a maiúsculas/minúsculas, como é característico da linguagem Pascal,
configurada com `reflags = re.IGNORECASE`.

Portanto, a definição do analisador léxico garante uma identificação correta dos constituintes léxicos
da linguagem e fornece uma sequência válida de *tokens* para ser posteriormente analisada na fase
seguinte.

## Análise Sintática

A análise sintática constitui uma das fases fundamentais do processo de compilação, sucedendo à
análise léxica. O seu principal objetivo é verificar se a sequência de _tokens_ produzida pelo analisador
léxico forma estruturas válidas segundo as regras sintáticas de Pascal.
Para isso, é utilizada uma **gramática livre de contexto**, a qual descreve formalmente a sintaxe da linguagem.

Assim, apresenta-se a gramática desenvolvida para a linguagem alvo do projeto, estruturada
segundo o formalismo G = (T, N, S, P), onde:

- **S** é o símbolo inicial da gramática;
- **T** representa o conjunto de símbolos terminais (tokens);
- **N** representa o conjunto de símbolos não-terminais;
- **P** é o conjunto de produções sintáticas.

```
S = Program
```

```
T = { PROGRAM, VAR, COLON, OF, PROCEDURE, FUNCTION,
  ARRAY, BEGIN, END, ASSIGN, IF, THEN, ELSE,
  WHILE, DO, FOR, TO, DOWNTO, EQUAL, GREATER_THAN,
  LESS_THAN, NOT_EQUAL, GREATER_THAN_EQUAL,
  LESS_THAN_EQUAL, OR, DIV, MOD, AND, NOT, TRUE, FALSE,
  identifier, string, char, num_int, num_real
  '(',')', ';', ',', '.', '[', ']', '+', '-', '*', '/'
}
```

```
N = {
Program, Header, Content, ListH, Declarations, CompoundStatement,
VariableDeclarationPart, ProcedureDeclarationPart, FunctionDeclarationPart,
ListVarsDeclaration, ElemVarsDeclaration, IdentifierList, Array, ListParametersDeclaration,
ListOfListParameters, ListParameters, ElemParameter, ListStatement,
ListStatementAux, LastStatement, Statement, SimpleStatement, StructeredStatement,
AssignmentStatement, ProcedureStatement, Variable, Expression, ListArgs, Arg,
ConditionalStatement, RepetitiveStatement, IfStatement, WhileStatement,
ForStatement, SimpleExpression, RelationalOperator, Term, SecondPriorityOperator, Sign, Factor,
FirstPriorityOperator, UnsignedConstant, FunctionDesignator,
Constant, UnsignedNumber, ListExpressions
}
```

Seguem-se, de seguida, as regras produções da gramática agrupadas por secções. A gramática define a
estrutura de programas completos, incluindo a declaração principal, definições de variáveis,
procedimentos e funções, bem como comandos compostos e estruturas de controlo de fluxo.
Além disso, contempla as regras necessárias para a construção de expressões aritméticas e booleanas,
respeitando a precedência e associatividade dos operadores.

### 1. Estrutura Global do Programa

```
Program → Header Content '.'

Header  → PROGRAM identifier '(' ListH ')' ';'
        | PROGRAM identifier ';'

ListH   → ListH ',' identifier
        | identifier

Content → Declarations CompoundStatement
```

### 2. Declarações

#### 2.1 Declarações Gerais

```
Declarations → Declarations VariableDeclarationPart
             | Declarations ProcedureDeclarationPart
             | Declarations FunctionDeclarationPart
             | ε
```

#### 2.2 Declarações de Variáveis

```
VariableDeclarationPart → VAR ListVarsDeclaration

ListVarsDeclaration     → ListVarsDeclaration ElemVarsDeclaration ';'
                        | ElemVarsDeclaration ';'

ElemVarsDeclaration     → IdentifierList ':' identifier
                        | IdentifierList ':' Array

Array                   → ARRAY '[' Constant '..' Constant ']' OF identifier

IdentifierList          → IdentifierList ',' identifier
                        | identifier
```

#### 2.3 Declarações de Procedimentos

```
ProcedureDeclarationPart → PROCEDURE identifier ListParametersDeclaration ';' Content ';'
```

#### 2.4 Declarações de Funções

```
FunctionDeclarationPart → FUNCTION identifier ListParametersDeclaration ':' identifier ';' Content ';'
```

### 3. Argumentos de Funções e Procedimentos

```
ListParametersDeclaration → '(' ListOfListParameters ')'
                          | '(' ')'
                          | ε

ListOfListParameters      → ListOfListParameters ';' ListParameters
                          | ListOfListParameters ';' VAR ListParameters
                          | ListParameters
                          | VAR ListParameters

ListParameters            → ListParameters ',' ElemParameter
                          | ElemParameter

ElemParameter             → IdentifierList ':' ARRAY OF identifier
                          | IdentifierList ':' identifier
```

### 4. Comandos Compostos

```
CompoundStatement → BEGIN ListStatement END

ListStatement     → ListStatementAux LastStatement

ListStatementAux  → ListStatementAux Statement ';'
                  | ε

LastStatement     → Statement
                  | ε
```

### 5. Instruções

```
Statement → SimpleStatement
          | StructeredStatement
```

#### 5.1 Instruções Simples

```
SimpleStatement     → AssignmentStatement
                    | ProcedureStatement

AssignmentStatement → Variable ASSIGN Expression

ProcedureStatement  → identifier '(' ListArgs ')'
                    | identifier '(' ')'
                    | identifier

ListArgs            → ListArgs ',' Arg
                    | Arg
Arg                 → Expression
```

#### 5.2 Instruções Estruturadas

```
StructeredStatement → CompoundStatement
                    | ConditionalStatement
                    | RepetitiveStatement
```

### 6. Estruturas de Controlo

#### 6.1 Condicional

```
ConditionalStatement → IfStatement

IfStatement          → IF Expression THEN Statement
                     | IF Expression THEN Statement ELSE Statement
```

#### 6.2 Repetitivas

```
RepetitiveStatement → WhileStatement
                    | ForStatement

WhileStatement      → WHILE Expression DO Statement

ForStatement        → FOR identifier ASSIGN Expression TO Expression DO Statement
                    | FOR identifier ASSIGN Expression DOWNTO Expression DO Statement
```

### 7. Expressões

#### 7.1 Expressão

```
Expression → SimpleExpression RelationalOperator Expression
           | SimpleExpression
```

#### 7.2 Operadores Relacionais

```
RelationalOperator → EQUAL
                   | GREATER_THAN
                   | LESS_THAN
                   | NOT_EQUAL
                   | GREATER_THAN_EQUAL
                   | LESS_THAN_EQUAL
```

#### 7.3 Expressões Simples

```
SimpleExpression → Sign Term SecondPriorityOperator SimpleExpression
                 | Term SecondPriorityOperator SimpleExpression
                 | Term
```

##### Operadores de Segunda Prioridade

```
SecondPriorityOperator → '+'
                       | '-'
                       | OR
```

##### Sinais

```
Sign → '+'
     | '-'
```

#### 7.4 Termos

```
Term → Factor FirstPriorityOperator Term
     | Factor
```

##### Operadores de Primeira Prioridade

```
FirstPriorityOperator → '*'
                      | '/'
                      | DIV
                      | MOD
                      | AND
```

### 8. Fatores

```
Factor → '(' Expression ')'
       | Variable
       | UnsignedConstant
       | FunctionDesignator
       | NOT Factor
       | TRUE
       | FALSE
```

### 9. Designadores de Funções

```
FunctionDesignator → identifier '(' ListArgs ')'
                   | identifier '(' ')'
```

### 10. Constantes e Números

```
UnsignedConstant → UnsignedNumber
                 | string
                 | char

Constant         → num_int
                 | Sign num_int
                 | char

UnsignedNumber   → num_int
                 | num_real
```

### 11. Variáveis

```
Variable        → identifier
                | identifier '[' ListExpressions ']'

ListExpressions → ListExpressions ',' Expression
                | Expression
```

A especificação da gramática foi concebida com o intuito de suportar a geração de um
**analisador sintático top-down**, de modo a ser possível utilizar a ferramenta **PLY** (Python Lex-Yacc).

## Análise Semântica

A **análise semântica** constitui uma etapa essencial no processo de fazer um compilador, esta é
responsável por validar a **correção lógica e contextual** de um programa após a análise sintática.
Esta fase assegura que o código respeita as regras de semântica de Pascal, como
coerência de tipos, existência e escopo de identificadores, chamadas a funções com parâmetros adequados,
entre outros.

A implementação analisada efetua a travessia da **árvore sintática abstrata (AST)**, percorrendo os
seus nodos de forma recursiva e executando verificações semânticas apropriadas a cada tipo de construção.
Durante esta travessia, é mantida uma **tabela de símbolos com suporte a escopos aninhados**, crucial
para a correta gestão de identificadores e respetivos atributos.

### Estrutura e Mecanismos Fundamentais

* **Gestão de Escopos**:
  * Utiliza-se uma estrutura em _stack_ (lista de dicionários) para representar os escopos.
  * Cada entrada na _stack_ corresponde a um novo nível de escopo (p.e., blocos de funções e procedimentos).
  * Esta abordagem permite suportar regras de visibilidade e evitar conflitos de nomes.

* **Despacho Dinâmico por Tipo de Nodo**:
  * O método `_visit` atua como ponto central da travessia da árvore.
  * Determina dinamicamente qual é o método específico a invocar com base no tipo do nodo.
  * Quando não existe um método específico, é feita uma travessia genérica pelos filhos do nodo.

* **Validação de Declarações**:
  * Verifica-se a duplicação de identificadores no mesmo escopo.
  * O registo de funções e procedimentos inclui parâmetros e tipo de retorno (em funções).
  * Os parâmetros são automaticamente introduzidos no escopo local como variáveis.

### Verificações Semânticas Específicas

* **Declaração e Uso de Variáveis**:
  * Suporte a variáveis simples e arrays.
  * Os arrays são validados quanto ao tipo base e limites (inferior e superior), incluindo avaliação de
  expressões constantes.
  * Os arrays de caracteres são tratados como strings, simplificando comparações de tipo.

* **Atribuições**:
  * Verificação de compatibilidade entre o tipo da variável e o tipo da expressão.
  * Compatibilidades implícitas são permitidas (p.e., inteiro para real), mas incompatibilidades explícitas são
  reportadas como erro.

* **Chamadas a Funções e Procedimentos**:
  * Verificação de existência e do tipo do identificador chamado.
  * Comparação do número e do tipo dos argumentos passados com os parâmetros esperados.
  * Tratamento especial para funções/procedimentos embutidos (p.e., `write`, `writeln`, `readln`, `write`),
  incluindo regras específicas:
    * `readln` só aceita variáveis como argumentos.
    * `writeln` aceita múltiplos argumentos de tipos diversos, mas todos devem ser reconhecidos.

* **Instruções de Controlo**:
  * `if` e `while`: a condição deve ser do tipo booleano.
  * `for`: a variável de controlo deve estar previamente declarada e ser do tipo inteiro. Limites devem
  ser compatíveis com expressões inteiras.

* **Resolução de Tipos em Expressões**:
  * O método `_get_expression_type` determina o tipo de expressões aritméticas, relacionais e lógicas.
  * Valida o uso correto de operadores:
    * Operadores aritméticos: `+`, `-`, `*`, `/`, `div`, `mod` requerem operandos numéricos.
    * Operadores lógicos: `and`, `or`, `not` exigem operandos booleanos.
    * Operadores relacionais verificam compatibilidade entre operandos e resultam num tipo booleano.

* **Avaliação de Constantes**:
  * Expressões constantes são avaliadas para permitir validações estáticas (p.e., limites de arrays, literais em `for`).

A análise semântica implementada revela-se **modular, extensível e robusta**, cobrindo os aspetos
essenciais de uma linguagem imperativa com tipagem estática como Pascal.

## Geração de Código

A geração de código constitui a fase final do processo de compilação, onde a **árvore sintática abstrata (AST)**, validada semanticamente, é convertida em código de máquina executável. Este processo envolve a aplicação de um **visit pattern**, que permite percorrer recursivamente a AST, gerando as instruções de máquina correspondentes a cada nó da árvore.

### Visit Pattern

A implementação da geração de código baseia-se num padrão de projeto conhecido como **visit pattern**, que permite a separação da lógica de processamento da estrutura dos dados. Este padrão é aplicado através de um método `_visit` que, consoante o tipo de nó da AST, invoca métodos específicos para cada construção da linguagem. Estes métodos, como `_visit_program`, `_visit_ifstatement` ou `_visit_forstatement`, encapsulam a lógica de geração de código para cada tipo de construção, promovendo assim um código modular e extensível.

### Estruturas Auxiliares

Durante a geração de código, são utilizadas diversas estruturas auxiliares para manter o estado e facilitar a tradução. Conceptualmente, uma tabela de símbolos é mantida para mapear variáveis aos seus endereços de memória, sendo diferenciadas variáveis globais e locais (dentro de funções). Além disso, são geridos contadores para endereçamento de variáveis e funções, bem como mapas para armazenar os tipos de variáveis e limites de arrays.

### Operações Aritméticas e Relacionais

As operações aritméticas e relacionais são traduzidas para as instruções de máquina correspondentes, respeitando a **prioridade das operações**. Assim, operadores de primeira prioridade (como `*`, `/`, `div`, `mod`) são processados antes dos de segunda prioridade (`+`, `-`), e as operações relacionais (`=`, `<`, `>`, etc.) são avaliadas após as aritméticas. Para tal, o gerador de código utiliza uma abordagem recursiva, processando primeiro os operandos e, em seguida, aplicando o operador correspondente.

### Variáveis

As variáveis são geridas através da estrutura que as mapeia para endereços de memória. Durante a geração de código, são emitidas instruções para carregar (`PUSHG` para variáveis globais ou `PUSHL` para variáveis locais) e armazenar (`STOREG` ou `STOREL`) valores nas respetivas posições de memória. A inicialização de variáveis é efetuada no momento da sua declaração, garantindo que todas as variáveis têm um valor definido antes de serem utilizadas.

### Arrays

Os arrays são tratados de forma especial, sendo adaptados os índices para o limite inferior declarado. Para aceder a um elemento de um array, são geradas instruções para calcular o endereço correto, ajustando o índice fornecido pelo limite inferior e carregando o valor correspondente (`LOADN`). A declaração de arrays envolve a alocação de memória suficiente para armazenar todos os elementos, baseando-se no tipo base e nos limites superior e inferior.

### Ciclos

A implementação de ciclos, nomeadamente `for` e `while`, recorre a instruções de salto condicional (`JZ`, `JUMP`) e a rótulos para controlar o fluxo de execução. No caso do ciclo `for`, são geridas as instruções para inicializar a variável de controlo, verificar a condição de continuação e atualizar o valor da variável após cada iteração. Para o ciclo `while`, é verificada a condição no início de cada iteração e efetuado o salto condicional para o final do ciclo caso a condição não seja satisfeita.

### Estruturas de Decisão

As estruturas de decisão, como o `if-then-else`, são traduzidas utilizando instruções de salto condicional (`JZ` para saltar para o bloco `else` caso a condição seja falsa e `JUMP` para saltar para o final da estrutura após o bloco `then`). São gerados rótulos para marcar o início do bloco `else` e o final da estrutura de decisão, garantindo a correta execução do fluxo condicional.

### Implementação de Funções

As funções são geridas através de uma estrutura que mapeia o nome da função ao seu tipo de retorno. Durante a chamada a uma função, são geradas instruções para carregar os argumentos na *stack* e efetuar a chamada (`CALL`). No corpo da função, os parâmetros são tratados como variáveis locais e alcançadas a partir da posição negativa relativa ao *frame pointer*, sendo carregados a partir da *stack* e armazenados nas posições correspondentes. A função termina com uma instrução `RETURN`, que retorna o controlo para o ponto de chamada.

O gerador de código produz assim um conjunto de instruções que, quando executadas, replicam o comportamento do programa Pascal original, convertendo-o numa representação executável que respeita as regras semânticas e sintáticas da linguagem alvo.

## Testes

A implementação do compilador foi acompanhada de uma abordagem sistemática de testes automáticos,
onde foram abrangidos os três componentes principais do processo de compilação:

* Analisador Léxico (*Lexer*)
* Analisador Sintático (*Parser*)
* Analisador Semântico

Os testes foram desenvolvidos com o objetivo principal de garantir correção, robustez e conformidade com a
gramática de Pascal, cobrindo uma variedade de construções léxicas, sintáticas e semânticas.

* Utilização da framework de testes `pytest`, integrado com o módulo `assert`, para verificar automaticamente os resultados.
* Estrutura modular de testes, organizada por componente (`lex`, `parser`, `semantic`), com
reutilização dos mesmos blocos de código para validação cruzada das fases.

### Testes ao Analisador Léxico

Os testes léxicos têm como objetivo validar a correta tokenização de código-fonte Pascal. São utilizados exemplos representativos com diversos elementos da linguagem.

**Características testadas**:
* Reconhecimento de palavras-chave (`program`, `begin`, `end`, `if`, `then`, `else`, `while`, `for`, etc.)
* Identificadores, números inteiros, strings e símbolos especiais (`:=`, `;`, `:`, `+`, `-`, `*`, `(`, `)`, etc.)
* Comentários em diferentes formatos (`{ ... }` e `(* ... *)`)
* Suporte a estruturas de controlo e declarações complexas (ciclos, condições, funções, procedimentos)

**Exemplo resumido de teste léxico**:
```python
def test_program_simple_header():
    code = "program HelloWorld; begin end."
    tokens = tokenize(code)
    expected = [
        ('PROGRAM', 'program'),
        ('identifier', 'HelloWorld'),
        (';', ';'),
        ('BEGIN', 'begin'),
        ('END', 'end'),
        ('.', '.')
    ]
    assert tokens == expected
```

### Testes ao Analisador Sintático

O parser utiliza uma gramática LL baseada no `PLY` para construir a Árvore Sintática Abstrata
(**AST**) a partir dos tokens.

**Objetivos dos testes sintáticos**:
* Verificar que a estrutura da árvore sintática gerada corresponde à estrutura esperada da linguagem.
* Confirmar que elementos opcionais (e.g., parâmetros, declarações) são corretamente representados com `None` ou nós específicos.
* Testar a robustez da parser face a diferentes níveis de complexidade do código.

**Exemplo resumido de teste sintático**:
```python
def test_program_simple_header():
    code = "program HelloWorld; begin end."
    result = parser.parse(code)
    expected = ASTNode("Program", [
        ASTNode("Header", [ASTNode("Identifier", [ASTNode("HelloWorld")])]),
        ASTNode("Content", [
            None,
            ASTNode("CompoundStatement", [
                ASTNode("ListStatement", [None, None])
            ])
        ])
    ])
    assert result == expected
```

Os testes sintáticos reutilizam os mesmos fragmentos de código que os testes léxicos, assegurando consistência entre fases.

### Testes à Análise Semântica

A fase de análise semântica introduz verificações adicionais sobre a coerência lógica e contextual do programa.

**Objetivos principais**:
* Garantir que variáveis, funções e procedimentos são declarados antes de serem utilizados.
* Confirmar compatibilidade de tipos em atribuições, expressões e chamadas de função.
* Validar estruturas de controlo como `for`, `if`, `while`, assegurando requisitos semânticos (e.g., condição booleana).

**Estrutura dos testes semânticos**:
* Cada teste invoca o parser para gerar a AST.
* A AST é passada ao `SemanticAnalyzer`, que efetua a verificação.
* A ausência de erros semânticos é verificada com:

  ```python
  assert analyzer.analyze(result) == []
  assert analyzer.errors == []
  ```

**Exemplo simplificado**:
```python
def test_program_with_parameters():
    code = "program HelloWorld(a, b, c); begin end."
    analyzer = SemanticAnalyzer()
    result = parser.parse(code)
    assert analyzer.analyze(result) == []
    assert analyzer.errors == []
```

Os testes cobrem:
1. Declaração de variáveis simples e compostas
2. Atribuições e expressões aritméticas/lógicas
3. Estruturas de controlo (`if-then-else`, `while`, `for`)
4. Subprogramas: `procedure` e `function`, com e sem parâmetros
5. Interação com funções integradas (`readln`, `writeln`)
6. Tratamento de comentários e literais

## Extras

### Árvore AST

### Interface gráfica

## Manual de utilização

### Parser

```bash
python3 -m Compiler.parser < Tests/testN.pas
```

### Tree_Drawer

```bash
python3 -m Compiler.parser < Tests/testN.pas | python3 -m ASTree.tree_drawer
```

### App

```bash
python3 -m ASTree.app
```

## Conclusões

O desenvolvimento deste compilador para a linguagem Pascal permitiu uma exploração aprofundada dos conceitos fundamentais de processamento de linguagens, como análise léxica, análise sintática, análise semântica e geração de código. A utilização de ferramentas, como Python e PLY, facilitou a implementação e demonstrou eficácia.

Além disso, a inclusão de uma interface gráfica para visualização da árvore abstrata de sintaxe (AST) e a criação de um conjunto de testes automatizados contribuíram para a robustez e usabilidade do projeto. Esses elementos não apenas garantiram a qualidade do sistema, mas também proporcionaram uma experiência prática enriquecedora no desenvolvimento de compiladores.

Por fim, este projeto destacou os desafios inerentes ao processo de compilação e as soluções adotadas para superá-los, aprofundando o funcionamento interno de linguagens de programação.

## Referências

- Enunciado do Projeto (PL).
- [Máquina virtual EWVM](https://ewvm.epl.di.uminho.pt/)
- [Pascal ISO 7185:1990](https://www.cs.bilkent.edu.tr/~guvenir/courses/CS315/iso7185pascal.pdf)
- Sebenta de Processamento de Linguagens Reconhecedores Sintáticos, José João Almeida e José Bernardo Barros

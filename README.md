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

## Descrição Geral do Projeto

## Objetivos

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

## Testes

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

## Referências

- Enunciado do Projeto (PL).
- [Máquina virtual EWVM](https://ewvm.epl.di.uminho.pt/)
- [Pascal ISO 7185:1990](https://www.cs.bilkent.edu.tr/~guvenir/courses/CS315/iso7185pascal.pdf)
- Sebenta de Processamento de Linguagens Reconhecedores Sintáticos, José João Almeida e José Bernardo Barros

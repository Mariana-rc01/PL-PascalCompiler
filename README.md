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

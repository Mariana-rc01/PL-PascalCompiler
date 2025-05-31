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

O desenvolvimento deste compilador para a linguagem Pascal permitiu uma exploração aprofundada dos conceitos fundamentais de processamento de linguagens, como análise léxica, análise sintática, análise semântica e geração de código. A utilização de ferramentas, como Python e PLY, facilitou a implementação e demonstrou eficácia.

Além disso, a inclusão de uma interface gráfica para visualização da árvore abstrata de sintaxe (AST) e a criação de um conjunto de testes automatizados contribuíram para a robustez e usabilidade do projeto. Esses elementos não apenas garantiram a qualidade do sistema, mas também proporcionaram uma experiência prática enriquecedora no desenvolvimento de compiladores.

Por fim, este projeto destacou os desafios inerentes ao processo de compilação e as soluções adotadas para superá-los, aprofundando o funcionamento interno de linguagens de programação.

## Referências

- Enunciado do Projeto (PL).
- [Máquina virtual EWVM](https://ewvm.epl.di.uminho.pt/)
- [Pascal ISO 7185:1990](https://www.cs.bilkent.edu.tr/~guvenir/courses/CS315/iso7185pascal.pdf)
- Sebenta de Processamento de Linguagens Reconhecedores Sintáticos, José João Almeida e José Bernardo Barros

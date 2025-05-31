from Compiler.parser import parser
from ASTree.astree import ASTNode

def test_program_simple_header():
    code = """
        program HelloWorld;
        begin
        end.
    """
    result = parser.parse(code)
    expected = ASTNode("Program", [
        ASTNode("Header", [
            ASTNode("Identifier", [ASTNode("HelloWorld")])]),
        ASTNode("Content", [ None,
            ASTNode("CompoundStatement", [
                ASTNode("ListStatement", [None, None])
            ])
        ])
    ])
    assert result == expected

def test_program_with_parameters():
    code = """
        program HelloWorld(a, b, c);
        begin
        end.
    """
    result = parser.parse(code)
    expected = ASTNode("Program", [
        ASTNode("Header", [
            ASTNode("Identifier", ["HelloWorld"]),
            ASTNode("IdentifierList", [
                ASTNode("Identifier", ["a"]),
                ASTNode("Identifier", ["b"]),
                ASTNode("Identifier", ["c"])
            ])
        ]),
        ASTNode("Content", [
            None,
            ASTNode("CompoundStatement", [
                ASTNode("ListStatement", [None, None])
            ])
        ])
    ])

    assert result == expected

def test_variable_declaration():
    code = """
    program P;
    var
        x, y: integer;
    begin
    end.
    """
    result = parser.parse(code)
    expected = ASTNode("Program", [
        ASTNode("Header", [ASTNode("Identifier", [ASTNode("P")])]),
        ASTNode("Content", [
            ASTNode("Declarations", [
                None,
                ASTNode("VarDeclaration", [
                    ASTNode("ListVarDeclaration", [
                        ASTNode("VarElemDeclaration", [
                            ASTNode("IdentifierList", [
                                ASTNode("Identifier", [ASTNode("x")]),
                                ASTNode("Identifier", [ASTNode("y")])
                            ]),
                            ASTNode("Type", [ASTNode("integer")])
                        ])
                    ])
                ])
            ]),
            ASTNode("CompoundStatement", [
                ASTNode("ListStatement", [None, None])
            ])
        ])
    ])
    assert result == expected

def test_assignment_statement():
    code = """
    program Teste;
    var
        x: integer;
    begin
        x := 5;
    end.
    """

    result = parser.parse(code)

    expected = ASTNode('Program', [
        ASTNode('Header', [
            ASTNode('Identifier', [
                ASTNode('Teste', [])
            ])
        ]),
        ASTNode('Content', [
            ASTNode('Declarations', [
                None,
                ASTNode('VarDeclaration', [
                    ASTNode('ListVarDeclaration', [
                        ASTNode('VarElemDeclaration', [
                            ASTNode('IdentifierList', [
                                ASTNode('Identifier', [
                                    ASTNode('x', [])
                                ])
                            ]),
                            ASTNode('Type', [
                                ASTNode('integer', [])
                            ])
                        ])
                    ])
                ])
            ]),
            ASTNode('CompoundStatement', [
                ASTNode('ListStatement', [
                    ASTNode('ListStatementAux', [
                        None,
                        ASTNode('Statement', [
                            ASTNode('SimpleStatement', [
                                ASTNode('Assignment', [
                                    ASTNode('Variable', [
                                        ASTNode('Identifier', ['x'])
                                    ]),
                                    ASTNode('Expression', [
                                        ASTNode('SimpleExpression', [
                                            ASTNode('Term', [
                                                ASTNode('Factor', [
                                                    ASTNode('UnsignedConstant', [
                                                        ASTNode('Num_Int', ['5'])
                                                    ])
                                                ])
                                            ])
                                        ])
                                    ])
                                ])
                            ])
                        ])
                    ]),
                    None
                ])
            ])
        ])
    ])

    assert result == expected


def test_if_else_statement():
    code = """
    program Teste;
    var
        x: integer;
    begin
        if 5 < 10 then x := 1 else x := 0
    end.
    """
    result = parser.parse(code)
    expected = ASTNode(
        'Program', [
            ASTNode(
                'Header', [
                    ASTNode(
                        'Identifier', [
                            ASTNode('Teste', [])
                        ]
                    )
                ]
            ),
            ASTNode(
                'Content', [
                    ASTNode(
                        'Declarations', [
                            None,
                            ASTNode(
                                'VarDeclaration', [
                                    ASTNode(
                                        'ListVarDeclaration', [
                                            ASTNode(
                                                'VarElemDeclaration', [
                                                    ASTNode(
                                                        'IdentifierList', [
                                                            ASTNode('Identifier', [ASTNode('x', [])])
                                                        ]
                                                    ),
                                                    ASTNode('Type', [ASTNode('integer', [])])
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    ASTNode(
                        'CompoundStatement', [
                            ASTNode(
                                'ListStatement', [
                                    None,
                                    ASTNode(
                                        'LastStatement', [
                                            ASTNode(
                                                'Statement', [
                                                    ASTNode(
                                                        'StructeredStatement', [
                                                            ASTNode(
                                                                'ConditionalStatement', [
                                                                    ASTNode(
                                                                        'IfStatement', [
                                                                            ASTNode(
                                                                                'Expression', [
                                                                                    ASTNode(
                                                                                        'SimpleExpression', [
                                                                                            ASTNode(
                                                                                                'Term', [
                                                                                                    ASTNode(
                                                                                                        'Factor', [
                                                                                                            ASTNode(
                                                                                                                'UnsignedConstant', [
                                                                                                                    ASTNode('Num_Int', ['5'])
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    ),
                                                                                    ASTNode(
                                                                                        'Operator', [
                                                                                            ASTNode('RelationalOperator', ['<'])
                                                                                        ]
                                                                                    ),
                                                                                    ASTNode(
                                                                                        'Expression', [
                                                                                            ASTNode(
                                                                                                'SimpleExpression', [
                                                                                                    ASTNode(
                                                                                                        'Term', [
                                                                                                            ASTNode(
                                                                                                                'Factor', [
                                                                                                                    ASTNode(
                                                                                                                        'UnsignedConstant', [
                                                                                                                            ASTNode('Num_Int', ['10'])
                                                                                                                        ]
                                                                                                                    )
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            ),
                                                                            ASTNode(
                                                                                'Statement', [
                                                                                    ASTNode(
                                                                                        'SimpleStatement', [
                                                                                            ASTNode(
                                                                                                'Assignment', [
                                                                                                    ASTNode(
                                                                                                        'Variable', [
                                                                                                            ASTNode('Identifier', ['x'])
                                                                                                        ]
                                                                                                    ),
                                                                                                    ASTNode(
                                                                                                        'Expression', [
                                                                                                            ASTNode(
                                                                                                                'SimpleExpression', [
                                                                                                                    ASTNode(
                                                                                                                        'Term', [
                                                                                                                            ASTNode(
                                                                                                                                'Factor', [
                                                                                                                                    ASTNode(
                                                                                                                                        'UnsignedConstant', [
                                                                                                                                            ASTNode('Num_Int', ['1'])
                                                                                                                                        ]
                                                                                                                                    )
                                                                                                                                ]
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    )
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            ),
                                                                            ASTNode(
                                                                                'Statement', [
                                                                                    ASTNode(
                                                                                        'SimpleStatement', [
                                                                                            ASTNode(
                                                                                                'Assignment', [
                                                                                                    ASTNode(
                                                                                                        'Variable', [
                                                                                                            ASTNode('Identifier', ['x'])
                                                                                                        ]
                                                                                                    ),
                                                                                                    ASTNode(
                                                                                                        'Expression', [
                                                                                                            ASTNode(
                                                                                                                'SimpleExpression', [
                                                                                                                    ASTNode(
                                                                                                                        'Term', [
                                                                                                                            ASTNode(
                                                                                                                                'Factor', [
                                                                                                                                    ASTNode(
                                                                                                                                        'UnsignedConstant', [
                                                                                                                                            ASTNode('Num_Int', ['0'])
                                                                                                                                        ]
                                                                                                                                    )
                                                                                                                                ]
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    )
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    assert result == expected


def test_while_statement():
    code = """
    program LoopTest;
    var
        i, x: integer;
    begin
        while x < 10 do x := x + 1
    end.
    """
    result = parser.parse(code)
    expected = ASTNode(
        'Program', [
            ASTNode(
                'Header', [
                    ASTNode(
                        'Identifier', [
                            ASTNode('LoopTest', [])
                        ]
                    )
                ]
            ),
            ASTNode(
                'Content', [
                    ASTNode(
                        'Declarations', [
                            None,
                            ASTNode(
                                'VarDeclaration', [
                                    ASTNode(
                                        'ListVarDeclaration', [
                                            ASTNode(
                                                'VarElemDeclaration', [
                                                    ASTNode(
                                                        'IdentifierList', [
                                                            ASTNode('Identifier', [ASTNode('i', [])]),
                                                            ASTNode('Identifier', [ASTNode('x', [])])
                                                        ]
                                                    ),
                                                    ASTNode('Type', [ASTNode('integer', [])])
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    ASTNode(
                        'CompoundStatement', [
                            ASTNode(
                                'ListStatement', [
                                    None,
                                    ASTNode(
                                        'LastStatement', [
                                            ASTNode(
                                                'Statement', [
                                                    ASTNode(
                                                        'StructeredStatement', [
                                                            ASTNode(
                                                                'RepetitiveStatement', [
                                                                    ASTNode(
                                                                        'WhileStatement', [
                                                                            ASTNode(
                                                                                'Expression', [
                                                                                    ASTNode(
                                                                                        'SimpleExpression', [
                                                                                            ASTNode(
                                                                                                'Term', [
                                                                                                    ASTNode(
                                                                                                        'Factor', [
                                                                                                            ASTNode(
                                                                                                                'Variable', [
                                                                                                                    ASTNode('Identifier', ['x'])
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    ),
                                                                                    ASTNode(
                                                                                        'Operator', [
                                                                                            ASTNode('RelationalOperator', ['<'])
                                                                                        ]
                                                                                    ),
                                                                                    ASTNode(
                                                                                        'Expression', [
                                                                                            ASTNode(
                                                                                                'SimpleExpression', [
                                                                                                    ASTNode(
                                                                                                        'Term', [
                                                                                                            ASTNode(
                                                                                                                'Factor', [
                                                                                                                    ASTNode(
                                                                                                                        'UnsignedConstant', [
                                                                                                                            ASTNode('Num_Int', ['10'])
                                                                                                                        ]
                                                                                                                    )
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            ),
                                                                            'Do',
                                                                            ASTNode(
                                                                                'Statement', [
                                                                                    ASTNode(
                                                                                        'SimpleStatement', [
                                                                                            ASTNode(
                                                                                                'Assignment', [
                                                                                                    ASTNode(
                                                                                                        'Variable', [
                                                                                                            ASTNode('Identifier', ['x'])
                                                                                                        ]
                                                                                                    ),
                                                                                                    ASTNode(
                                                                                                        'Expression', [
                                                                                                            ASTNode(
                                                                                                                'SimpleExpression', [
                                                                                                                    ASTNode(
                                                                                                                        'Term', [
                                                                                                                            ASTNode(
                                                                                                                                'Factor', [
                                                                                                                                    ASTNode(
                                                                                                                                        'Variable', [
                                                                                                                                            ASTNode('Identifier', ['x'])
                                                                                                                                        ]
                                                                                                                                    )
                                                                                                                                ]
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    ),
                                                                                                                    ASTNode(
                                                                                                                        'Operator', [
                                                                                                                            ASTNode('SecondPriorityOperator', ['+'])
                                                                                                                        ]
                                                                                                                    ),
                                                                                                                    ASTNode(
                                                                                                                        'SimpleExpression', [
                                                                                                                            ASTNode(
                                                                                                                                'Term', [
                                                                                                                                    ASTNode(
                                                                                                                                        'Factor', [
                                                                                                                                            ASTNode(
                                                                                                                                                'UnsignedConstant', [
                                                                                                                                                    ASTNode('Num_Int', ['1'])
                                                                                                                                                ]
                                                                                                                                            )
                                                                                                                                        ]
                                                                                                                                    )
                                                                                                                                ]
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    )
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    assert result == expected


def test_for_loop():
    code = """
        program LoopFor;
        var
            i, x: integer;
        begin
            for i := 1 to 10 do x := x + i
        end.
    """
    result = parser.parse(code)
    expected = ASTNode(
        'Program', [
            ASTNode(
                'Header', [
                    ASTNode(
                        'Identifier', [
                            ASTNode('LoopFor', [])
                        ]
                    )
                ]
            ),
            ASTNode(
                'Content', [
                    ASTNode(
                        'Declarations', [
                            None,
                            ASTNode(
                                'VarDeclaration', [
                                    ASTNode(
                                        'ListVarDeclaration', [
                                            ASTNode(
                                                'VarElemDeclaration', [
                                                    ASTNode(
                                                        'IdentifierList', [
                                                            ASTNode('Identifier', [ASTNode('i', [])]),
                                                            ASTNode('Identifier', [ASTNode('x', [])])
                                                        ]
                                                    ),
                                                    ASTNode('Type', [ASTNode('integer', [])])
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    ASTNode(
                        'CompoundStatement', [
                            ASTNode(
                                'ListStatement', [
                                    None,
                                    ASTNode(
                                        'LastStatement', [
                                            ASTNode(
                                                'Statement', [
                                                    ASTNode(
                                                        'StructeredStatement', [
                                                            ASTNode(
                                                                'RepetitiveStatement', [
                                                                    ASTNode(
                                                                        'ForStatement', [
                                                                            ASTNode('Identifier', [ASTNode('i', [])]),
                                                                            'Assign',
                                                                            ASTNode(
                                                                                'Expression', [
                                                                                    ASTNode(
                                                                                        'SimpleExpression', [
                                                                                            ASTNode(
                                                                                                'Term', [
                                                                                                    ASTNode(
                                                                                                        'Factor', [
                                                                                                            ASTNode(
                                                                                                                'UnsignedConstant', [
                                                                                                                    ASTNode('Num_Int', ['1'])
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            ),
                                                                            'To',
                                                                            ASTNode(
                                                                                'Expression', [
                                                                                    ASTNode(
                                                                                        'SimpleExpression', [
                                                                                            ASTNode(
                                                                                                'Term', [
                                                                                                    ASTNode(
                                                                                                        'Factor', [
                                                                                                            ASTNode(
                                                                                                                'UnsignedConstant', [
                                                                                                                    ASTNode('Num_Int', ['10'])
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            ),
                                                                            'Do',
                                                                            ASTNode(
                                                                                'Statement', [
                                                                                    ASTNode(
                                                                                        'SimpleStatement', [
                                                                                            ASTNode(
                                                                                                'Assignment', [
                                                                                                    ASTNode(
                                                                                                        'Variable', [
                                                                                                            ASTNode('Identifier', ['x'])
                                                                                                        ]
                                                                                                    ),
                                                                                                    ASTNode(
                                                                                                        'Expression', [
                                                                                                            ASTNode(
                                                                                                                'SimpleExpression', [
                                                                                                                    ASTNode(
                                                                                                                        'Term', [
                                                                                                                            ASTNode(
                                                                                                                                'Factor', [
                                                                                                                                    ASTNode(
                                                                                                                                        'Variable', [
                                                                                                                                            ASTNode('Identifier', ['x'])
                                                                                                                                        ]
                                                                                                                                    )
                                                                                                                                ]
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    ),
                                                                                                                    ASTNode(
                                                                                                                        'Operator', [
                                                                                                                            ASTNode('SecondPriorityOperator', ['+'])
                                                                                                                        ]
                                                                                                                    ),
                                                                                                                    ASTNode(
                                                                                                                        'SimpleExpression', [
                                                                                                                            ASTNode(
                                                                                                                                'Term', [
                                                                                                                                    ASTNode(
                                                                                                                                        'Factor', [
                                                                                                                                            ASTNode(
                                                                                                                                                'Variable', [
                                                                                                                                                    ASTNode('Identifier', ['i'])
                                                                                                                                                ]
                                                                                                                                            )
                                                                                                                                        ]
                                                                                                                                    )
                                                                                                                                ]
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    )
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    assert result == expected


def test_procedure_declaration():
    code = """
    program MyProgram;
    procedure Show;
    begin
    end;
    begin
    end.
    """
    result = parser.parse(code)
    expected = ASTNode(
        'Program', [
            ASTNode(
                'Header', [
                    ASTNode(
                        'Identifier', [
                            ASTNode('MyProgram', [])
                        ]
                    )
                ]
            ),
            ASTNode(
                'Content', [
                    ASTNode(
                        'Declarations', [
                            None,
                            ASTNode(
                                'ProcedureDeclaration', [
                                    ASTNode('Identifier', ['Show']),
                                    None,
                                    ASTNode(
                                        'Content', [
                                            None,
                                            ASTNode(
                                                'CompoundStatement', [
                                                    ASTNode(
                                                        'ListStatement', [
                                                            None,
                                                            None
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    ASTNode(
                        'CompoundStatement', [
                            ASTNode(
                                'ListStatement', [
                                    None,
                                    None
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    assert result == expected

def test_function():
    code = """
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
    """
    result = parser.parse(code)
    expected = ASTNode(
        'Program', [
            ASTNode(
                'Header', [
                    ASTNode(
                        'Identifier', [
                            ASTNode('VerifyHello', [])
                        ]
                    )
                ]
            ),
            ASTNode(
                'Content', [
                    ASTNode(
                        'Declarations', [
                            ASTNode(
                                'Declarations', [
                                    None,
                                    ASTNode(
                                        'VarDeclaration', [
                                            ASTNode(
                                                'ListVarDeclaration', [
                                                    ASTNode(
                                                        'VarElemDeclaration', [
                                                            ASTNode(
                                                                'IdentifierList', [
                                                                    ASTNode(
                                                                        'Identifier', [
                                                                            ASTNode('palavra', [])
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            ASTNode(
                                                                'Type', [
                                                                    ASTNode('string', [])
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            ),
                            ASTNode(
                                'FunctionDeclaration', [
                                    ASTNode('Identifier', ['Hello']),
                                    ASTNode(
                                        'ListParametersDeclaration', [
                                            ASTNode(
                                                'Parameters', [
                                                    ASTNode(
                                                        'Parameter', [
                                                            ASTNode(
                                                                'IdentifierList', [
                                                                    ASTNode(
                                                                        'Identifier', [
                                                                            ASTNode('s', [])
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            ASTNode('Type', ['string'])
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    ASTNode('ReturnType', ['boolean']),
                                    ASTNode(
                                        'Content', [
                                            None,
                                            ASTNode(
                                                'CompoundStatement', [
                                                    ASTNode(
                                                        'ListStatement', [
                                                            ASTNode(
                                                                'ListStatementAux', [
                                                                    None,
                                                                    ASTNode(
                                                                        'Statement', [
                                                                            ASTNode(
                                                                                'SimpleStatement', [
                                                                                    ASTNode(
                                                                                        'Assignment', [
                                                                                            ASTNode(
                                                                                                'Variable', [
                                                                                                    ASTNode('Identifier', ['Hello'])
                                                                                                ]
                                                                                            ),
                                                                                            ASTNode(
                                                                                                'Expression', [
                                                                                                    ASTNode(
                                                                                                        'SimpleExpression', [
                                                                                                            ASTNode(
                                                                                                                'Term', [
                                                                                                                    ASTNode(
                                                                                                                        'Factor', [
                                                                                                                            ASTNode(
                                                                                                                                'Variable', [
                                                                                                                                    ASTNode('Identifier', ['s'])
                                                                                                                                ]
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    )
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    ),
                                                                                                    ASTNode(
                                                                                                        'Operator', [
                                                                                                            ASTNode('RelationalOperator', ['='])
                                                                                                        ]
                                                                                                    ),
                                                                                                    ASTNode(
                                                                                                        'Expression', [
                                                                                                            ASTNode(
                                                                                                                'SimpleExpression', [
                                                                                                                    ASTNode(
                                                                                                                        'Term', [
                                                                                                                            ASTNode(
                                                                                                                                'Factor', [
                                                                                                                                    ASTNode(
                                                                                                                                        'UnsignedConstant', [
                                                                                                                                            ASTNode('String', ['Hello'])
                                                                                                                                        ]
                                                                                                                                    )
                                                                                                                                ]
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    )
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                            None
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    ASTNode(
                        'CompoundStatement', [
                            ASTNode(
                                'ListStatement', [
                                    ASTNode(
                                        'ListStatementAux', [
                                            ASTNode(
                                                'ListStatementAux', [
                                                    ASTNode(
                                                        'ListStatementAux', [
                                                            None,
                                                            ASTNode(
                                                                'Statement', [
                                                                    ASTNode(
                                                                        'SimpleStatement', [
                                                                            ASTNode(
                                                                                'ProcedureCall', [
                                                                                    ASTNode(
                                                                                        'Identifier', [
                                                                                            ASTNode('writeln', [])
                                                                                        ]
                                                                                    ),
                                                                                    ASTNode(
                                                                                        'ListArgs', [
                                                                                            ASTNode(
                                                                                                'Arg', [
                                                                                                    ASTNode(
                                                                                                        'Expression', [
                                                                                                            ASTNode(
                                                                                                                'SimpleExpression', [
                                                                                                                    ASTNode(
                                                                                                                        'Term', [
                                                                                                                            ASTNode(
                                                                                                                                'Factor', [
                                                                                                                                    ASTNode(
                                                                                                                                        'UnsignedConstant', [
                                                                                                                                            ASTNode('String', ['Escreve uma palavra:'])
                                                                                                                                        ]
                                                                                                                                    )
                                                                                                                                ]
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    )
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                    ASTNode(
                                                        'Statement', [
                                                            ASTNode(
                                                                'SimpleStatement', [
                                                                    ASTNode(
                                                                        'ProcedureCall', [
                                                                            ASTNode(
                                                                                'Identifier', [
                                                                                    ASTNode('readln', [])
                                                                                ]
                                                                            ),
                                                                            ASTNode(
                                                                                'ListArgs', [
                                                                                    ASTNode(
                                                                                        'Arg', [
                                                                                            ASTNode(
                                                                                                'Expression', [
                                                                                                    ASTNode(
                                                                                                        'SimpleExpression', [
                                                                                                            ASTNode(
                                                                                                                'Term', [
                                                                                                                    ASTNode(
                                                                                                                        'Factor', [
                                                                                                                            ASTNode(
                                                                                                                                'Variable', [
                                                                                                                                    ASTNode('Identifier', ['palavra'])
                                                                                                                                ]
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    )
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            ),
                                            ASTNode(
                                                'Statement', [
                                                    ASTNode(
                                                        'StructeredStatement', [
                                                            ASTNode(
                                                                'ConditionalStatement', [
                                                                    ASTNode(
                                                                        'IfStatement', [
                                                                            ASTNode(
                                                                                'Expression', [
                                                                                    ASTNode(
                                                                                        'SimpleExpression', [
                                                                                            ASTNode(
                                                                                                'Term', [
                                                                                                    ASTNode(
                                                                                                        'Factor', [
                                                                                                            ASTNode(
                                                                                                                'FunctionCall', [
                                                                                                                    ASTNode(
                                                                                                                        'Identifier', [
                                                                                                                            ASTNode('Hello', [])
                                                                                                                        ]
                                                                                                                    ),
                                                                                                                    ASTNode(
                                                                                                                        'ListArgs', [
                                                                                                                            ASTNode(
                                                                                                                                'Arg', [
                                                                                                                                    ASTNode(
                                                                                                                                        'Expression', [
                                                                                                                                            ASTNode(
                                                                                                                                                'SimpleExpression', [
                                                                                                                                                    ASTNode(
                                                                                                                                                        'Term', [
                                                                                                                                                            ASTNode(
                                                                                                                                                                'Factor', [
                                                                                                                                                                    ASTNode(
                                                                                                                                                                        'Variable', [
                                                                                                                                                                            ASTNode('Identifier', ['palavra'])
                                                                                                                                                                        ]
                                                                                                                                                                    )
                                                                                                                                                                ]
                                                                                                                                                            )
                                                                                                                                                        ]
                                                                                                                                                    )
                                                                                                                                                ]
                                                                                                                                            )
                                                                                                                                        ]
                                                                                                                                    )
                                                                                                                                ]
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    )
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            ),
                                                                            ASTNode(
                                                                                'Statement', [
                                                                                    ASTNode(
                                                                                        'SimpleStatement', [
                                                                                            ASTNode(
                                                                                                'ProcedureCall', [
                                                                                                    ASTNode(
                                                                                                        'Identifier', [
                                                                                                            ASTNode('writeln', [])
                                                                                                        ]
                                                                                                    ),
                                                                                                    ASTNode(
                                                                                                        'ListArgs', [
                                                                                                            ASTNode(
                                                                                                                'Arg', [
                                                                                                                    ASTNode(
                                                                                                                        'Expression', [
                                                                                                                            ASTNode(
                                                                                                                                'SimpleExpression', [
                                                                                                                                    ASTNode(
                                                                                                                                        'Term', [
                                                                                                                                            ASTNode(
                                                                                                                                                'Factor', [
                                                                                                                                                    ASTNode(
                                                                                                                                                        'UnsignedConstant', [
                                                                                                                                                            ASTNode('String', ['Disseste Hello!'])
                                                                                                                                                        ]
                                                                                                                                                    )
                                                                                                                                                ]
                                                                                                                                            )
                                                                                                                                        ]
                                                                                                                                    )
                                                                                                                                ]
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    )
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            ),
                                                                            ASTNode(
                                                                                'Statement', [
                                                                                    ASTNode(
                                                                                        'SimpleStatement', [
                                                                                            ASTNode(
                                                                                                'ProcedureCall', [
                                                                                                    ASTNode(
                                                                                                        'Identifier', [
                                                                                                            ASTNode('writeln', [])
                                                                                                        ]
                                                                                                    ),
                                                                                                    ASTNode(
                                                                                                        'ListArgs', [
                                                                                                            ASTNode(
                                                                                                                'Arg', [
                                                                                                                    ASTNode(
                                                                                                                        'Expression', [
                                                                                                                            ASTNode(
                                                                                                                                'SimpleExpression', [
                                                                                                                                    ASTNode(
                                                                                                                                        'Term', [
                                                                                                                                            ASTNode(
                                                                                                                                                'Factor', [
                                                                                                                                                    ASTNode(
                                                                                                                                                        'UnsignedConstant', [
                                                                                                                                                            ASTNode('String', ['Não disseste Hello...'])
                                                                                                                                                        ]
                                                                                                                                                    )
                                                                                                                                                ]
                                                                                                                                            )
                                                                                                                                        ]
                                                                                                                                    )
                                                                                                                                ]
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    )
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    None
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    assert result == expected


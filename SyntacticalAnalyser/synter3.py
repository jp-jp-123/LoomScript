from LexicalAnalyser import lexer
from LexicalAnalyser import tokens
from SyntacticalAnalyser import expr_table as expt


# TODO: LOOP


class Synter:
    def __init__(self):
        self.lexerOut = None
        self.symTable = None
        self.symTIndex = 0
        self.farLook = 0

        self.beforeTok = None
        self.currTok = None
        self.currTokVal = None
        self.currLine = None
        self.savedExpectedTok = None
        self.savedExpectedVal = None

        self.kw = tokens.KEYWORDS
        self.sc = tokens.SPECIAL_CHARACTERS
        self.op = tokens.OPERATORS
        self.unop = tokens.UNARY_OPS
        self.dblop = tokens.DOUBLE_OPERATORS
        self.validAtoms = ['NUM_LITERAL', 'STRING_LITERAL', 'IDENTIFIER', 'LPAREN_SC', 'INP_KW', 'GET_KW']
        self.invalidAtomLimits = ['EOF_TOKEN', 'RPAREN_SC', 'INP_KW']

    class Node:
        def __init__(self, nodeType, left=None, right=None, value=None):
            self.nodeType = nodeType
            self.left = left
            self.right = right
            self.value = value

        def __repr__(self):
            if self.left is None and self.right is None:
                return f'({self.value}: {self.nodeType})'
            elif self.left is None:
                return f'({self.value}: {self.nodeType}, {self.right})'
            elif self.right is None:
                return f'({self.left}, {self.value}: {self.nodeType})'
            else:
                return f'({self.left}, {self.value}: {self.nodeType}, {self.right})'

    def Generate(self, fpath):
        self.lexerOut = lexer.Lexer()
        self.lexerOut.SourceToLexemes(fpath)
        self.symTable = self.lexerOut.tokenTable
        # print(self.symTable)

    def GetToken(self):
        # Get the token of the current index
        i = self.symTIndex

        self.beforeTok = self.symTable[-1 + i][2]
        self.beforeTokVal = self.symTable[-1 + i][1]
        self.currTok = self.symTable[i][2]
        self.currTokVal = self.symTable[i][1]
        self.currLine = self.symTable[i][0]

    def Advance(self):
        # Advance to next token
        self.symTIndex += 1

        # has far_look or not, still advances to the next token. The far look index is just not consumed
        if self.symTIndex < len(self.symTable):
            self.GetToken()

    def Lookahead(self, steps=0):
        look_idx = self.symTIndex + steps

        if look_idx < len(self.symTable):
            return self.symTable[look_idx][2]
        else:
            return self.symTable[-1][2]

    def MakeNode(self, nodeType, left, right=None, n=None):
        return Synter.Node(nodeType, left, right, value=n)

    def MakeLeaf(self, nodeType, n):
        # Makes a leaf node but not connected to anything yet
        return Synter.Node(nodeType, value=n)

    # TODO: Add more robust method for error handling/unify Expects() and Error() in one method
    def Expects(self, msg, token):
        if self.currTok == token:
            self.Advance()
            return
        print(f"{msg}: Expecting '{token}', found '{self.currTok}', in line: {self.currLine}")
        exit(1)

    def Error(self, msg, token):
        print(f"{msg}: Expecting '{token}', found '{self.currTok}', in line: {self.currLine}")
        exit(1)

    def Skips(self, items: list, equal_to=True):
        if equal_to:
            while self.currTok == items:
                self.Advance()
                if self.currTok == 'EOF_TOKEN':
                    break
                elif self.currTok != 'NEWLINE':
                    break
                else:
                    pass
        else:
            while self.currTok != items:
                self.Advance()
                if self.currTok == 'EOF_TOKEN':
                    break
                elif self.currTok != 'NEWLINE':
                    break
                else:
                    pass

        return

    def ArgsExpr(self, expected_expr=None):
        # Similar to ParenExpr(), except this handles multiple arguments instead of expression
        args = None
        self.Expects(self.currTok, self.sc['('])
        while self.currTok in expected_expr:
            args = self.MakeNode('ARGUMENT', args, self.currTok)
            self.Advance()
            if self.currTok == self.sc[',']:
                self.Advance()
            else:
                # Finds the closing paren before returning
                self.Expects(self.currTok, self.sc[')'])
                return args

    def ParenExpr(self, func, parens: list, expected_expr=None):
        # Build the expression inside the parenthesis here

        self.Expects(self.currTok, self.sc[parens[0]])
        if expected_expr:
            self.Expects(self.currTok, expected_expr)
            # Since expects already advances the statements, we use beforeTok to return what we need
            self.savedExpectedTok = self.beforeTok
            self.savedExpectedVal = self.beforeTokVal
            node = self.MakeLeaf(self.beforeTokVal, self.savedExpectedTok)
        else:
            if func == self.Expression:
                node = func(1)
            else:
                self.Advance()  # Skips the associated NEWLINE after the bracket
                node = func()

        self.Expects(self.currTok, self.sc[parens[1]])
        return node

    def SDLCExpression(self):
        # still broken
        node_rep = None

        if self.currTok == 'NEWLINE':
            self.Skips(['IDENTIFIER', 'STRING_LITERAL', self.sc['}']], False)
            if self.currTok in ['IDENTIFIER', 'STRING_LITERAL']:
                pass
            elif self.currTok == self.sc['}']:
                pass

        if self.currTok in ['IDENTIFIER', 'STRING_LITERAL']:
            node_rep = self.MakeLeaf(self.currTok, self.currTokVal)
            self.Advance()
            if self.currTok == 'NEWLINE':
                pass
            else:
                self.Expects(self.currTok, self.sc[':'])



        while self.currTok not in [self.sc['}'], 'EOF_TOKEN', 'NEWLINE']:
            direction = self.currTok
            self.Advance()

            if self.currTok in [self.sc['}'], 'EOF_TOKEN', 'NEWLINE']:
                # print('breaking', node_rep)
                return node_rep

            self.ParenExpr(self.Expression, parens=['(', ')'], expected_expr='NUM_LITERAL')

            # If we get to this statement it means we got the expected expression inside the (), use saveExpected to
            # retrieve last value and make the condition leaf
            head_leaf = self.MakeNode(direction, self.MakeLeaf(self.savedExpectedTok, self.savedExpectedVal), None)
            self.Expects(self.currTok, self.sc[':'])

            node = self.SDLCExpression()

            node_rep = self.MakeNode(head_leaf, node_rep, node)
            # print('nodes', node_rep)
            return node_rep

        # print('last node', node_rep)
        return node_rep

    def LookaheadAtom(self):
        node_rep = self.MakeLeaf(self.currTok, self.currTokVal)
        self.Advance()

        # Lookahead, Atoms expect these things. Further check is NEWLINE is the self.currTok
        if self.currTok not in expt.all_op and self.currTok not in self.invalidAtomLimits:
            if self.currTok == 'NEWLINE':
                # returns the node representation if self.currTok avoided illegal lookahead tokens
                return node_rep
            else:
                self.Error(self.currTok, "OPERATORS")

        # returns the node representation if self.currTok avoided illegal lookahead tokens
        return node_rep

    def Expression(self, precedence):
        # Building the Expression

        node_rep = None  # Building the Node Representation here
        p = precedence

        # This if-else block checks for "Atoms"
        if self.currTok == 'IDENTIFIER':  # Identifier
            node_rep = self.LookaheadAtom()

        elif self.currTok == 'NUM_LITERAL':  # NUM_LITERALS
            node_rep = self.LookaheadAtom()

        elif self.currTok == 'STRING_LITERAL':  # STRING_LITERALS
            node_rep = self.LookaheadAtom()

        elif self.currTok == 'INP_KW':  # INPUT KEYWORD
            node_rep = self.MakeLeaf(self.currTok, self.currTokVal)
            self.Advance()
            self.ParenExpr(self.Expression, parens=['(', ')'], expected_expr='STRING_LITERAL')

        elif self.currTok == 'GET_KW':
            self.Advance()
            node_rep = self.MakeNode('GET_KW', self.ArgsExpr(['IDENTIFIER', 'STRING_LITERAL']), None)

        elif self.currTok == self.sc['(']:  # START OF PARENTHESIS EXPR
            node_rep = self.ParenExpr(self.Expression, parens=['(', ')'])

        elif self.currTok == 'NEWLINE':
            self.Advance()

        elif self.currTok in ['ARITHMETIC_ADD', 'ARITHMETIC_SUBTRACT', 'UNARY_INCREMENT', 'UNARY_DECREMENT']:  # UNARIES
            # Switching all of them to unary except add
            if self.currTok == 'ARITHMETIC_SUBTRACT':
                op = 'UNARY_SUBTRACT'
            elif self.currTok == 'UNARY_DECREMENT':
                op = 'UNARY_DECREMENT'
            elif self.currTok == 'UNARY_INCREMENT':
                op = 'UNARY_INCREMENT'
            else:
                op = 'ARITHMETIC_ADD'

            self.Advance()

            # Lookahead, Unaries expect these things. If not satisfied, proceed to syntax error
            if self.currTok not in self.validAtoms:
                self.Error(op, self.validAtoms)

            # Call Expression() again with precedence same to UNARY_SUBTRACT. Any prefix unaries are fine
            node = self.Expression(expt.all_op['UNARY_SUBTRACT'][2])
            node_rep = self.MakeNode(op, None, node)

        else:
            # TODO: Add support for postfix unaries
            self.Error(self.currTok, "'NUM_LITERAL', 'STRING_LITERAL', 'IDENTIFIER'")

        # Try catch block for Key Error due to self.currTok to getting unintended tokens for the while loop
        try:
            #  Condition for expression. Check if it's a binary and precedence is >= to p
            while expt.all_op[self.currTok][1] and expt.all_op[self.currTok][2] >= p:
                # Save the current token to op
                op = self.currTok
                op_value = self.currTokVal

                # Advance and check if the next token is as expected, error otherwise
                self.Advance()
                if self.currTok not in self.validAtoms:
                    self.Error(self.beforeTok, "'NUM_LITERAL', 'STRING_LITERAL', 'IDENTIFIER', 'LPAREN_SC', 'INP_KW'")

                # Get the precedence of op/saved token
                op_prec = expt.all_op[op][2]

                # Check is has left assoc, add 1 to precedence
                if not expt.all_op[op][0]:
                    op_prec += 1

                # call Expression() again, and save the node_rep to node
                node = self.Expression(op_prec)

                # build the created nodes
                node_rep = self.MakeNode(op, node_rep, node, op_value)

        except KeyError:
            pass

        return node_rep

    def Statement(self):
        # Building the Statement
        # Basically every if is a syntax of the statement

        node_rep = None  # Building the Node Representation here

        if self.currTok == 'IDENTIFIER':
            # TODO: incomplete declaration statement
            left_leaf = self.MakeLeaf(self.currTok, self.currTokVal)
            self.Advance()
            self.Expects("Assign", self.currTok)
            right_leaf = self.Expression(0)
            node_rep = self.MakeNode('ASSIGN_OP', left_leaf, right_leaf)
            self.ExitCond()

        elif self.currTok == 'OUT_KW':
            self.Advance()
            right_leaf = self.ParenExpr(self.Expression, parens=['(', ')'])
            node_rep = self.MakeNode('OUT_KW', None, right_leaf)
            self.ExitCond()

        elif self.currTok == 'SET_KW':
            self.Advance()
            expect = self.Lookahead(1)
            cond_leaf = None
            if expect == 'STRING_LITERAL':
                cond_leaf = self.ParenExpr(self.Expression, parens=['(', ')'], expected_expr='STRING_LITERAL')
            elif expect == 'IDENTIFIER':
                cond_leaf = self.ParenExpr(self.Expression, parens=['(', ')'], expected_expr='IDENTIFIER')
            else:
                self.Error(expect, "'STRING_LITERAL', IDENTIFIER")

            self.Expects(self.currTok, self.sc['{'])
            self.Advance()

            while self.currTok != self.sc['}']:
                right_node = self.Statement()
                if right_node == None:
                    pass
                else:
                    node_rep = self.MakeNode('BODY', node_rep, right_node)

            head_node = self.MakeNode('SET_KW', None, cond_leaf)
            node_rep = self.MakeNode('BODY', head_node, node_rep)

            self.ExitCond(custom=self.sc['}'])

        elif self.currTok == 'FILEOP_KW':
            self.Advance()
            node_rep = self.MakeNode('FILEOP_KW', self.ArgsExpr(['IDENTIFIER', 'STRING_LITERAL']), None)

        elif self.currTok == 'TODO_KW':
            self.Advance()
            node_rep = self.MakeNode('TODO_KW', self.ArgsExpr(['IDENTIFIER', 'STRING_LITERAL']), None)

        elif self.currTok == 'SDLC_KW':
            self.Advance()
            t = None
            self.Expects(self.currTok, self.sc['{'])

            while True:
                body_node = self.SDLCExpression()
                if body_node is None:
                    # print('in bd', body_node)
                    pass
                else:
                    if body_node is not None:
                        t = self.MakeNode('SDLC_BODY', t, body_node)
                self.Skips(['IDENTIFIER', 'STRING_LITERAL', self.sc['}']], False)
                if self.currTok == self.sc['}']:
                    break

            self.Expects(self.currTok, self.sc['}'])

            node_rep = self.MakeNode('SDLC_KW', None, t)
            return node_rep

        elif self.currTok == 'IF_KW':
            if_node_rep = None
            ifelse_body_rep = None
            ifelse_node_wrap = None
            ifelse_blocks = []
            else_node_rep = None

            self.Advance()
            cond_leaf = self.ParenExpr(self.Expression, parens=['(', ')'])
            self.Expects(self.currTok, self.sc['{'])
            self.Advance()

            while self.currTok != self.sc['}']:
                if_node = self.Statement()
                if if_node is None:
                    pass
                else:
                    if_node_rep = self.MakeNode('BODY', if_node_rep, if_node)

            # Creates a node for the condition statement
            if_cond_node = self.MakeNode('CONDITION', None, cond_leaf)
            self.Expects(self.currTok, self.sc['}'])

            # Continuously iterates over tokens until it gets the possible next value [IF_KW, ELSE_KW]
            self.Skips(['ELSE_KW', 'IF_ELSE_TOKEN'], False)

            while self.currTok == 'IF_ELSE_TOKEN':
                self.Advance()
                ifelse_cond_leaf = self.ParenExpr(self.Expression, parens=['(', ')'])
                self.Expects(self.currTok, self.sc['{'])
                self.Advance()

                while self.currTok != self.sc['}']:
                    ifelse_node = self.Statement()
                    if ifelse_node is None:
                        pass
                    else:
                        ifelse_body_rep = self.MakeNode('BODY', ifelse_body_rep, ifelse_node)

                # Creates a node for the condition statement
                ifelse_cond_node = self.MakeNode('CONDITION', None, ifelse_cond_leaf)

                # Build the body of the statement
                ifelse_body_rep = self.MakeNode('IF_ELSE', ifelse_cond_node, ifelse_body_rep)

                self.Expects(self.currTok, self.sc['}'])

                # After creating the node, append to the list to separate the blocks of each if else
                ifelse_blocks.append(ifelse_body_rep)
                ifelse_body_rep = None

                # Continuously iterates over tokens until it gets the possible next value [IF_KW, ELSE_KW]
                self.Skips(['ELSE_KW', 'IF_ELSE_TOKEN'], False)

            if ifelse_blocks:
                for block in ifelse_blocks:
                    ifelse_node_wrap = self.MakeNode('IF_ELSE_BLOCK', ifelse_node_wrap, block)

            if self.currTok == 'ELSE_KW':
                self.Advance()
                self.Expects(self.currTok, self.sc['{'])
                self.Advance()

                while self.currTok != self.sc['}']:
                    else_node = self.Statement()
                    if else_node is None:
                        pass
                    else:
                        else_node_rep = self.MakeNode('BODY', else_node_rep, else_node)

                self.Expects(self.currTok, self.sc['}'])

            if ifelse_blocks:
                node_rep = self.MakeNode('IF_KW', None, (self.MakeNode('IF_BODY', if_cond_node, if_node_rep),
                                                         self.MakeNode('IF_ELSE_BODY', None, ifelse_node_wrap),
                                                         self.MakeNode('ELSE_BODY', None, else_node_rep)
                                                         ))
            elif len(ifelse_blocks) == 0 and else_node_rep:
                node_rep = self.MakeNode('IF_KW', None, (self.MakeNode('IF_BODY', if_cond_node, if_node_rep),
                                                         self.MakeNode('ELSE_BODY', None, else_node_rep)
                                                         ))

            elif len(ifelse_blocks) != 0 and else_node_rep is None:
                node_rep = self.MakeNode('IF_KW', None, (self.MakeNode('IF_BODY', if_cond_node, if_node_rep),
                                                         self.MakeNode('IF_ELSE_BODY', None, ifelse_node_wrap)
                                                         ))

            elif len(ifelse_blocks) == 0 and else_node_rep is None:
                node_rep = self.MakeNode('IF_KW', None, self.MakeNode('IF_BODY', if_cond_node, if_node_rep))

        elif self.currTok == 'COMMENT':
            self.Advance()

        elif self.currTok == 'NEWLINE':
            self.Advance()

        else:
            # TODO: Postfix unaries exits here, add support for postfix unary
            # TODO: unexpected syntax error might exit here, test for every expression errors as you like and report
            if self.currTok == 'RPAREN_SC':
                # RPAREN_SC at the end exits here, this catches it for now
                self.Expects(self.currTok, self.sc['('])
            else:
                if self.currTok == 'NEWLINE':
                    print("is nl", self.currTok)
                    self.Expects(self.currTok, 'NEWLINE')
                elif self.currTok == 'EOF_TOKEN':
                    print(" is eof")
                    self.Expects(self.currTok, 'EOF_TOKEN')
                else:
                    print(f"Error in this token {self.beforeTok}, {self.currTok}")
                    exit(1)

        return node_rep

    def ExitCond(self, custom=None):
        if custom:
            self.Expects(self.currTok, custom)
        if self.currTok == 'NEWLINE':
            self.Expects(self.currTok, 'NEWLINE')
        elif self.currTok == 'EOF_TOKEN':
            self.Expects(self.currTok, 'EOF_TOKEN')
        else:
            print(f"Error in this token {self.currTok}")
            exit(1)

    def Parse(self):
        # Generate the Symbol Table
        path = "C:\\Users\\Lenovo\\Documents\\GitHub\\LoomScript\\TestCase\\test3.loom"
        self.Generate(path)

        # Start parsing by getting the first/index 0 token, call the statement() to see where to branch off
        tree = None
        self.GetToken()
        while True:
            node_result = self.Statement()

            # Filters the result of the node
            if node_result is None:
                # if it is none, ignores it, avoids creating nodes that doesn't contain anything
                pass
            else:
                # if it contains anything, create a node
                if node_result is not None:
                    tree = self.MakeNode('SEQUENCE', tree, node_result)
            if self.currTok == "EOF_TOKEN":
                break

        return tree


if __name__ == '__main__':
    main = Synter()
    parser = main.Parse()
    print(parser)

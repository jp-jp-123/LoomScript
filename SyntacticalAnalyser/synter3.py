from LexicalAnalyser import lexer
from LexicalAnalyser import tokens
from SyntacticalAnalyser import expr_table as expt


class ConstNode:
    def __init__(self, tok):
        self.token = tok

    def __repr__(self):
        return f'{self.token}'


class BinNode:
    def __init__(self, tok, l_node, r_node):
        self.token = tok
        self.lNode = l_node
        self.rNode = r_node

    def __repr__(self):
        return f'{self.lNode}, {self.token}, {self.rNode}'


class Synter:
    def __init__(self):
        self.lexerOut = None
        self.symTable = None
        self.symTIndex = 0
        self.farLook = 0

        self.beforeTok = None
        self.currTok = None
        self.currTokVar = None
        self.currLine = None

        self.kw = tokens.KEYWORDS
        self.sc = tokens.SPECIAL_CHARACTERS
        self.op = tokens.OPERATORS
        self.unop = tokens.UNARY_OPS
        self.dblop = tokens.DOUBLE_OPERATORS
        self.validAtoms = ['NUM_LITERAL', 'STRING_LITERAL', 'IDENTIFIER', 'LPAREN_SC', 'INP_KW']

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
        self.currTok = self.symTable[i][2]
        self.currTokVar = self.symTable[i][1]
        self.currLine = self.symTable[i][0]

    def Advance(self, far_look=0):
        # Advance to next token
        self.symTIndex += 1

        # local isFarLook
        isFarLook = False

        # for farther (>1) lookahead (ex: parenthesis expecting multiple possibilities)
        # farLook index = current + far_look
        if far_look > 0:
            isFarLook = True
            self.farLook = self.symTIndex + far_look

        # has far_look or not, still advances to the next token. The far look index is just not consumed
        if self.symTIndex < len(self.symTable):
            self.GetToken()
            # returns token value of the specified lookahead index, returns EOF others
            if isFarLook:
                if far_look < len(self.symTable):
                    return self.symTable[self.farLook][2]
                else:
                    return 'EOF_TOKEN'

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
        print(f"{msg}: Expecting '{token}', found '{self.beforeTok}', in line: {self.currLine}")
        exit(1)

    def Error(self, msg, token):
        print(f"{msg}: Expecting '{token}', found '{self.currTok}', in line: {self.currLine}")
        exit(1)

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

    def ParenExpr(self, expected_expr=None):
        # Build the expression inside the parenthesis here
        self.Expects(self.currTok, self.sc['('])
        if expected_expr:
            node = self.Expects(self.currTok, expected_expr)
        else:
            node = self.Expression(1)

        self.Expects(self.currTok, self.sc[')'])
        return node

    def LookaheadAtom(self):
        node_rep = self.MakeLeaf(self.currTok, self.currTokVar)
        self.Advance()

        # Lookahead, Atoms expect these things. Further check is NEWLINE is the self.currTok
        if self.currTok not in expt.all_op and self.currTok != 'EOF_TOKEN' and self.currTok != 'RPAREN_SC' and self.currTok != 'INP_KW':
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
        if self.currTok == 'IDENTIFIER':                                # Identifier
            node_rep = self.LookaheadAtom()

        elif self.currTok == 'NUM_LITERAL':                             # NUM_LITERALS
            node_rep = self.LookaheadAtom()

        elif self.currTok == 'STRING_LITERAL':                          # STRING_LITERALS
            node_rep = self.LookaheadAtom()

        elif self.currTok == 'INP_KW':                                  # INPUT KEYWORD
            node_rep = self.MakeLeaf(self.currTok, self.currTokVar)
            self.Advance()
            self.ParenExpr(expected_expr='STRING_LITERAL')

        elif self.currTok == self.sc['(']:                              # START OF PARENTHESIS EXPR
            node_rep = self.ParenExpr()

        elif self.currTok == 'NEWLINE':
            self.Advance()

        elif self.currTok in ['ARITHMETIC_ADD', 'ARITHMETIC_SUBTRACT', 'UNARY_INCREMENT', 'UNARY_DECREMENT']:   # UNARIES
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
                self.Error(op, "'NUM_LITERAL', 'STRING_LITERAL', 'IDENTIFIER', 'LPAREN_SC', 'INP_KW'")

            # Call Expression() again with precedence same to UNARY_SUBTRACT. Any prefix unaries are fine
            node = self.Expression(expt.all_op['UNARY_SUBTRACT'][2])
            node_rep = self.MakeNode(op, None, node)

        else:
            # TODO: Add support for postfix unaries
            self.Error(self.currTok, "'NUM_LITERAL', 'STRING_LITERAL', 'IDENTIFIER'")

        # Try catch block for Key Error due to self.currTok to unintended tokens for the while loop
        try:
            #  Condition for expression. Check if it's a binary and precedence is >= to p
            while expt.all_op[self.currTok][1] and expt.all_op[self.currTok][2] >= p:
                # Save the current token to op
                op = self.currTok
                op_value = self.currTokVar

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
            left_leaf = self.MakeLeaf(self.currTok, self.currTokVar)
            self.Advance()
            self.Expects("Assign", self.currTok)
            right_leaf = self.Expression(0)
            node_rep = self.MakeNode('ASSIGN_OP', left_leaf, right_leaf)
            self.ExitCond()

        elif self.currTok == 'OUT_KW':
            self.Advance()
            right_leaf = self.ParenExpr()
            node_rep = self.MakeNode('OUT_KW', None, right_leaf)
            self.ExitCond()

        elif self.currTok == 'SET_KW':
            expect = self.Advance(far_look=1)
            left_leaf = None
            if expect == 'STRING_LITERAL':
                left_leaf = self.ParenExpr(expected_expr='STRING_LITERAL')
            elif expect == 'IDENTIFIER':
                left_leaf = self.ParenExpr(expected_expr='IDENTIFIER')
            else:
                self.Error(expect, "'STRING_LITERAL', IDENTIFIER")

            self.Expects(self.currTok, self.sc['{'])
            self.Advance()

            while self.currTok != self.sc['}']:
                # Same logic as expressions, NEWLINES just returns None and should be ignored
                right_node = self.Statement()
                if right_node == None:
                    pass
                else:
                    node_rep = self.MakeNode('BODY', node_rep, right_node)

            node_rep = self.MakeNode('SET_KW', left_leaf, node_rep)

            self.ExitCond(custom=self.sc['}'])

        elif self.currTok == 'NEWLINE':
            self.Advance()

        else:
            # TODO: Postfix unaries exits here, add support for postfix unary
            # TODO: unexpected syntax error might exit here, test for every expression errors as you like and report
            if self.currTok == 'RPAREN_SC':
                # RPAREN_SC at the end exits here, this catches it for n0w
                self.Expects(self.currTok, self.sc['('])
            else:
                if self.currTok == 'NEWLINE':
                    print("is nl", self.currTok)
                    self.Expects(self.currTok, 'NEWLINE')
                elif self.currTok == 'EOF_TOKEN':
                    print(" is eof")
                    self.Expects(self.currTok, 'EOF_TOKEN')
                else:
                    print(f"Error in this token {self.currTok}")
                    exit(1)

        return node_rep

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
            if tree is None:
                # if it is none, store it back to tree, avoids creating nodes that doesn't contain anything
                tree = node_result
            else:
                # if it contains anything, create a node
                if tree is not None:
                    tree = self.MakeNode('SEQUENCE', tree, node_result)
            if self.currTok == "EOF_TOKEN":
                break

        return tree


if __name__ == '__main__':
    main = Synter()
    parser = main.Parse()
    print(parser)

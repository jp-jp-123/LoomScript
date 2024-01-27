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

        self.beforeTok = None
        self.currTok = None
        self.currTokVar = None
        self.currLine = None

        self.kw = tokens.KEYWORDS
        self.sc = tokens.SPECIAL_CHARACTERS
        self.op = tokens.OPERATORS
        self.unop = tokens.UNARY_OPS
        self.dblop = tokens.DOUBLE_OPERATORS

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

    def Advance(self):
        # Advance to next token
        self.symTIndex += 1

        if self.symTIndex < len(self.symTable):
            self.GetToken()

    def MakeNode(self, nodeType, left, right=None):
        return Synter.Node(nodeType, left, right)

    def MakeLeaf(self, nodeType, n):
        # Makes a leaf node but not connected to anything yet
        return Synter.Node(nodeType, value=n)

    def Expects(self, msg, token):
        if self.currTok == token:
            self.Advance()
            return
        print(f"{msg}: Expecting '{token}', found '{self.beforeTok}', in line: {self.currLine}")
        exit(1)

    def Error(self, msg, token):
        print(f"{msg}: Expecting '{token}', found '{self.currTok}', in line: {self.currLine}")
        exit(1)

    def ParenExpr(self):
        # Build the expression inside the parenthesis here
        self.Expects("Unbalanced Parenthesis", self.sc['('])
        node = self.Expression(1)
        self.Expects("Unbalanced Parenthesis", self.sc[')'])
        return node

    def Expression(self, precedence):
        # Building the Expression

        node_rep = None  # Building the Node Representation here
        p = precedence

        # This if-else block checks for "Atoms"
        if self.currTok == 'IDENTIFIER':                                # Identifier
            node_rep = self.MakeLeaf(self.currTok, self.currTokVar)
            self.Advance()

            # Lookahead, Atoms expect these things. If not satisfied, proceed to syntax error
            if self.currTok not in expt.all_op and self.currTok != 'EOF_TOKEN':
                self.Error(self.currTok, "OPERATORS")

        elif self.currTok == 'NUM_LITERAL':                             # NUM_LITERALS
            node_rep = self.MakeLeaf(self.currTok, self.currTokVar)
            self.Advance()

            # Lookahead, Atoms expect these things. If not satisfied, proceed to syntax error
            if self.currTok not in expt.all_op and self.currTok != 'EOF_TOKEN':
                self.Error(self.currTok, "OPERATORS")

        elif self.currTok == 'STRING_LITERAL':                          # STRING_LITERALS
            node_rep = self.MakeLeaf(self.currTok, self.currTokVar)
            self.Advance()

            # Lookahead, Atoms expect these things. If not satisfied, proceed to syntax error
            if self.currTok not in expt.all_op and self.currTok != 'EOF_TOKEN':
                self.Error(self.currTok, "OPERATORS")

        elif self.currTok == self.sc['(']:                              # START OF PARENTHESIS EXPR
            node_rep = self.ParenExpr()

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
            if self.currTok not in ['NUM_LITERAL', 'STRING_LITERAL', 'IDENTIFIER', 'LPAREN_SC']:
                self.Error(op, "'NUM_LITERAL', 'STRING_LITERAL', 'IDENTIFIER'")

            # Call Expression() again with precedence same to UNARY_SUBTRACT. Any prefix unaries are fine
            node = self.Expression(expt.unary_pref['UNARY_SUBTRACT'][2])
            # if op == 'ARITHMETIC_ADD':
            # node_rep = node
            # else:
            # Makes node where any literals or idents are on the right (as expected)
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

                # Advance and check if the next token is as expected, error otherwise
                self.Advance()
                if self.currTok not in ['NUM_LITERAL', 'STRING_LITERAL', 'IDENTIFIER', 'LPAREN_SC']:
                    self.Error(self.beforeTok, "'NUM_LITERAL', 'STRING_LITERAL', 'IDENTIFIER', 'LPAREN_SC'")

                # Get the precedence of op/saved token
                op_prec = expt.all_op[op][2]

                # Check is has left assoc, add 1 to precedence
                if not expt.all_op[op][0]:
                    op_prec += 1

                # call Expression() again, and save the node_rep to node
                node = self.Expression(op_prec)

                # build the created nodes
                node_rep = self.MakeNode(op, node_rep, node)

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
            # print(node_rep)
        else:
            # TODO: Postfix unaries exits here, add support for postfix unary
            # TODO: unexpected syntax error might exit here, test for every expression errors as you like and report
            self.Expects(self.currTok, self.sc['('])

        return node_rep

    def Parse(self):
        # Generate the Symbol Table
        path = "C:\\Users\\Lenovo\\Documents\\GitHub\\LoomScript\\TestCase\\test3.loom"
        self.Generate(path)

        # Start parsing by getting the first/index 0 token, call the statement() to see where to branch off
        t = None
        self.GetToken()
        while True:
            t = self.MakeNode('SEQUENCE', t, self.Statement())
            if self.currTok == "EOF_TOKEN":
                break

        return t


if __name__ == '__main__':
    main = Synter()
    parser = main.Parse()
    print(parser)
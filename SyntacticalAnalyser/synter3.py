from LexicalAnalyser import lexer
from LexicalAnalyser import tokens
from SyntacticalAnalyser import expr_table as expt


# TODO: LAST TO DO. BUG AND CODE CLEANUP


class Synter:
    def __init__(self):
        self.lexerOut = None    # Calls lexer
        self.symTable = None    # Symbol table
        self.symTIndex = 0      # Symbol Table Index
        self.farLook = 0        # Custom table index, for Lookahead

        self.beforeTok = None   # Before Token
        self.currTok = None     # Current Token
        self.currTokVal = None  # Current Token Value
        self.currLine = None    # Current Line
        self.savedExpectedTok = None    # Saves Expected Token
        self.savedExpectedVal = None    # Saves Expected Value

        self.kw = tokens.KEYWORDS
        self.sc = tokens.SPECIAL_CHARACTERS
        self.op = tokens.OPERATORS
        self.unop = tokens.UNARY_OPS
        self.dblop = tokens.DOUBLE_OPERATORS

        # Atoms = Terms (Atoms: expected tokens after operators)
        self.validAtoms = ['NUM_LITERAL', 'STRING_LITERAL', 'IDENTIFIER', 'LPAREN_SC', 'INP_KW', 'GET_KW']
        # validAtomLimits = what expected to see after atoms
        self.validAtomLimits = ['EOF_TOKEN', 'RPAREN_SC', 'COMMA_SC']     # i removed INP_KW, seems unnecessary, if anything effs up, look here first

    class Node:
        def __init__(self, nodeType, left=None, right=None, value=None):
            self.nodeType = nodeType
            self.left = left
            self.right = right
            self.value = value

        # repr = representation
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
        # Generates the symbol table
        self.lexerOut = lexer.Lexer()
        self.lexerOut.SourceToLexemes(fpath)
        self.symTable = self.lexerOut.tokenTable

    def GetToken(self):
        # Get the token of the current index
        i = self.symTIndex

        self.beforeTok = self.symTable[-1 + i][2]
        self.beforeTokVal = self.symTable[-1 + i][1]

        # [[line, lexeme, token], .....]
        self.currTok = self.symTable[i][2]
        self.currTokVal = self.symTable[i][1]
        self.currLine = self.symTable[i][0]

    def Advance(self):
        # Advance to next token
        self.symTIndex += 1

        if self.symTIndex < len(self.symTable):
            self.GetToken()

    def Lookahead(self, steps=0):
        look_idx = self.symTIndex + steps   # index 6 + 2 = index 8

        if look_idx < len(self.symTable):
            return self.symTable[look_idx][2]
        else:
            return self.symTable[-1][2]     # returns the last value of the symbol table i.e. EOF_TOKEN

    # For making parent node
    def MakeNode(self, nodeType, left, right=None, n=None):
        return Synter.Node(nodeType, left, right, value=n)

    # Makes a leaf node but not connected to anything yet
    def MakeLeaf(self, nodeType, n):
        return Synter.Node(nodeType, value=n)

    # Expects() takes one character only and checks if your current token matches to what you want to see (...)
    def Expects(self, msg, token, advance=True):
        if self.currTok == token:
            if advance:     # if advance is false, Expects() will not get the next token. True by default
                self.Advance()
            return
        print(f"{msg}: Expecting '{token}', found '{self.currTok}', in line: {self.currLine}")
        exit(1)

    # Similar to Expects, except if you don't want to compare and sure you will get an error
    def Error(self, msg, token):
        print(f"{msg}: Expecting '{token}', found '{self.currTok}', in line: {self.currLine}")
        exit(1)

    # Skips newlines and eof token
    def Skips(self, items: list, equal_to=True):
        # items: are list you expected to see or not to see
        # equal_to: type of comparison you want
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

    # Similar to ParenExpr() except, these handles multiple non-expression arguments or parameters
    def ArgsExpr(self, expected_expr=None):
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

    # These can handle singular parameter syntax or expression
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
            direction = None
            if self.currTok in ['TOUP_KW', 'TODOWN_KW', 'TORIGHT_KW', 'TOLEFT_KW']:
                direction = self.currTok
                self.Advance()
            else:
                self.Error(self.currTok, "'TOUP_KW', 'TODOWN_KW', 'TORIGHT_KW', 'TOLEFT_KW'")

            if self.currTok in [self.sc['}'], 'EOF_TOKEN', 'NEWLINE']:
                self.Error(self.currTok, self.sc['('])

            self.ParenExpr(self.Expression, parens=['(', ')'], expected_expr='NUM_LITERAL')

            # If we get to this statement it means we got the expected expression inside the (), use saveExpected to
            # retrieve last value and make the condition leaf
            head_leaf = self.MakeNode(direction, self.MakeLeaf(self.savedExpectedTok, self.savedExpectedVal), None)
            self.Expects(self.currTok, self.sc[':'])

            node = self.SDLCExpression()

            node_rep = self.MakeNode(head_leaf, node_rep, node)
            return node_rep

        return node_rep

    def PostfixExpr(self, token, leaf):

        # Switching the current token/unary into postfix unary
        if token == 'ARITHMETIC_SUBTRACT':
            self.currTok = 'POSF_UNARY_SUBTRACT'
        elif token == 'UNARY_DECREMENT':
            self.currTok = 'POSF_UNARY_DECREMENT'
        elif token == 'UNARY_INCREMENT':
            self.currTok = 'POSF_UNARY_INCREMENT'
        else:
            self.currTok = 'POSF_UNARY_ADD'

        node_rep = self.MakeNode(self.currTok, leaf, n=self.currTokVal)
        self.Advance()

        return node_rep

    def LookaheadAtom(self):
        node_rep = self.MakeLeaf(self.currTok, self.currTokVal)
        self.Advance()

        # This block looks ahead and checks  the End of Statement
        # it basically restricts the postfixes to appear at the end of statement
        k = self.Lookahead(1)
        if k in ['NEWLINE', 'EOF_TOKEN']:
            # Getting these operators just before end of statement means their postfixes
            if self.currTok in ['ARITHMETIC_ADD', 'ARITHMETIC_SUBTRACT', 'UNARY_INCREMENT', 'UNARY_DECREMENT']:
                # test for unary add and sub
                node_rep = self.PostfixExpr(self.currTok, node_rep)
                return node_rep

        # Check if current token is an illegal character after atoms
        # expt.all_op: list of all operators
        # condition of operator is that next token must not be: an operator and validatomlimits
        if self.currTok not in expt.all_op and self.currTok not in self.validAtomLimits:
            if self.currTok == 'NEWLINE':
                # returns the node representation if self.currTok avoided illegal lookahead tokens
                return node_rep
            else:
                self.Error(self.currTok, "OPERATORS")

        # returns the node representation if self.currTok avoided illegal lookahead tokens
        return node_rep

    def Expression(self, precedence):
        # Building the Expression

        node_rep = None  # Building the Node/Tree Representation here
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

        # Unary operators are undecided if postfix/prefix, prefix are decided here, and postfix is decided
        # after checking the lookahead of other atoms
        elif self.currTok in ['ARITHMETIC_ADD', 'ARITHMETIC_SUBTRACT', 'UNARY_INCREMENT', 'UNARY_DECREMENT']:  # UNARIES
            # Switching all of them to unary except add
            if self.currTok == 'ARITHMETIC_SUBTRACT':
                op = 'PREF_UNARY_SUBTRACT'
                op_val = '-'
            elif self.currTok == 'UNARY_DECREMENT':
                op = 'PREF_UNARY_DECREMENT'
                op_val = '--'
            elif self.currTok == 'UNARY_INCREMENT':
                op = 'PREF_UNARY_INCREMENT'
                op_val = '++'
            else:
                op = 'PREF_UNARY_ADD'
                op_val = '+'

            self.Advance()

            # Lookahead, Unaries expect these things. If not satisfied, proceed to syntax error
            if self.currTok not in self.validAtoms:
                self.Error(op, self.validAtoms)

            # Call Expression() again with precedence same to UNARY_SUBTRACT. Any prefix unaries are fine
            node = self.Expression(expt.all_op['PREF_UNARY_SUBTRACT'][2])
            node_rep = self.MakeNode(op, None, node, n=op_val)

        else:
            self.Error(self.currTok, "'NUM_LITERAL', 'STRING_LITERAL', 'IDENTIFIER'")

        # Try catch block for Key Error due to self.currTok getting unintended tokens for the while loop
        try:
            #  Condition for expression. Check if it's a binary and precedence is >= to p
            while expt.all_op[self.currTok][1] and expt.all_op[self.currTok][2] >= p:
                # Save the current token to op
                op = self.currTok
                op_value = self.currTokVal

                # Advance and check if the next token is as expected, error otherwise
                self.Advance()
                if self.currTok not in self.validAtoms:
                    self.Error(self.beforeTok, self.validAtoms)

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
            left_leaf = self.MakeLeaf(self.currTok, self.currTokVal)    # Ex: (identifier_name: IDENTIFIER)
            self.Advance()
            self.Expects(self.currTok, 'ASSIGN_OP')     # Expects(msg, expected_tok)
            right_leaf = self.Expression(0)
            node_rep = self.MakeNode('ASSIGN_OP', left_leaf, right_leaf)

        elif self.currTok == 'OUT_KW':
            self.Advance()
            right_leaf = self.ParenExpr(self.Expression, parens=['(', ')'])
            node_rep = self.MakeNode('OUT_KW', None, right_leaf)

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

            self.Expects(self.currTok, self.sc['}'])

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

        elif self.currTok == 'LOOP_KW':
            self.Advance()
            arg1 = None
            arg2 = None
            if_arg1 = True
            get_args = True

            t = None

            self.Expects(self.currTok, self.sc['('], advance=False)

            while get_args:
                looks = self.Lookahead(1)

                if looks == 'IDENTIFIER':
                    # Since we haven't advanced yet, we double the lookahead to see if it's just an identifier or an
                    # actual expression
                    looks = self.Lookahead(2)

                    # Seeing the assign_op means an EXPRESSION is ahead
                    if looks == 'ASSIGN_OP':
                        self.Advance()
                        if if_arg1:
                            arg1 = self.Statement()
                        else:
                            arg2 = self.Statement()

                    # Seeing an operator means an EXPRESSION is ahead
                    elif looks in expt.all_op:
                        self.Advance()
                        if if_arg1:
                            arg1 = self.Expression(0)
                        else:
                            arg2 = self.Expression(0)

                    # Seeing unary postfix operator means an EXPRESSION is ahead
                    elif looks in expt.unary_posf:
                        self.Advance()
                        if if_arg1:
                            arg1 = self.Expression(0)
                        else:
                            arg2 = self.Expression(0)

                        # Seeing the delimiter means the IDENTIFIER is alone
                    elif looks == self.sc[',']:
                        self.Advance()
                        if if_arg1:
                            arg1 = self.MakeLeaf('IDENTIFIER', n=self.currTokVal)
                        else:
                            arg2 = self.MakeLeaf('IDENTIFIER', n=self.currTokVal)

                    # Seeing other than this results to an Error
                    else:
                        self.Advance()
                        self.Error(looks, "EXPRESSION OR COMMA DELIMITER")

                elif looks == 'NUM_LITERAL':
                    # Since we haven't advanced yet, we double the lookahead to see if it's just an identifier or an
                    # actual expression
                    looks = self.Lookahead(2)

                    # Seeing operators means EXPRESSION is ahead
                    if looks in expt.all_op:
                        self.Advance()
                        if if_arg1:
                            arg1 = self.Expression(0)
                        else:
                            arg2 = self.Expression(0)

                    # Seeing unary postfix operator means an EXPRESSION is ahead
                    elif looks in expt.unary_posf:
                        self.Advance()
                        if if_arg1:
                            arg1 = self.Expression(0)
                        else:
                            arg2 = self.Expression(0)

                    # Seeing the delimiter means the NUM_LITERAL is alone
                    elif looks == self.sc[',']:
                        self.Advance()
                        if arg1:
                            arg1 = self.MakeLeaf('NUM_LITERAL', n=self.currTokVal)
                        else:
                            arg2 = self.MakeLeaf('NUM_LITERAL', n=self.currTokVal)

                    # Seeing other than this results to an Error
                    else:
                        self.Advance()
                        self.Error(looks, "EXPRESSION OR COMMA DELIMITER")

                # Seeing unary prefix operator means an EXPRESSION is ahead
                elif looks in expt.unary_pref :
                    self.Advance()
                    if if_arg1:
                        arg1 = self.Expression(0)
                    else:
                        arg2 = self.Expression(0)

                elif if_arg1:
                    # Since NULL is only accepted in 1st argument, it will be only checked if if_arg1 is True
                    if looks == 'NULL_KW':
                        self.Advance()
                        arg1 = self.MakeLeaf('NULL_KW', n='NULL')
                        self.Advance()

                # Seeing other than this results to an Error
                else:
                    self.Advance()
                    self.Error(looks, "EXPRESSION OR COMMA DELIMITER")

                if if_arg1:
                    # reaching here means end of arg_1, switch it to false and start writing to arg2
                    self.Expects(self.currTok, self.sc[','], advance=False)
                    if_arg1 = False
                else:
                    # reaching here means end of arg_2, switch get_args to false to end the loop
                    get_args = False

            cond_node = self.MakeNode('CONDITION', arg1, arg2)

            self.Expects(self.currTok, self.sc[')'])
            self.Expects(self.currTok, self.sc['{'])

            # Recursively calls Statement() method
            while self.currTok != self.sc['}']:
                body_node = self.Statement()
                if body_node is None:
                    pass
                else:
                    if body_node is not None:
                        t = self.MakeNode('LOOP_BODY', t, body_node)

            self.Expects(self.currTok, self.sc['}'])

            node_rep = self.MakeNode('LOOP_KW', cond_node, t)

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
            print(f"Error in this token {self.beforeTok}, {self.currTok}, Line: {self.currLine}")
            exit(1)

        return node_rep

    def Parse(self, path):
        # Generate the Symbol Table
        self.Generate(path)

        # Start parsing by getting the first/index 0 token, call the statement() to see where to branch off
        tree = None
        self.GetToken()
        while True:
            node_result = self.Statement()

            # Filters the result of the node
            if node_result is None:
                # if it is none, ignores it, avoids creating nodes that doesn't contain anything
                # Comments and Newlines returns None
                pass
            else:
                # if it contains anything, create a node (parent node, left, right)
                if node_result is not None:
                    tree = self.MakeNode('SEQUENCE', tree, node_result)
            if self.currTok == "EOF_TOKEN":
                break

        return tree


if __name__ == '__main__':
    fpath = "C:\\Users\\Lenovo\\Documents\\GitHub\\LoomScript\\TestCase\\test2.loom"
    main = Synter()
    parser = main.Parse(fpath)
    print(parser)

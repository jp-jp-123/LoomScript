from LexicalAnalyser.tokens import *
from charset import *
from collections import OrderedDict

'''
utilizes only one buffer and clearer stopFlag logics in an effort to make a clearer and efficient lexer.
The difference from previous lexer is that in stopFlag, instead of adding to buffer then comparing, it compares first 
before adding to buffer.
'''


class Lexer:

    def __init__(self):
        self.tokenTable = []
        self.sourceCode = None

        self.buffer = ''

        self.stopFlag = False
        self.stopFlagValue = ''
        self.nonLexeme = False

        self.lineNo = 1
        self.charNo = 0
        self.lineLength = 0

    def SourceToLexemes(self, filepath: str):

        with open(filepath) as file:
            self.sourceCode = file.readlines()

        # Feeds file to parser by line
        for perLine in self.sourceCode:
            self.lineLength = len(perLine)
            self.LexemeParser(perLine)

        if self.buffer:
            self.Tokenizer(self.lineNo, self.buffer)
            self.BufferClear()
        self.tokenTable.append((self.lineNo, 'EOF', "EOF_TOKEN"))

    def LexemeParser(self, lexemes: str):

        for char in lexemes:

            # Char no. tracking
            self.charNo += 1

            # Line no. tacking
            if char == '\n':
                self.lineNo += 1
                self.charNo = 0

            if not self.stopFlag:
                # Mainly checks for identifiers, includes _ since it is a valid char for naming
                if char.isalnum() or char == '_':
                    # Tokenizes buffer if buffer contained non-identifier characters (use case ex: +1 +a)
                    if not self.ValidIdent(self.buffer):
                        self.Tokenizer(self.lineNo, self.buffer)
                        self.BufferClear()

                    # Checks if the buffer has contents and its first char
                    # Alphabet first char allows every character
                    # Digit first char only allows numbers, invalid lexeme otherwise.
                    if self.buffer:
                        if self.buffer[0].isalpha():
                            self.buffer += char
                        elif self.buffer[0].isdigit():
                            if char.isdigit():
                                self.buffer += char
                            else:
                                # We allow to add the illegal start of identifier, but will be tokenized as ERROR_TOKEN
                                print(f'Illegal Character at Char no. {self.charNo}, Line no. {self.lineNo}: {lexemes}')
                                self.buffer += char
                        # for debugging, if unexpected error arises
                        else:
                            print(f'Unknown Error at Char no. {self.charNo}, Line no. {self.lineNo}: {lexemes}')

                    # This just means that buffer is empty and will accept any char
                    else:
                        self.buffer += char

                    # Checks if the character is at EOL, necessary to get tokenized if didn't get followed by another
                    # character
                    if char == lexemes[-1]:
                        self.Tokenizer(self.lineNo, self.buffer)
                        self.BufferClear()

                # Basic tokenizing technique. If it hits whitespace, all in the buffer is one token
                elif char.isspace():
                    # Checks if buffer has contents
                    if self.buffer:
                        self.Tokenizer(self.lineNo, self.buffer)
                        self.BufferClear()

                elif char in SPECIAL_CHARACTERS:
                    # If a special char is hit after taking an alphanum, it means it is a separate token
                    # ex: 1+ a+ (1 gets tokenized, + goes down the further the if-else)
                    if self.buffer.replace('_', '').isalnum() and char != '.':
                        self.Tokenizer(self.lineNo, self.buffer)
                        self.BufferClear()

                    # Checks for start of STRING_LITERAL
                    if char == '"' or char == '\'':
                        if char == '"':
                            # flips stopFlag value, necessary to collect ALL the chars inside the string into the buffer
                            self.stopFlag = not self.stopFlag
                            self.stopFlagValue = '"'
                            self.buffer += char

                        else:
                            # flips stopFlag value, necessary to collect ALL the chars inside the string into the buffer
                            self.stopFlag = not self.stopFlag
                            self.stopFlagValue = '\''
                            self.buffer += char

                    # Checks for start of comment buffer = / char = / //
                    elif char == '/' and self.buffer == '/':
                        self.stopFlag = not self.stopFlag
                        self.stopFlagValue = '//'
                        self.nonLexeme = not self.nonLexeme
                        self.buffer += char

                    # Checks for start of decimal
                    elif char == '.':
                        self.stopFlag = not self.stopFlag
                        self.stopFlagValue = NOT_IN_DECIMAL
                        self.buffer += char

                        # if decimal found to be at EOL and ending in dot symbol (ex: d = 2.), tokenize
                        if self.charNo == self.lineLength:
                            self.Tokenizer(self.lineNo, self.buffer)
                            self.BufferClear()

                    else:
                        # char is in DOUBLES, add to buffer but don't tokenize
                        if char in DOUBLES:
                            self.buffer += char

                        # if not a DOUBLES, char is tokenized directly
                        else:
                            # Tokenize whatever inside the buffer
                            if self.buffer:
                                self.Tokenizer(self.lineNo, self.buffer)
                            self.Tokenizer(self.lineNo, char)
                            self.BufferClear()

                # takes the illegal characters
                else:
                    print(f'Illegal Character at Char no. {self.charNo}, Line no. {self.lineNo}: {lexemes}')

                    # Block for Illegal Characters in Identifiers

                    # Tokenizes current buffer contents (if it contains anything) and clears it
                    if self.buffer:
                        self.Tokenizer(self.lineNo, self.buffer)
                        self.BufferClear()

                    # Tokenizes the illegal character as error
                    self.tokenTable.append((self.lineNo, char, "ERROR_TOKEN"))

            # if stopFlag value is true, every character will be accepted
            else:
                # String Checker
                if char == self.stopFlagValue:
                    # Adds the last char checked to buffer
                    self.buffer += char

                    # For ignoring escape chars and avoid immature halting of stopFlag
                    if self.buffer[-2] == '\\':
                        continue

                    # If stop value has been satisfied, stop flag is lifted and the buffer is tokenized
                    if char == self.stopFlagValue or char in self.stopFlagValue:
                        self.stopFlag = not self.stopFlag
                        self.tokenTable.append((self.lineNo, self.buffer, "STRING_LITERAL"))
                        self.BufferClear()

                # Comment Checker
                elif char == '/' and self.buffer[-1] == '/':
                    # Adds the last char checked to buffer
                    self.buffer += char

                    self.stopFlag = not self.stopFlag

                    # If it is a non-lexeme (ex. Comments), flips non lexeme bool but won't be tokenized
                    if self.buffer[-2:] == self.stopFlagValue:
                        self.nonLexeme = not self.nonLexeme
                        # self.tokenTable.append((self.lineNo, self.buffer, "COMMENT"))

                    self.BufferClear()

                # Decimal/Float Literal Checker
                elif char in self.stopFlagValue and '.' in self.buffer:

                    # Since stop value has been satisfied, stop flag is lifted
                    self.stopFlag = not self.stopFlag

                    # Tokenizes the buffer since we know it contains decimals
                    self.Tokenizer(self.lineNo, self.buffer)
                    self.BufferClear()

                    # Since we have a char in queue, check if it is not a space, do add, ignore otherwise
                    if not char.isspace():
                        self.buffer += char

                # if it reaches EOL/EOF without stop flag, tokenize and emit error token, usually for unclosed string
                elif self.charNo == self.lineLength:
                    self.buffer += char
                    self.Tokenizer(self.lineNo, self.buffer)
                    self.BufferClear()

                # if it is not any of the stop flag, adds to buffer
                else:
                    self.buffer += char

    def Tokenizer(self, lineNo, lexeme):

        # Check if buffer is a SPECIAL CHARACTER or an OPERATOR
        if (lexeme in DOUBLE_OPERATORS) or (lexeme in OPERATORS) or (lexeme in SPECIAL_CHARACTERS):
            self.SpecialCharTokenizer(lineNo, lexeme)

        # Check if buffer is a KEYWORD
        elif lexeme in KEYWORDS:
            self.tokenTable.append((lineNo, lexeme, KEYWORDS[lexeme]))

        # Check if buffer is an INT LITERAL
        elif lexeme.replace('.', '').isdigit():
            self.tokenTable.append((lineNo, lexeme, "NUM_LITERAL"))

        # Check if buffer is an IDENTIFIER
        elif lexeme.replace('_', '').isalnum() and lexeme[0].isalpha():
            self.tokenTable.append((lineNo, lexeme, "IDENTIFIER"))

        else:
            self.tokenTable.append((lineNo, lexeme, "ERROR_TOKEN"))

    def SpecialCharTokenizer(self, lineNo, charLexeme: str):

        if charLexeme in DOUBLE_OPERATORS:
            self.tokenTable.append((lineNo, charLexeme, DOUBLE_OPERATORS[charLexeme]))

        elif charLexeme in OPERATORS:
            self.tokenTable.append((lineNo, charLexeme, OPERATORS[charLexeme]))

        else:
            self.tokenTable.append((lineNo, charLexeme, SPECIAL_CHARACTERS[charLexeme]))

    def BufferClear(self):

        self.buffer = ''

    def ValidIdent(self, ident):
        return set(ident).issubset(IDENTIFIER)

    def LexerOutput(self):

        # removes the duplicates
        '''tokenTable = list(OrderedDict.fromkeys(self.tokenTable))

        for buffer in tokenTable:
            print(buffer)'''

        for lexeme in self.tokenTable:
            print(lexeme)


if __name__ == '__main__':
    lxc = Lexer()
    lxc.SourceToLexemes("C:\\Users\\Lenovo\\Documents\\GitHub\\LoomScript\\TestCase\\test3.loom")
    lxc.LexerOutput()

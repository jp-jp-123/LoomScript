from tokens import *
from charset import *
from collections import OrderedDict

'''
TODO:   Lexical Error Handling
'''


class Lexer:

    def __init__(self):
        self.tokenTable = []
        self.sourceCode = None

        self.lexemeBuffer = ''
        self.specialCharBuffer = ''

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

                    # Tokenizes the special buffer. This just means that the special char is a lexeme by itself
                    # and the special char can be tokenized now. Ex: +1
                    if self.specialCharBuffer:
                        self.Tokenizer(self.specialCharBuffer)
                        self.BufferClear('spc')

                    # Checks if the lexemeBuffer has contents and its first char
                    # Alphabet first char allows every character
                    # Digit first char only allows numbers, invalid lexeme otherwise. Also serves as Left-Hand of float
                    if self.lexemeBuffer:
                        if self.lexemeBuffer[0].isalpha():
                            self.lexemeBuffer += char

                        elif self.lexemeBuffer[0].isdigit():
                            if char.isdigit():
                                self.lexemeBuffer += char
                            else:
                                # We allow to add the illegal start of identifier, but we will tokenize as TOKEN_ERROR
                                # later
                                print(f'Illegal Character at Char no. {self.charNo}, Line no. {self.lineNo}: {lexemes}')
                                self.lexemeBuffer += char

                        else:
                            print("Undetermined Lexer Error")

                    # This just means that lexemeBuffer is empty and will accept any char
                    else:
                        self.lexemeBuffer += char

                    if char == lexemes[-1]:
                        self.Tokenizer(self.lexemeBuffer)
                        self.BufferClear('lxm')

                # Basic tokenizing technique. If it hits whitespace, all in the buffer is one token
                elif char.isspace():
                    if self.lexemeBuffer or self.specialCharBuffer:

                        # if a special buffer is found isolated in whitespaces, it is a single token
                        if self.specialCharBuffer:
                            self.Tokenizer(self.specialCharBuffer)
                        else:
                            self.Tokenizer(self.lexemeBuffer)
                    self.BufferClear()

                # Takes the special chars
                elif char in SPECIAL_CHARACTERS:

                    # If a special char is hit after taking an alphanum, it means it is a separate token
                    # ex: 1+ (1 gets tokenized, + goes to buffer)
                    if self.lexemeBuffer and char != '.':
                        self.Tokenizer(self.lexemeBuffer)
                        self.BufferClear('lxm')

                    # Checks the start for STRING_LITERAL
                    if char == '"' or char == '\'':
                        if char == '"':

                            # Checks if special char buffer contains anything, tokenizes it first then clears buffer
                            if self.specialCharBuffer:
                                self.Tokenizer(self.specialCharBuffer)
                                self.BufferClear('spc')

                            # flips stopFlag value, necessary to collect ALL the chars inside the string into the buffer
                            self.stopFlag = not self.stopFlag
                            self.stopFlagValue = '"'
                            self.specialCharBuffer += char

                        else:

                            # Checks if special char buffer contains anything, tokenizes it and clears buffer
                            if self.specialCharBuffer:
                                self.Tokenizer(self.specialCharBuffer)
                                self.BufferClear('spc')

                            # flips stopFlag value, necessary to collect ALL the chars inside the string into the buffer
                            self.stopFlag = not self.stopFlag
                            self.stopFlagValue = '\''
                            self.specialCharBuffer += char

                    # Checks if it hits a comment syntax, collects everything inside
                    elif char == '/' and self.specialCharBuffer == '/':
                        self.stopFlag = not self.stopFlag
                        self.stopFlagValue = '//'
                        self.nonLexeme = not self.nonLexeme
                        self.specialCharBuffer += char

                    # Checks the start for decimal
                    elif char == '.':

                        # Checks if special char buffer contains anything, tokenizes it and clears buffer
                        if self.specialCharBuffer:
                            self.Tokenizer(self.specialCharBuffer)
                            self.BufferClear('spc')

                        self.stopFlag = not self.stopFlag
                        self.stopFlagValue = NOT_IN_DECIMAL
                        self.specialCharBuffer += char

                    # Puts the special char in the buffer waiting for the following chars
                    else:

                        # if the special char has doubles, add to buffer
                        if self.specialCharBuffer or char in DOUBLES:
                            self.specialCharBuffer += char

                        # if the special char is not a double, tokenizes char
                        else:
                            self.Tokenizer(char)
                            self.BufferClear('spc')

                # Usually takes the illegal characters
                else:
                    print(f'Illegal Char at Char no. {self.charNo}, Line no. {self.lineNo}: {lexemes}')

                    # Block for Illegal Characters in Identifiers

                    # Tokenizes current buffer contents (if it contains anything) and clears it
                    if self.lexemeBuffer:
                        self.Tokenizer(self.lexemeBuffer)
                        self.BufferClear("lxm")

                    # Tokenizes the illegal character as error
                    self.tokenTable.append((char, "ERROR_TOKEN"))

            # if stopFlag value is true, adds to the special char buffer
            else:
                self.specialCharBuffer += char

                # Checks if it encounters a stop value (for lexemes that require single char to end) or
                # if the last 2 chars is a stop value (for comments e.g., //) or
                # if it reaches the end of line without matching a stop flag (will result in error)
                if char == self.stopFlagValue:

                    if self.specialCharBuffer[-2] == "\\":
                        print("in here")
                        continue

                    # Since stop value has been satisfied, stop flag is lifted
                    if char == self.stopFlagValue or char in self.stopFlagValue:
                        self.stopFlag = not self.stopFlag

                    # Check if the collected is a lexeme
                    if not self.nonLexeme:
                        if (('"' or '\'') == self.specialCharBuffer[0]) and (
                                ('"' or '\'') == self.specialCharBuffer[-1]):

                            # No need to call the tokenizer, understood to be a string_literal
                            self.tokenTable.append((self.specialCharBuffer, "STRING_LITERAL"))

                            self.BufferClear('spc')

                        else:
                            pass
                            # print(self.specialCharBuffer)

                # Comment Checker
                elif self.specialCharBuffer[-2:] == self.stopFlagValue:

                    self.stopFlag = not self.stopFlag

                    # If it is a non-lexeme (ex. Comments), flips non lexeme bool but won't be tokenized
                    if self.specialCharBuffer[-2:] == self.stopFlagValue:
                        self.nonLexeme = not self.nonLexeme

                    self.BufferClear('spc')

                # Decimal/Float Literal Checker
                elif (char in self.stopFlagValue or self.charNo == self.lineLength) and '.' == self.specialCharBuffer[
                    0]:
                    # Since stop value has been satisfied, stop flag is lifted
                    self.stopFlag = not self.stopFlag

                    # If it is a decimal, specialCharBuffer should start with decimal
                    # Since the stop value is already appended, we remove from the original string
                    # and re-assign it
                    lastChar = ''

                    if not self.specialCharBuffer[-1].isdigit():
                        lastChar = self.specialCharBuffer[-1]
                        self.specialCharBuffer = self.specialCharBuffer[:-1]

                    # If lexemesBuffer contains a left-hand side, join them and tokenize
                    if self.lexemeBuffer and self.lexemeBuffer.isdigit():
                        self.lexemeBuffer += self.specialCharBuffer
                        self.Tokenizer(self.lexemeBuffer)
                        self.BufferClear()

                    else:
                        self.Tokenizer(self.specialCharBuffer)
                        self.BufferClear()

                    # if the lastChar is not a space, add to buffer, ignore otherwise
                    if not lastChar.isspace():
                        self.specialCharBuffer += lastChar

                else:
                    pass
                    # print(self.specialCharBuffer)

    def Tokenizer(self, lexeme):

        # Check if lexemeBuffer is a SPECIAL CHARACTER or an OPERATOR
        if (lexeme in DOUBLE_OPERATORS) or (lexeme in OPERATORS) or (lexeme in SPECIAL_CHARACTERS):
            self.SpecialCharTokenizer(lexeme)

        # Check if lexemeBuffer is a KEYWORD
        elif lexeme in KEYWORDS:
            self.tokenTable.append((lexeme, KEYWORDS[lexeme]))

        # Check if lexemeBuffer is an INT LITERAL
        elif lexeme.replace('.', '').isdigit():
            self.tokenTable.append((lexeme, "NUM_LITERAL"))

        # Check if lexemeBuffer is an IDENTIFIER
        elif lexeme.replace('_', '').isalnum() and lexeme[0].isalpha():
            self.tokenTable.append((lexeme, "IDENTIFIER"))

        else:
            self.tokenTable.append((lexeme, "ERROR_TOKEN"))

    def SpecialCharTokenizer(self, charLexeme: str):

        if charLexeme in DOUBLE_OPERATORS:
            self.tokenTable.append((charLexeme, DOUBLE_OPERATORS[charLexeme]))

        elif charLexeme in OPERATORS:
            self.tokenTable.append((charLexeme, OPERATORS[charLexeme]))

        else:
            self.tokenTable.append((charLexeme, SPECIAL_CHARACTERS[charLexeme]))

    def BufferClear(self, clear='all'):

        if clear == 'lxm':
            self.lexemeBuffer = ''
        elif clear == 'spc':
            self.specialCharBuffer = ''
        else:
            self.lexemeBuffer = ''
            self.specialCharBuffer = ''

    def LexerOutput(self):

        # removes the duplicates
        '''tokenTable = list(OrderedDict.fromkeys(self.tokenTable))

        for lexemeBuffer in tokenTable:
            print(lexemeBuffer)'''

        for lexeme in self.tokenTable:
            print(lexeme)


if __name__ == '__main__':
    lxc = Lexer()
    lxc.SourceToLexemes("C:\\Users\\Lenovo\\Documents\\GitHub\\LoomScript\\LexicalAnalyser\\test.txt")
    lxc.LexerOutput()

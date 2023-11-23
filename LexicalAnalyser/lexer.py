from tokens import *
from charset import *
from collections import OrderedDict

'''
TODO:   Decimal parsing
        Lexical Error Handling

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
        self.commentFlag = '//'

        self.lineNo = 1
        self.charNo = 0

    def SourceToLexemes(self, filepath: str):

        with open(filepath) as file:
            self.sourceCode = file.readlines()

        # Feeds file to parser by line
        for perLine in self.sourceCode:
            # print(perLine)

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

                    self.lexemeBuffer += char

                    # Tokenizes the special buffer. This just means that the special char is a lexeme by itself
                    # and the special char can be tokenized now
                    if self.specialCharBuffer:
                        self.Tokenizer(self.specialCharBuffer)
                        self.BufferClear('spc')

                    if char == lexemes[-1]:
                        self.Tokenizer(self.lexemeBuffer)

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
                    if self.lexemeBuffer:
                        self.Tokenizer(self.lexemeBuffer)
                        self.BufferClear('lxm')

                    # Checks the start and end of STRING_LITERAL
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
                    if char == '/' and self.specialCharBuffer == '/':
                        self.stopFlag = not self.stopFlag
                        self.stopFlagValue = '//'
                        self.nonLexeme = not self.nonLexeme
                        self.specialCharBuffer += char
                        print(self.specialCharBuffer)

                    # Puts the special char in the buffer waiting for the following chars
                    else:

                        # if the special char has doubles, add to buffer
                        if self.specialCharBuffer or char in DOUBLES:
                            self.specialCharBuffer += char

                        # if the special char is not a double, tokenizes char
                        else:
                            self.Tokenizer(char)
                            self.BufferClear('spc')

                else:
                    print(f'Unidentified Token at Char no. {self.charNo}, Line no. {self.lineNo}: {lexemes}')

            # if stopFlag value is true, and is not a char, adds to the special char buffer
            else:
                self.specialCharBuffer += char

                # Checks if it encounters a stop value (for lexemes that require single char to end) or
                # if the last 2 chars is a stop value (for comments e.g., //)
                if (char == self.stopFlagValue) or (self.specialCharBuffer[-2:] == self.stopFlagValue):

                    # Since stop value has been satisfied, stop flag is lifted
                    self.stopFlag = not self.stopFlag

                    # Check if the collected is a lexeme
                    if not self.nonLexeme:
                        if '"' or '\'' == (self.specialCharBuffer[0] and self.specialCharBuffer[-1]):

                            # Tokenize the opening quote
                            self.Tokenizer(self.specialCharBuffer[0])

                            # No need to call the tokenizer, understood to be a string_literal
                            self.tokenTable.append((self.specialCharBuffer[2:-1], "STRING_LITERAL"))

                            # Tokenize the closing quote
                            self.Tokenizer(self.specialCharBuffer[-1])

                    # If it is a non-lexeme (ex. Comments), flips non lexeme bool but won't be tokenized
                    if self.specialCharBuffer[-2:] == self.stopFlagValue:
                        self.nonLexeme = not self.nonLexeme

                    self.BufferClear('spc')

    def Tokenizer(self, lexeme):

        # Check if lexemeBuffer is a SPECIAL CHARACTER or an OPERATOR
        if (lexeme in DOUBLE_OPERATORS) or (lexeme in OPERATORS) or (lexeme in SPECIAL_CHARACTERS):
            self.SpecialCharTokenizer(lexeme)

        # Check if lexemeBuffer is a KEYWORD
        elif lexeme in KEYWORDS:
            self.tokenTable.append((lexeme, "KEYWORD"))

        # Check if lexemeBuffer is an INT LITERAL
        elif lexeme.replace('_', '').isdigit():
            self.tokenTable.append((lexeme, "NUM_LITERAL"))

        # Check if lexemeBuffer is an IDENTIFIER
        elif lexeme.replace('_', '').isalnum():
            self.tokenTable.append((lexeme, "IDENTIFIER"))

        else:
            self.tokenTable.append((lexeme, "unidentified"))

    def BufferClear(self, clear='all'):

        if clear == 'lxm':
            self.lexemeBuffer = ''
        elif clear == 'spc':
            self.specialCharBuffer = ''
        else:
            self.lexemeBuffer = ''
            self.specialCharBuffer = ''

    def SpecialCharTokenizer(self, charLexeme: str):

        if charLexeme in DOUBLE_OPERATORS:
            self.tokenTable.append((charLexeme, "DOUBLE_OPERATOR"))

        elif charLexeme in OPERATORS:
            self.tokenTable.append((charLexeme, "OPERATOR"))

        else:
            self.tokenTable.append((charLexeme, "SPECIAL_CHAR"))

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

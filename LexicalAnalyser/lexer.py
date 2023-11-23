from tokens import *
from charset import *
from collections import OrderedDict
import re


class Lexer:

    def __init__(self):
        self.tokenTable = []
        self.sourceCode = None

        self.buffer = []

        self.lexemeBuffer = ''
        self.specialCharBuffer = ''

        self.stopFlag = False

    def SourceToLexemes(self, filepath: str):

        with open(filepath) as file:
            self.sourceCode = file.readlines()

        # Feeds file to parser by line
        for perLine in self.sourceCode:
            # print(perLine)

            self.LexemeParser(perLine)

    def LexemeParser(self, lexemes: str):

        for char in lexemes:

            # Mainly checks for identifiers, includes _ since it is a valid char for naming
            if (char.isalnum() or char == '_') and not self.stopFlag:

                self.lexemeBuffer += char

                # Tokenizes the special buffer. This just means that the special char is a lexeme by itself
                # and the special char can be tokenized now
                if self.specialCharBuffer:
                    self.Tokenizer(self.specialCharBuffer)
                    self.BufferClear('spc')

            # Basic tokenizing technique. If it hits whitespace, all in the buffer is one token
            elif char.isspace() and not self.stopFlag:
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
                        # flips stopFlag value, necessary to collect ALL the chars inside the string into the buffer
                        self.stopFlag = not self.stopFlag
                        self.specialCharBuffer += char

                        # if stopFlag is detected to be false, string has reached its end and can be tokenized
                        if not self.stopFlag:
                            self.specialCharBuffer += char
                            self.Tokenizer(self.specialCharBuffer)
                            self.BufferClear('spc')
                    else:
                        self.stopFlag = not self.stopFlag
                        self.specialCharBuffer += char
                        if not self.stopFlag:
                            self.specialCharBuffer += char
                            self.Tokenizer(self.specialCharBuffer)
                            self.BufferClear('spc')

                # Puts the special char in the buffer waiting for the following chars
                else:
                    # if the special chars has doubles, add to buffer
                    if self.specialCharBuffer or char in DOUBLES:
                        self.specialCharBuffer += char
                    else:
                        self.specialCharBuffer += char
                        self.Tokenizer(self.specialCharBuffer)
                        self.BufferClear('spc')

            # if stopFlag value is true, and is not a char, adds to the special char buffer
            else:
                self.specialCharBuffer += char

    def Tokenizer(self, lexeme):

        # Check if lexemeBuffer is a SPECIAL CHARACTER or an OPERATOR
        if (lexeme in DOUBLE_OPERATORS) or (lexeme in OPERATORS) or (lexeme in SPECIAL_CHARACTERS):
            self.SpecialCharTokenizer(lexeme)

        # Check if lexemeBuffer is a KEYWORD
        elif lexeme in KEYWORDS:
            self.tokenTable.append((lexeme, "KEYWORD"))

        # Check if lexemeBuffer is an INT LITERAL
        elif lexeme.isdigit():
            self.tokenTable.append((lexeme, "INT_LITERAL"))

        # Check if lexemeBuffer is an IDENTIFIER
        elif lexeme.replace('_', '').isalnum():
            self.tokenTable.append((lexeme, "IDENTIFIER"))

        elif ('"' in lexeme[0]) or ('\'' in lexeme[0]):
            self.tokenTable.append((lexeme, "STRING_LITERAL"))

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

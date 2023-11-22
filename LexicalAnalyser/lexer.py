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
            if char.isalnum() or char == '_':

                self.lexemeBuffer += char

                # Tokenizes in both buffers. This just means that the special chars and alphanums are separated
                if self.specialCharBuffer:
                    self.Tokenizer(self.specialCharBuffer)
                    self.Tokenizer(self.lexemeBuffer)
                    self.BufferClear()

            # Basic tokenizing technique. If it hits whitespace, all in the buffer is one token
            elif char.isspace():
                if not self.lexemeBuffer.isspace() and (self.lexemeBuffer or self.specialCharBuffer):

                    # if a special buffer is found isolated in whitespaces, it is a single token
                    if self.specialCharBuffer:
                        self.lexemeBuffer = self.specialCharBuffer
                    self.Tokenizer(self.lexemeBuffer)
                self.stopFlag = False
                self.BufferClear()

            # Takes the special chars
            elif char in SPECIAL_CHARACTERS:

                # If special char is hit after taking an alphanum, it means it is a separate token
                if not self.stopFlag:
                    self.stopFlag = True
                    if len(self.lexemeBuffer) != 0:
                        self.Tokenizer(self.lexemeBuffer)
                        self.BufferClear()

                # Puts the special char in the buffer waiting if a double operator is available, if not, gets tokenized
                self.specialCharBuffer += char

    def Tokenizer(self, lexeme):

        # Check if lexemeBuffer is a SPECIAL CHARACTER or an OPERATOR
        if lexeme in (DOUBLE_OPERATORS or OPERATORS or SPECIAL_CHARACTERS):
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

        else:
            self.tokenTable.append((lexeme, "unidentified"))

    def BufferClear(self):
        self.lexemeBuffer = ''
        self.specialCharBuffer = ''
    def SpecialCharTokenizer(self, charLexeme: str):

        if charLexeme in DOUBLE_OPERATORS:
            self.tokenTable.append((charLexeme, "DOUBLE_OPERATOR"))

        elif charLexeme in OPERATORS:
            self.tokenTable.append((charLexeme, "OPERATOR"))

        else:
            self.tokenTable.append((charLexeme, "SPECIAL_CHAR"))

    def Lookahead(self, inputStr: str, flag: str, peekLenght: int):

        lookaheadBuffer = []
        index = 0

        while index + peekLenght < len(inputStr) and flag != inputStr[index]:

            lookaheadBuffer.append(inputStr[index])

            index += 1

        return lookaheadBuffer

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

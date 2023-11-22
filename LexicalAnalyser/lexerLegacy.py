# Lexical Analyser for LoomScript
'''
TODO: times where code doesnt have space, ex:
        b=1+5
        OUTPUT("x is also less than 15")
        INPUT("get data")
'''

from tokens import *
from collections import OrderedDict
import re


class Lexer:

    def __init__(self):
        self.lookAheadFlag = ''
        self.startInstanceFound = False
        self.unparsedLexeme = []
        self.quote = 0  # tracks the number of quotation mark
        self.stringLiteralBuffer = []  # buffer array for string literals
        self.singleStringLiteralBufferActive = False  # single quotation string buffer checker
        self.doubleStringLiteralBufferActive = False  # double quotation string buffer checker
        self.buffer = []
        self.bufferActive = False
        self.tokenTable = []  # table for tokenized lexemes
        self.sourceCode = None  # source code

    # Gets the file to be fed to Lexer
    def SourceToLexemes(self, filepath: str):

        with open(filepath) as file:
            self.sourceCode = file.readlines()

        # Feeds file to parser by line
        for perLine in self.sourceCode:
            lexemes = perLine.strip().split()

            self.LexemeParser(lexemes)

    def CompoundLexemeParser(self, lexemeStr: str):
        # print("the lexemeBuffer: ", lexemeStr)
        # self.bufferActive = True
        lexeme = ""

        for char in lexemeStr:
            # print(char)
            if char.isalnum() or ('_' in char) or ('"' in char) or ('\'' in char):
                lexeme += char

            elif char in SPECIAL_CHARACTERS:
                # print(char)
                if lexeme:
                    # print(lexemeBuffer)
                    self.unparsedLexeme.append(lexeme)
                    lexeme = ""
                self.unparsedLexeme.append(char)

        if lexeme:
            # print("entering")
            self.unparsedLexeme.append(lexeme)

    # Parses the line of Lexemes into singular lexemeBuffer
    def LexemeParser(self, lexemes: list[str]):
        self.unparsedLexeme = []

        for lexeme in lexemes:
            if self.bufferActive:
                self.LookAhead('"', lexeme)
            else:
                self.Tokenizer(lexeme)

            if self.unparsedLexeme:
                self.LexemeParser(self.unparsedLexeme)
                self.unparsedLexeme = []

    # Tokenizing the lexemes happens here
    def Tokenizer(self, lexeme: str):

        print(lexeme)
        # Check if lexemeBuffer is a SPECIAL CHARACTER or an OPERATOR
        if lexeme in (SPECIAL_CHARACTERS or OPERATORS):
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

        # Check if lexemeBuffer is a STRING_LITERAL
        elif ('"' in lexeme[0] and '"' in lexeme[-1]) or ('\'' in lexeme[0] and '\'' in lexeme[-1]):
            self.StringLiteralDirector(lexeme)

        # Check if lexemeBuffer can't be tokenized/need more parsing
        else:
            if ('"' in lexeme):
                self.LookAhead('"', lexeme)
            else:
                self.CompoundLexemeParser(lexeme)

    # If the lexemeBuffer is a special character checks if it is an operator or not
    def SpecialCharTokenizer(self, charLexeme: str):

        if charLexeme in OPERATORS:
            self.tokenTable.append((charLexeme, "OPERATOR"))
        else:
            self.tokenTable.append((charLexeme, "SPECIAL_CHAR"))

    def StringLiteralDirector(self, lexeme):
        if '"' in lexeme or '\'' in lexeme:
            if '"' in lexeme:
                self.doubleStringLiteralBufferActive = True
                self.DoubleStringLiteralTokenizer(lexeme)
            else:
                self.singleStringLiteralBufferActive = True
                self.SingleStringLiteralTokenizer(lexeme)

    # Tokenizing the string literal happens here
    def DoubleStringLiteralTokenizer(self, lexeme: list[str]):

        string = ' '.join(lexeme)

        quotation = string[0]
        self.SpecialCharTokenizer(quotation)

        full_string = string.strip('"')
        self.tokenTable.append((full_string, "STRING_LITERAL"))

        self.ClearStringLiteralBuffer()

    def SingleStringLiteralTokenizer(self, lexeme: str):

        # Adds the lexemes to the string buffer while keeping track of quotations passed
        self.stringLiteralBuffer.append(lexeme)
        if '\'' in lexeme:
            self.quote += lexeme.count('\'')

        # Turns off the buffer if quotations reached two
        if self.quote == 2:
            string = ' '.join(self.stringLiteralBuffer)

            quotation = string[0]
            self.SpecialCharTokenizer(quotation)

            full_string = string.strip('\'')
            self.tokenTable.append((full_string, "STRING_LITERAL"))

            self.ClearStringLiteralBuffer()

    def ClearStringLiteralBuffer(self):

        self.singleStringLiteralBufferActive = False
        self.doubleStringLiteralBufferActive = False
        self.stringLiteralBuffer = []
        self.buffer = []
        self.quote = 0

    def LookAhead(self, flag: str, stack: str):

        self.bufferActive = True

        if flag in stack:
            if not self.startInstanceFound:
                self.buffer.append(stack)
                self.bufferActive = True
                self.startInstanceFound = True
            else:
                self.buffer.append(stack)
                self.bufferActive = False

        if flag not in stack:
            self.buffer.append(stack)

        if not self.bufferActive:
            self.DoubleStringLiteralTokenizer(self.buffer)

        # return self.buffer

    # Displays the lexer output
    def LexerOutput(self):

        # removes the duplicates
        tokenTable = list(OrderedDict.fromkeys(self.tokenTable))

        for lexeme in tokenTable:
            print(lexeme)


if __name__ == '__main__':
    lxc = Lexer()
    lxc.SourceToLexemes("C:\\Users\\Lenovo\\Documents\\GitHub\\LoomScript\\LexicalAnalyser\\test.txt")
    lxc.LexerOutput()

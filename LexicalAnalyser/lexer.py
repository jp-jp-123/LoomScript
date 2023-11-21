# Lexical Analyser for LoomScript
'''
TODO: times where code doesnt have space, ex: b=1+5
'''

from tokens import *
from collections import OrderedDict
import re


class Lexer:

    def __init__(self):
        self.quote = 0  # tracks the number of quotation mark
        self.stringLiteralBuffer = []  # Buffer array for string literals
        self.singleStringLiteralBufferActive = False    # single quotation string buffer checker
        self.doubleStringLiteralBufferActive = False    # double quotation string buffer checker
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

    # Parses the line of Lexemes into singular lexeme
    def LexemeParser(self, lexemes: list[str]):

        for lexeme in lexemes:
            # Checks if String Buffer is active
            if self.singleStringLiteralBufferActive:
                self.SingleStringLiteralTokenizer(lexeme)
            elif self.doubleStringLiteralBufferActive:
                self.DoubleStringLiteralTokenizer(lexeme)
            else:
                self.Tokenizer(lexeme)

    # Tokenizing the lexemes happens here
    def Tokenizer(self, lexeme: str):

        # Check if lexeme is a SPECIAL CHARACTER or an OPERATOR
        if lexeme in (SPECIAL_CHARACTERS or OPERATORS):
            self.SpecialCharTokenizer(lexeme)

        # Check if lexeme is a KEYWORD
        elif lexeme in KEYWORDS:
            self.tokenTable.append((lexeme, "KEYWORD"))

        # Check if lexeme is an INT LITERAL
        elif lexeme.isdigit():
            self.tokenTable.append((lexeme, "INT_LITERAL"))

        # Check if lexeme is an IDENTIFIER or a STRING_LITERAL
        elif re.match(r"(?<![\S'])([^'\s]+)(?![\S'])", lexeme) or re.match(r'(?<![\S"])([^"\s]+)(?![\S"])', lexeme):

            # if STRING_LITERAL
            if '"' in lexeme or '\'' in lexeme:
                if '"' in lexeme:
                    self.doubleStringLiteralBufferActive = True
                    self.DoubleStringLiteralTokenizer(lexeme)
                else:
                    self.singleStringLiteralBufferActive = True
                    self.SingleStringLiteralTokenizer(lexeme)

            # if IDENTIFIER
            else:
                self.tokenTable.append((lexeme, "IDENTIFIER"))

        else:
            print(lexeme, "Untokenized")

    # If the lexeme is a special character checks if it is an operator or not
    def SpecialCharTokenizer(self, charLexeme: str):

        if charLexeme in OPERATORS:
            self.tokenTable.append((charLexeme, "OPERATOR"))
        else:
            self.tokenTable.append((charLexeme, "SPECIAL_CHAR"))

    # Tokenizing the string literal happens here
    def DoubleStringLiteralTokenizer(self, lexeme: str):

        # Adds the lexemes to the string buffer while keeping track of quotations passed
        self.stringLiteralBuffer.append(lexeme)
        if '"' in lexeme:
             self.quote += lexeme.count('"')

        # Turns off the buffer if quotations reached two
        if self.quote == 2:
            string = ' '.join(self.stringLiteralBuffer)

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
        self.stringLiteralBuffer = []
        self.quote = 0

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

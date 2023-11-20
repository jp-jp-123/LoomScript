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
        self.stringLiteralBufferActive = False  # Checks if the string literal array buffer is active
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
            if self.stringLiteralBufferActive:
                self.StringLiteralTokenizer(lexeme)
            else:
                self.Tokenizer(lexeme)

    # Tokenizing the lexemes happens here
    def Tokenizer(self, lexeme: str):

        # Check if lexeme is a SPECIAL CHARACTER or an OPERATOR
        if lexeme in SPECIAL_CHARACTERS or OPERATORS:
            self.SpecialCharTokenizer(lexeme)

        # Check if lexeme is a KEYWORD
        elif lexeme in KEYWORDS:
            self.tokenTable.append((lexeme, "KEYWORD"))

        # Check if lexeme is an IDENTIFIER or a STRING_LITERAL
        elif re.match(r"(?<![\S'])([^'\s]+)(?![\S'])", lexeme):

            # if STRING_LITERAL
            # TODO: single quotation string cant be read
            if ('"' or "'") in lexeme:
                self.stringLiteralBufferActive = True
                self.StringLiteralTokenizer(lexeme)

            # if IDENTIFIER
            else:
                self.tokenTable.append((lexeme, "IDENTIFIER"))

        # Check if lexeme is an INT LITERAL
        # TODO: fix the lexeme where ints are identified as IDENTIFIERS
        elif lexeme.isdigit():
            self.tokenTable.append((lexeme, "INT_LITERAL"))

    # If the lexeme is a special character checks if it is an operator or not
    def SpecialCharTokenizer(self, charLexeme: str):

        if charLexeme in OPERATORS:
            self.tokenTable.append((charLexeme, "OPERATOR"))
        else:
            self.tokenTable.append((charLexeme, "SPECIAL_CHAR"))

    # Tokenizing the string literal happens here
    def StringLiteralTokenizer(self, lexeme: str):

        # Adds the lexemes to the string buffer while keeping track of quotations passed
        # TODO: edge cases for quotations inside quotations exists
        self.stringLiteralBuffer.append(lexeme)
        if ('"' or "'") in lexeme:
            self.quote += 1

        # Turns off the buffer if quotations reached two
        if self.quote == 2:
            string = ' '.join(self.stringLiteralBuffer)

            quotation = string[0]
            self.SpecialCharTokenizer(quotation)

            full_string = string.strip('"')
            self.tokenTable.append((full_string, "STRING_LITERAL"))

            quotation = string[-1]
            self.SpecialCharTokenizer(quotation)

            self.stringLiteralBufferActive = False
            self.quote = 0

    # Displays the lexer output
    def LexerOutput(self):

        # removes the duplicates
        tokenTable = list(OrderedDict.fromkeys(self.tokenTable))

        print(tokenTable)


if __name__ == '__main__':
    lxc = Lexer()
    lxc.SourceToLexemes("C:\\Users\\Lenovo\\Documents\\GitHub\\LoomScript\\LexicalAnalyser\\test.txt")
    lxc.LexerOutput()

# Lexical Analyser for LoomScript

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

    def SourceToLexemes(self, filepath: str):
        with open(filepath) as file:
            self.sourceCode = file.readlines()

        for perLine in self.sourceCode:
            lexemes = perLine.strip().split()

            self.LexemeParser(lexemes)

    def LexemeParser(self, lexemes: list[str]):

        for lexeme in lexemes:
            if self.stringLiteralBufferActive:
                self.StringLiteralTokenizer(lexeme)
            else:
                self.Tokenizer(lexeme)

    def Tokenizer(self, lexeme: str):

        # Check if lexeme is a SPECIAL CHARACTER
        if lexeme in SPECIAL_CHARACTERS:
            self.SpecialCharTokenizer(lexeme)

        # Check if lexeme is a KEYWORD
        elif lexeme in KEYWORDS:
            self.tokenTable.append((lexeme, "KEYWORD"))

        # Check if lexeme is an IDENTIFIER or a STRING_LITERAL
        elif re.match(r"(?<![\S'])([^'\s]+)(?![\S'])", lexeme):

            # if STRING_LITERAL
            if ('"' or "'") in lexeme:
                self.stringLiteralBufferActive = True
                self.StringLiteralTokenizer(lexeme)

            # if IDENTIFIER
            else:
                self.tokenTable.append((lexeme, "IDENTIFIER"))

        # Check if lexeme is an INT LITERAL
        elif lexeme.isdigit():
            self.tokenTable.append((lexeme, "INT_LITERAL"))

    def SpecialCharTokenizer(self, charLexeme: str):

        if charLexeme in OPERATORS:
            self.tokenTable.append((charLexeme, "OPERATOR"))
        else:
            self.tokenTable.append((charLexeme, "SPECIAL_CHAR"))

    def StringLiteralTokenizer(self, lexeme: str):
        self.stringLiteralBuffer.append(lexeme)
        if ('"' or "'") in lexeme:
            self.quote += 1

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

    def LexerOutput(self):
        k = list(OrderedDict.fromkeys(self.tokenTable))

        print(k)


if __name__ == '__main__':
    lxc = Lexer()
    lxc.SourceToLexemes("C:\\Users\\Lenovo\\Documents\\GitHub\\LoomScript\\LexicalAnalyser\\test.txt")
    lxc.LexerOutput()

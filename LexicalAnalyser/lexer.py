# Lexical Analyser for LoomScript

from tokens import *
import re


class Lexer:

    def __init__(self):
        self.stringLiteralBuffer = []   # Buffer array for string literals
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

        if ('"' or '\'') in lexeme:
            self.stringLiteralBufferActive = True
            self.stringLiteralBuffer.append(lexeme)

        # Check if lexeme is a SPECIAL CHARACTER
        if lexeme in SPECIAL_CHARACTERS:
            self.SpecialCharTokenizer(lexeme)

        # Check if lexeme is a KEYWORD
        elif lexeme in KEYWORDS:
            self.tokenTable.append((lexeme, "KEYWORD"))

        # Check if lexeme is an IDENTIFIER
        elif re.match(r"(?<![\S'])([^'\s]+)(?![\S'])", lexeme):
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
        quote = 0
        # while quote < 2:
        self.stringLiteralBuffer.append(lexeme)
        if ('"' or '\'') in lexeme:
            quote += 1
            print(quote)

        if quote == 2:
            string = ' '.join(self.stringLiteralBuffer)
            self.tokenTable.append((string, "STRING_LITERAL"))
            self.stringLiteralBufferActive = False


    def LexerOutput(self):
        print(self.tokenTable)


if __name__ == '__main__':
    lxc = Lexer()
    lxc.SourceToLexemes("C:\\Users\\Lenovo\\Documents\\GitHub\\LoomScript\\LexicalAnalyser\\test.txt")
    lxc.LexerOutput()

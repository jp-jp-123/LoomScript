from LexicalAnalyser import lexer

# k = lexer.Lexer()
# k.SourceToLexemes("C:\\Users\\Lenovo\\Documents\\GitHub\\LoomScript\\TestCase\\test.loom")
# outs = k.tokenTable


class Synter:
    def __init__(self):
        self.lexerOut = None
        self.outs = None

    def Test(self, fpath):
        self.lexerOut = lexer.Lexer()
        self.lexerOut.SourceToLexemes(fpath)
        self.outs = self.lexerOut.tokenTable


if __name__ == '__main__':
    path = "C:\\Users\\Lenovo\\Documents\\GitHub\\LoomScript\\TestCase\\test.loom"
    main = Synter()
    main.Test(path)

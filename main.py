from LexicalAnalyser import lexer


class Main:

    def __init__(self):
        self.src = "TestCase/test.loom"

        self.lxc = lexer.Lexer()
        self.lxc.SourceToLexemes(self.src)

        self.outs = self.lxc.tokenTable

    def CheckFileExtension(self):
        if self.src.endswith('.loom'):
            self.WriteFile()
        else:
            print("Wrong File Format")

    def WriteFile(self):
        try:
            # Open the file in write mode
            with open('SymbolTable.txt', 'w') as file:
                # Write each item in the list to a new line
                file.write("Lexeme".ljust(40) + "Token\n")

                for x in range(50):
                    file.write("=")

                file.write("\n")

                for item in self.outs:
                    file.write(f"{item[0]}".ljust(40) + f"{item[1]}\n")

                file.close()

            print(f"Successfully Written to {self.src}")

        except Exception as e:
            print("Error Found", e)


if __name__ == '__main__':
    main = Main()
    main.CheckFileExtension()

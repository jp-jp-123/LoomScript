from LexicalAnalyser import lexer
import os


class Main:

    def __init__(self):
        self.outs = None
        self.lxc = None
        self.src = "TestCase/test.loom"
        self.dest = 'SymbolTable.txt'

    def CheckFileExtension(self):
        if os.path.isfile(self.src):
            if self.src.endswith('.loom'):
                self.lxc = lexer.Lexer()
                self.lxc.SourceToLexemes(self.src)

                self.outs = self.lxc.tokenTable
                self.WriteFile()
            else:
                print("Wrong File Format")

        else:
            print("File Doesn't Exist!")

    def WriteFile(self):
        try:
            # Open the file in write mode
            with open(self.dest, 'w') as file:
                # Write each item in the list to a new line
                file.write("Line No.".ljust(20) + "Lexeme".ljust(40) + "Token\n")

                for x in range(70):
                    file.write("=")

                file.write("\n")

                for item in self.outs:
                    file.write(f"{item[0]}".ljust(20) + f"{item[1]}".ljust(40) + f"{item[2]}\n")

                file.close()

            print(f"Successfully Written to {self.dest}")

        except Exception as e:
            print("Error Found", e)


if __name__ == '__main__':
    main = Main()
    main.CheckFileExtension()

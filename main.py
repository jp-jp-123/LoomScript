from LexicalAnalyser import lexer
import os
import csv


class Main:

    def __init__(self):
        self.outs = None
        self.lxc = None
        self.src = "TestCase/test1.loom"
        self.dest = 'SymbolTable.txt'
        self.destcsv = 'SymbolTable.csv'

    def CheckFileExtension(self):
        if os.path.isfile(self.src):
            if self.src.endswith('.loom'):
                self.lxc = lexer.Lexer()
                self.lxc.SourceToLexemes(self.src)

                self.outs = self.lxc.tokenTable
                self.Driver()
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

    def WriteCSV(self):
        try:
            # Open the file in write mode
            with open(self.destcsv, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['lineNo', 'Lexeme', 'Token'])
                writer.writerows(self.outs)

            print(f"Successfully Written to {self.destcsv}")

        except Exception as e:
            print("Error Found", e)

    def Driver(self):
        i = input("Write to Formatted .txt? N=No, Any Other Keys=Yes: ")

        if i == 'N' or i == 'n':
            self.WriteCSV()

        else:
            self.WriteCSV()
            self.WriteFile()


if __name__ == '__main__':
    main = Main()
    main.CheckFileExtension()

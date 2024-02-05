from SyntacticalAnalyser import synter3
from LexicalAnalyser import lexer
import os
import csv


class Main:

    def __init__(self):
        self.outs = None
        self.lxc = None
        self.src = "TestCase/test3.loom"
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

                file.write('=' * 150)

                file.write("\n")

                # set wrap width
                import textwrap

                # Define the width for each column
                column_widths = [20, 100, 10]

                # Format and write each item to the file
                for item in self.outs:
                    # Format and wrap the second column (Value)
                    wrapped_value = textwrap.fill(str(item[1]), width=column_widths[1])

                    # Write the formatted item to the file
                    file.write(
                        f"{str(item[0]):<{column_widths[0]}} {wrapped_value:<{column_widths[1]}} {str(item[2]):<{column_widths[2]}}\n")

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

    def RunSynter(self):
        main_synter = synter3.Synter()
        parser = main_synter.Parse(self.src)

        if parser is not None:
            print("Parse Tree Successfully Generated")
            i = input("Print parse tree?  N=No, Any Other Keys=Yes: ")

            if i == 'N' or i == 'n':
                return

            else:
                print(parser)

        return

    def Driver(self):
        i = input("Write to Formatted .txt? N=No, Any Other Keys=Yes: ")

        if i == 'N' or i == 'n':
            self.WriteCSV()
            self.RunSynter()

        else:
            self.WriteCSV()
            self.WriteFile()
            self.RunSynter()


if __name__ == '__main__':
    main = Main()
    main.CheckFileExtension()

import parser
import scanner
import sys
import translator

def main():
    source = ""
    # open source file if supplied
    if len(sys.argv) > 1 and len(sys.argv) < 3:
        input_file = open(sys.argv[1])
        output_file = "a.py"
        source = input_file.read()
        s = scanner.Scanner(source)
        s.split_into_lexemes()
        if s.define_tokens() == False:
            print("Error: No match for Token")
            return

        for token in s.tokens:
            p = parser.Parser(s.tokens)

        # copy library to output_file
        standard_library = open("library/standard.py", "r")
        destination_file = open("a.py", "w")
        library = standard_library.readlines()
        destination_file.writelines(library)
        standard_library.close()
        destination_file.close()

        t = translator.Translator(output_file, s.tokens)
        t.translate()

if __name__=="__main__":
    main()

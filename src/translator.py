import scanner

class Translator:
    def __init__(self, python_file, tokens):
        self.index = 0
        self.num_parentheses = 0 # measures the indent level
        self.python_file = python_file # default is a.py
        self.tokens = tokens
        self.output_file = open(self.python_file, "w")

    def def_operator(self):
        print("def operator")
        print(self.num_parentheses)
        self.output_file.write("def ")
        self.index += 1
        self.output_file.write(self.replace_dash(self.index))
        self.output_file.write("(")
        self.index += 2

        # if there are no arguments
        if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
            self.output_file.write("):")
            self.output_file.write("\n\t")
            self.index += 1
        # if there are arguments
        elif self.tokens[self.index + 1].token_type == scanner.TokenType.LEFT_PAREN:
            self.index += 2
            while True:
                self.output.write(self.tokens[self.index].literal)
                self.index += 1
                # if we're at the end of the arguments
                if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
                    self.num_parentheses -= 1
                    self.index += 1
                    break
        self.translate()

    def import_operator(self):
        print("import_operator")
        self.index += 1
        while True:
            self.output_file.write(" ")
            self.output_file.write(self.tokens[self.index].literal)
            self.index += 1
            if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
                self.num_parentheses -= 1
                self.index += 1
                break
            else:
                self.output_file.write(", ")
        self.output_file.write("\n")

    def binary_operator(self):
        print("binary operator")
        operator = []
        operator.append(self.tokens[self.index].literal)
        self.output_file.write("(")
        self.index += 1
        while True:
            if self.tokens[self.index].token_type == scanner.TokenType.NUMBER or self.tokens[self.index].token_type == scanner.TokenType.IDENTIFIER:
                self.output_file.write(self.tokens[self.index].literal)
                self.index += 1
                if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
                    self.output_file.write(")")
                    self.num_parentheses -= 1
                    self.index += 1
                    operator.pop()
                    if self.num_parentheses == 0:
                        self.output_file.write("\n")
                        break
                    elif self.tokens[self.index].token_type == scanner.TokenType.NUMBER or self.tokens[self.index].token_type == scanner.TokenType.IDENTIFIER:
                        self.output_file.write(" " + operator[-1] + " ")
                elif self.tokens[self.index].token_type == scanner.TokenType.LEFT_PAREN:
                    # we know that this is after an argument
                    self.output_file.write(" " + operator[-1] + " ")
                    self.output_file.write("(")
                    self.num_parentheses += 1
                    self.index += 1
                    if self.tokens[self.index].token_type == scanner.TokenType.BINARY_OPERATOR:
                        operator.append(self.tokens[self.index].literal)
                        self.index += 1
                else:
                    self.output_file.write(" " + operator[-1] + " ")
        self.translate()


    def identifier(self):
        print("identifier")
        self.output_file.write(self.replace_dash(self.index))
        self.output_file.write("(")
        self.index += 1
        while True:
            print("while identifier")
            print(self.num_parentheses)
            if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN and self.num_parentheses <= 1:
                print("exiting identifier")
                self.output_file.write(")")
                self.num_parentheses -= 1
                self.index += 1
                self.output_file.write("\n")
                break
            elif self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
                # let's see how this flys in the future
                if self.num_parentheses == 2:
                    self.index += 1
                    self.num_parentheses -= 1
                else:
                    self.output_file.write(")")
                    self.index += 1
                    self.num_parentheses -= 1
            else:
                self.output_file.write(self.replace_dash(self.index))
                self.index += 1
                if self.tokens[self.index].token_type != scanner.TokenType.RIGHT_PAREN:
                    self.output_file.write(", ")

        self.translate()

    def quote_operator(self):
        self.index += 2
        self.output_file.write("[")
        while True:
            self.output_file.write(self.tokens[self.index].literal)
            if self.tokens[self.index + 1].token_type == scanner.TokenType.RIGHT_PAREN:
                self.output_file.write("]")
                self.index += 2
                break
            else:
                self.output_file.write(", ")
                self.index += 1
        self.translate()

    def translate(self):
        print("translate")
        print(self.num_parentheses)
        print(self.tokens[self.index].literal)
        # LEFT PARENTHESES
        if self.tokens[self.index].token_type == scanner.TokenType.LEFT_PAREN:
            print("left paren")
            self.num_parentheses += 1
            self.index += 1
            print(self.num_parentheses)

        # RIGHT PARENTHESES
        elif self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
            print("right paren")
            self.num_parentheses -= 1
            self.index += 1

        # DEFINE OPERATOR
        # (define IDENTIFIER ()) => def IDENTIFIER():
        # (define IDENTFIER (ARGUMENT, ...)) => def IDENTIFIER(ARGUMENT, ...):
        # TODO: (define IDENTIFIER VALUE(S) => IDENTIFIER = VALUE(S))
        if self.tokens[self.index].token_type == scanner.TokenType.DEF_OPERATOR:
            self.def_operator()

        # IMPORT OPERATOR
        # (import ARGUMENT) => import argument
        # (import ARGUMENT, ...) => import argument, ...
        elif self.tokens[self.index].token_type == scanner.TokenType.IMPORT_OPERATOR:
            self.import_operator()
        # BINARY OPERATOR
        # (BIN_OP ARGUMENT, ARGUMENT, ...) => (ARGUMENT, BIN_OP ARGUMENT, ...)
        elif self.tokens[self.index].token_type == scanner.TokenType.BINARY_OPERATOR:
            self.binary_operator()

        # IDENTIFIER
        # (IDENTIFIER ARGUMENT) => IDENTIFIER(ARGUMENT)
        # (IDENTIFIER ARGUMENT ...) => IDENTIFIER(ARGUMENT, ...)
        elif self.tokens[self.index].token_type == scanner.TokenType.IDENTIFIER:
            self.identifier()

        elif self.tokens[self.index].token_type == scanner.TokenType.EOF:
            return

    def newline_check(self, index):
        if self.tokens[index].line - self.tokens[index-1].line == 1:
            return True
        else:
            return False

    def replace_dash(self, index):
        return self.tokens[index].literal.replace("-", "_")


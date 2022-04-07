import scanner

class Translator:
    def __init__(self, python_file, tokens):
        self.index = 0
        #self.num_parentheses = 0 # measures the indent level
        self.python_file = python_file # default is a.py
        self.tokens = tokens
        self.output_file = open(self.python_file, "w")

    def define_operator(self, from_function):
        print("define operator")
        #self.output_file.write("def ")
        self.index += 1
        self.output_file.write(self.replace_dash(self.index))
        self.output_file.write(" = ")
        self.index += 1
        #self.output_file.write("(")
        #self.index += 2

        # lambda, number, identifier, list
        # lambda
        if self.tokens[self.index].token_type == scanner.TokenType.LEFT_PAREN:
            self.index += 1
            if self.tokens[self.index].token_type == scanner.TokenType.LAMBDA_OPERATOR:
                self.output_file.write("lambda ")
                self.index += 2 # skip left paren
                # there are no arguments to the function
                if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
                    self.output_file.write(": ")
                    self.index += 1
                else:  # if there are arguments
                    while True:
                        if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
                            self.index += 1
                            break
                        self.output.write(self.tokens[self.index].literal)
                        self.index += 1
                        # if we're at the end of the arguments

        self.translate("define")
        # if there are no arguments
        #if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
            #self.output_file.write(" = ")
            #self.output_file.write("):")
            #self.output_file.write("\n\t")
            #self.index += 1
        # if there are arguments
        #elif self.tokens[self.index + 1].token_type == scanner.TokenType.LEFT_PAREN:
            #self.index += 2
            #while True:
                #self.output.write(self.tokens[self.index].literal)
                #self.index += 1
                # if we're at the end of the arguments
                #if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
                #    self.num_parentheses -= 1
                #E    self.index += 1
                #    break

    def import_operator(self, from_function):
        print("import_operator")
        while True:
            self.output_file.write(self.tokens[self.index].literal)
            self.index += 1
            self.output_file.write(" ")
            self.output_file.write(self.tokens[self.index].literal)
            self.index += 1
            if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
                self.index += 1
                self.output_file.write("\n")
                break
            else:
                self.output_file.write(", ")
        self.translate("import")

    def binary_operator(self, from_function):
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
                    self.index += 1
                    operator.pop()
                    if self.tokens[self.index].token_type == scanner.TokenType.NUMBER or self.tokens[self.index].token_type == scanner.TokenType.IDENTIFIER:
                        self.output_file.write(" " + operator[-1] + " ")
                elif self.tokens[self.index].token_type == scanner.TokenType.LEFT_PAREN:
                    # we know that this is after an argument
                    self.output_file.write(" " + operator[-1] + " ")
                    self.output_file.write("(")
                    self.index += 1
                    if self.tokens[self.index].token_type == scanner.TokenType.BINARY_OPERATOR:
                        operator.append(self.tokens[self.index].literal)
                        self.index += 1
                else:
                    self.output_file.write(" " + operator[-1] + " ")
            else:
                if from_function == "identifier":
                    self.output_file.write(")")
                    pass
                self.output_file.write("\n")
                break
        self.translate("binary")


    def identifier(self, from_function):
        print("identifier")
        self.output_file.write(self.replace_dash(self.index))
        self.output_file.write("(")
        self.index += 1
        #for token in self.tokens:
            #print(token.token_type)
        while True:
            print("while identifier")
            if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN and self.tokens[self.index+1].token_type == scanner.TokenType.LEFT_PAREN:
                print("exiting identifier")
                if from_function != "define":
                    self.output_file.write(")")
                self.index += 1
                self.output_file.write("\n")
                break
            elif self.tokens[self.index].token_type == scanner.TokenType.EOF:
                break
            elif self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
                # let's see how this flies in the future
                self.index += 1
                self.output_file.write(")")
            elif self.tokens[self.index].token_type == scanner.TokenType.BINARY_OPERATOR:
                self.binary_operator("identifier")
            elif self.tokens[self.index].token_type == scanner.TokenType.LEFT_PAREN:
                #self.output_file.write("(")
                self.index += 1
            else:
                self.output_file.write(self.replace_dash(self.index))
                self.index += 1
                if self.tokens[self.index].token_type != scanner.TokenType.RIGHT_PAREN:
                    self.output_file.write(", ")

        self.translate("identifier")

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
        self.translate("quote")

    def translate(self, from_function=""):
        print("translate")
        print(self.tokens[self.index].literal)
        # LEFT PARENTHESES
        if self.tokens[self.index].token_type == scanner.TokenType.LEFT_PAREN:
            print("left paren")
            self.index += 1

        # RIGHT PARENTHESES
        elif self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
            print("right paren")
            self.index += 1

        # DEFINE OPERATOR
        # (define IDENTIFIER ()) => def IDENTIFIER():
        # (define IDENTFIER (ARGUMENT, ...)) => def IDENTIFIER(ARGUMENT, ...):
        # TODO: (define IDENTIFIER VALUE(S) => IDENTIFIER = VALUE(S))
        if self.tokens[self.index].token_type == scanner.TokenType.DEFINE_OPERATOR:
            self.define_operator(from_function)

        # IMPORT OPERATOR
        # (import ARGUMENT) => import argument
        # (import ARGUMENT, ...) => import argument, ...
        elif self.tokens[self.index].token_type == scanner.TokenType.IMPORT_OPERATOR:
            self.import_operator(from_function)
        # BINARY OPERATOR
        # (BIN_OP ARGUMENT, ARGUMENT, ...) => (ARGUMENT, BIN_OP ARGUMENT, ...)
        elif self.tokens[self.index].token_type == scanner.TokenType.BINARY_OPERATOR:
            self.binary_operator(from_function)

        # IDENTIFIER
        # (IDENTIFIER ARGUMENT) => IDENTIFIER(ARGUMENT)
        # (IDENTIFIER ARGUMENT ...) => IDENTIFIER(ARGUMENT, ...)
        elif self.tokens[self.index].token_type == scanner.TokenType.IDENTIFIER:
            self.identifier(from_function)

        elif self.tokens[self.index].token_type == scanner.TokenType.QUOTE_OPERATOR:
            self.quote_operator(from_function)

        elif self.tokens[self.index].token_type == scanner.TokenType.EOF:
            return

    def newline_check(self, index):
        if self.tokens[index].line - self.tokens[index-1].line == 1:
            return True
        else:
            return False

    def replace_dash(self, index):
        return self.tokens[index].literal.replace("-", "_")


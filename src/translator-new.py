import scanner

class Translator:
    def __init__(self, python_file, tokens):
        self.index = 0
        self.num_parentheses = 0 # measures the indent level
        self.python_file = python_file # default is a.py
        self.tokens = tokens
        self.output_file = open(self.python_file, "w")

    def def_operator(self):
        self.output_file.write("def ")
        self.index += 1
        self.output_file.write("(")
        self.index += 2 # skip over extra tokens

        # if there are no arguments
        if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
            self.output_file.write("):")
            self.newline_and_scope_insert()
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

    def translate(self):
        # LEFT PARENTHESES
        if self.tokens[self.index].token_type == scanner.TokenType.LEFT_PAREN:
            self.left_paren()
            continue

        # RIGHT PARENTHESES
        elif self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
            self.right_paren()
            continue

        # DEFINE OPERATOR
        # (define IDENTIFIER ()) => def IDENTIFIER():
        # (define IDENTFIER (ARGUMENT, ...)) => def IDENTIFIER(ARGUMENT, ...):
        # TODO: (define IDENTIFIER VALUE(S) => IDENTIFIER = VALUE(S))
        elif self.tokens[self.index].token_type == scanner.TokenType.DEF_OPERATOR:
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

    def left_paren(self):
        self.num_parentheses += 1
        self.index += 1

    def newline_check(self, index):
        if self.tokens[index].line - self.tokens[index-1].line == 1:
            return True
        else:
            return False

    def newline_and_scope_insert(self):
        self.output_file.write("\n\t")

    def replace_dash(self, index):
        return self.tokens[index].literal.replace("-", "_")

    def right_paren(self):
        self.num_parentheses -= 1
        self.index += 1

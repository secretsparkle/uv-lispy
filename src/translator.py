import scanner

class Translator:
    def __init__(self, python_file, tokens):
        self.index = 0
        self.output_file = ""
        self.num_parentheses = 0 # measures the indent level
        self.python_file = python_file # default is a.py
        self.tokens = tokens

    # DEFINE OPERATOR
    # (define IDENTIFIER ()) => def IDENTIFIER():
    # (define IDENTFIER (ARGUMENT, ...)) => def IDENTIFIER(ARGUMENT, ...):
    # TODO: (define IDENTIFIER VALUE(S) => IDENTIFIER = VALUE(S))
    def def_operator(self):
        self.output_file.write("def ")
        self.index += 1
        self.output_file.write(self.replace_dash(self.index))
        self.output_file.write("(")
        self.index += 2 # skip over left parenthesis
        if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN: # if there are no arguments
            self.output_file.write("):")
            self.newline_and_scope_insert()
        elif self.tokens[self.index + 1].token_type == scanner.TokenType.LEFT_PAREN: # if there are arguments
            self.index += 2
            while True:
                self.output_file.write(self.tokens[self.index].literal)
                self.index += 1
                # if we've reached the end of the arguments
                if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
                    self.num_parentheses -= 1
                    self.index += 1
                    break
        else:
            self.output_file.write(", ")
            self.output_file.write("):")
            self.newline_and_scope_insert()

    # IMPORT OPERATOR
    # (import ARGUMENT) => import argument
    # (import ARGUMENT, ...) => import argument, ...
    def import_operator(self):
        self.output_file.write("import")
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

    # BINARY OPERATOR
    # (BIN_OP ARGUMENT, ARGUMENT, ...) => (ARGUMENT, BIN_OP ARGUMENT, ...)
    def binary_operator(self):
        operator = []
        operator.append(self.tokens[self.index].literal)
        self.output_file.write("(") # these will always be in parentheses
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

    # IDENTIFIER
    # (IDENTIFIER ARGUMENT) => IDENTIFIER(ARGUMENT)
    # (IDENTIFIER ARGUMENT ...) => IDENTIFIER(ARGUMENT, ...)
    def identifier(self):
        self.output_file.write(self.replace_dash(self.index))
        self.output_file.write("(")
        self.index += 1 # skip over next left parenthesis
        while True:
            if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
                self.num_parentheses -= 1
                self.output_file.write(")")
                self.index += 1
                if self.num_parentheses > 0 and self.tokens[self.index].token_type != scanner.TokenType.RIGHT_PAREN:
                    self.output_file.write(", ")
                if self.num_parentheses > 0:
                    self.output_file.write(" ")
                else:
                    self.output_file.write("\n")
                    self.num_parentheses = 0
                    break
            elif self.tokens[self.index].token_type == scanner.TokenType.LEFT_PAREN:
                if self.tokens[self.index+1].token_type == scanner.TokenType.BINARY_OPERATOR:
                    bin_op = True
                    self.output_file.write("(") # these will always be in parentheses
                    operator = []
                    self.index += 1
                    operator.append(self.tokens[self.index].literal)
                    num_paren_bin_expr = 2
                    self.index += 1
                    while True:
                        if self.tokens[self.index].token_type == scanner.TokenType.NUMBER or self.tokens[self.index].token_type == scanner.TokenType.IDENTIFIER:
                            self.output_file.write(self.tokens[self.index].literal)
                            self.index += 1
                            if self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
                                self.output_file.write(")")
                                num_paren_bin_expr -= 1
                                self.index += 1
                                operator.pop()
                                if num_paren_bin_expr == 0:
                                    self.output_file.write("\n")
                                    break
                                elif self.tokens[self.index].token_type == scanner.TokenType.NUMBER or self.tokens[self.index].token_type == scanner.TokenType.IDENTIFIER:
                                    self.output_file.write(" " + operator[-1] + " ")
                            elif self.tokens[self.index].token_type == scanner.TokenType.LEFT_PAREN:
                                # we know that this is after an argument
                                self.output_file.write(" " + operator[-1] + " ")
                                self.output_file.write("(")
                                num_paren_bin_expr += 1
                                self.index += 1
                                if self.tokens[self.index].token_type == scanner.TokenType.BINARY_OPERATOR:
                                    operator.append(self.tokens[self.index].literal)
                                    self.index += 1
                            else:
                                self.output_file.write(" " + operator[-1] + " ")
                        elif self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
                            self.output_file.write(")")
                            num_paren_bin_expr -= 1
                            self.index += 1
                            if num_paren_bin_expr == 0:
                                self.output_file.write("\n")
                                break
                    if bin_op:
                    break
                self.output_file.write(self.tokens[self.index].literal)
                self.output_file.write(self.replace_dash(self.index+1))
                self.output_file.write("(")
                self.num_parentheses += 1
                self.index += 2
            elif self.tokens[self.index].token_type == scanner.TokenType.QUOTE_OPERATOR:
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
            else:
                self.output_file.write(self.replace_dash(self.index))
                self.index += 1
                if self.tokens[self.index].token_type != scanner.TokenType.RIGHT_PAREN:
                    self.output_file.write(", ")

    def translate(self):
        self.index = 0
        self.output_file = open(self.python_file, "w")
        while self.index < len(self.tokens) - 1:
            # LEFT PARENTHESES
            if self.tokens[self.index].token_type == scanner.TokenType.LEFT_PAREN:
                self.left_paren()
                continue
            # RIGHT PARENTHESES
            elif self.tokens[self.index].token_type == scanner.TokenType.RIGHT_PAREN:
                self.right_paren()
                continue
            elif self.tokens[self.index].token_type == scanner.TokenType.DEF_OPERATOR:
                self.def_operator()
            elif self.tokens[self.index].token_type == scanner.TokenType.IMPORT_OPERATOR:
                self.import_operator()
            elif self.tokens[self.index].token_type == scanner.TokenType.BINARY_OPERATOR:
                self.binary_operator()
            elif self.tokens[self.index].token_type == scanner.TokenType.IDENTIFIER:
               self.identifier()

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

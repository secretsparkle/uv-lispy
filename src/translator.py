import scanner

class Translator:
    def __init__(self, python_file, tokens):
        self.parentheses = 0 # measures the indent level
        self.output_file = ""
        self.python_file = python_file # default is a.py
        self.tokens = tokens

    def translate(self):
        index = 0
        self.output_file = open(self.python_file, "w")
        while index < len(self.tokens) - 1:
            # first left parenthesis
            #self.newline_check(index)
            if self.tokens[index].token_type == scanner.TokenType.LEFT_PAREN:
                self.parentheses += 1
                index += 1
                continue
            elif self.tokens[index].token_type == scanner.TokenType.RIGHT_PAREN:
                self.parentheses -= 1
                index += 1
                continue
            elif self.tokens[index].token_type == scanner.TokenType.DEF_OPERATOR:
                self.output_file.write("def ")
                index += 1
                self.output_file.write(self.replace_dash(index))
                self.output_file.write("(")
                index += 2 # skip over left parenthesis
                if self.tokens[index].token_type == scanner.TokenType.RIGHT_PAREN:
                    self.output_file.write("):")
                    self.newline_and_scope_insert()
                elif self.tokens[index + 1].token_type == scanner.TokenType.LEFT_PAREN: # if there are arguments
                    index += 2
                    while True:
                        self.output_file.write(self.tokens[index].literal)
                        index += 1
                        if self.tokens[index].token_type == scanner.TokenType.RIGHT_PAREN:
                            self.parentheses -= 1
                            index += 1
                            break
                        else:
                            self.output_file.write(", ")
                    self.output_file.write("):")
                    self.newline_and_scope_insert()
            elif self.tokens[index].token_type == scanner.TokenType.IDENTIFIER:
                # start of some function
                self.output_file.write(self.replace_dash(index))
                self.output_file.write("(")
                index += 1
                while True:
                    if self.tokens[index].token_type == scanner.TokenType.RIGHT_PAREN:
                        self.parentheses -= 1
                        self.output_file.write(")")
                        index += 1
                        break
                    self.output_file.write(self.replace_dash(index))
                    index += 1
                if self.parentheses == 0:
                    self.output_file.write("\n")

    def replace_dash(self, index):
        return self.tokens[index].literal.replace("-", "_")
    def newline_check(self, index):
        if self.tokens[index].line - self.tokens[index-1].line == 1:
            return True
        else:
            return False

    def newline_and_scope_insert(self):
        self.output_file.write("\n\t")

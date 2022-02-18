import re

class Parser:
    def __init__(self, source, tokens):
        self.current = 0
        self.parentheses_stack = []
        self.source = source
        self.tokens = tokens

    # doesn't catch too few closing parens
    def balanced_parentheses(self) -> bool:
        parentheses = []
        for char in self.source:
            if char == '(':
                parentheses.insert(-1, char)
            elif char == ')' and len(parentheses) > 0:
                parentheses.pop()
            elif char == ')':
                return False
            elif char != '(' and char != ')':
                continue
            elif len(parentheses) > 0:
                return False
        if len(parentheses) > 0:
            return False
        else:
            return True

    def get_next(self):
        self.current += 1

    def no_more_input(self):
        if self.current >= len(self.tokens):
            return True

    def is_valid_lisp_syntax(self):
        if self.no_more_input():
            return False
        if not self.balanced_parentheses():
            return False
        if self.is_list() or self.is_identifier() or self.is_number() or self.is_string():
            return True
        else:
            return False

    def is_list(self):
        if self.no_more_input():
            return False
        if not self.is_open_paren():
            return False
        if not self.is_identifier():
            return False

        while True:
            self.get_next()
            if self.is_list() or self.is_number() or self.is_identifier():
                continue
            else:
                break
        if self.is_closed_paren() and self.no_more_input():
            return True
        elif not self.is_closed_paren():
            return False

    def is_identifier(self):
        if self.no_more_input():
            return False
        if re.findall("^[a-zA-Z]+\-[a-zA-Z]+|^[a-zA-Z]+", self.tokens[self.current]):
            return True
        else:
            return False

    def is_number(self):
        if self.no_more_input():
            return False
        for element in self.tokens[self.current]:
            if not self.is_digit(element):
                return False
        self.get_next()
        return True

    def is_string(self):
        if self.no_more_input():
            return False
        if self.tokens[self.current][0] != "\"":
            return False
        if self.tokens[self.current][-1] != "\"":
            return False
        if re.findall(".*", self.tokens[self.current]):
            return True
        else:
            return False

    def is_character(self, element):
        return element.isprintable()
    def is_letter(self, element):
        return element.isalpha()
    def is_digit(self, element):
        return element.isdigit()
    def is_whitespace(self, element):
        return element.isspace()
    def is_open_paren(self):
        if self.current >= len(self.tokens):
            return True
        if self.tokens[self.current] == '(':
            self.get_next()
            return True
        else:
            return False
    def is_closed_paren(self):
        if self.current >= len(self.tokens):
            return True
        if self.tokens[self.current] == ')':
            self.get_next()
            return True
        else:
            return False

import re
import sys


class Error:
    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description

class Parser:
    def __init__(self, tokens, source):
        self.tokens = tokens
        self.source = source
        self.current = 0

    def get_next(self):
        self.current += 1

    # doesn't catch too few closing parens
    def balanced_parentheses(self, string) -> bool:
        parentheses = []
        for char in string:
            print(char)
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

    def no_more_input(self):
        if self.current >= len(self.tokens):
            return True

    def is_s_expression(self):
        print("s-expression")
        print(self.tokens[self.current:])
        if self.no_more_input():
            return False
        if not self.balanced_parentheses(self.source):
            return False
        if self.is_list() or self.is_identifier() or self.is_number() or self.is_string():
            return True
        else:
            return False

    def is_list(self):
        print("list")
        print(self.tokens[self.current:])
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
        print("identifier")
        print(self.tokens[self.current:])
        if self.no_more_input():
            return False
        if re.findall("[a-zA-Z]\-[a-zA-Z]|^[a-zA-Z]*$", self.tokens[self.current]):
            return True
        else:
            return False

    def is_number(self):
        print("number")
        print(self.tokens[self.current:])
        if self.no_more_input():
            return False
        for element in self.tokens[self.current]:
            if not self.is_digit(element):
                return False
        self.get_next()
        return True

    def is_string(self):
        print("string")
        print(self.tokens[self.current:])
        if self.no_more_input():
            return False
        if self.tokens[self.current][0] != "\"":
            return False
        if self.tokens[self.current][-1] != "\"":
            return False
        for element in self.tokens[self.current][1:-1]:
           if not self.is_character(element):
               return False
        return True

    def is_character(self, element):
        print("character")
        print(self.tokens[self.current:])
        return element.isprintable()
    def is_letter(self, element):
        print("letter")
        print(self.tokens[self.current:])
        return element.isalpha()
    def is_digit(self, element):
        print("digit")
        print(self.tokens[self.current:])
        return element.isdigit()
    def is_whitespace(self, element):
        print("whitespace")
        print(self.tokens[self.current:])
        return element.isspace()
    def is_open_paren(self):
        if self.current >= len(self.tokens):
            return True
        print("open paren")
        print(self.tokens[self.current:])
        if self.tokens[self.current] == '(':
            self.get_next()
            return True
        else:
            return False
    def is_closed_paren(self):
        if self.current >= len(self.tokens):
            return True
        print("closed paren")
        print(self.tokens[self.current:])
        if self.tokens[self.current] == ')':
            self.get_next()
            return True
        else:
            return False

class Scanner:
    def __init__(self, source):
        self.current = -1
        self.source = source
        self.tokens = []

    def split_into_lexemes(self):
        self.tokens = list(filter(None, re.split(r"(\s|[()])", self.source)))
        self.tokens = [x for x in self.tokens if x!='' and x!=' ' and x!='\n']

class Table:
    def __init__(self):
        self.table = {}

    def access(self, key):
        return self.table[key]

    def insert(self, key, value):
        self.table[key] = value

class Token:
    def __init__(self, tokentype, lexeme, literal, line):
       self.tokentype = tokentype
       self.lexeme = lexeme
       self.literal = literal
       self.line = line


source = ""
# open source file if supplied
if len(sys.argv) > 1 and len(sys.argv) < 3:
    f = open(sys.argv[1])
    source = f.read()
    s = Scanner(source)
    s.split_into_lexemes()
    print(s.tokens)
    parser = Parser(s.tokens, source)
    print(parser.is_s_expression())

else:
    while True:
        #symbol_table = Table()
        #symbol_table.insert("test", 2)
        #print(symbol_table.access("test"))

        query = input("> ")
        if balanced_parentheses(query):
            print(query)

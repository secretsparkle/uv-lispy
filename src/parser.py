import re
from scanner import Token
from scanner import TokenType

class Parser:
    def __init__(self, tokens):
        self.current = 0
        self.tokens = tokens

    def is_BODY(self):
        while not is_EOF():
            self.is_S_EXPRESSION()

    def is_EOF(self):
        if self.tokens[self.current].token_type == EOF:
            return True
        else:
            return False

    def is_IDENTIFIER(self):
        if self.tokens[self.current].token_type == IDENTIFIER:
            self.next_token()
            return True
        else:
            return False

    def is_LEFT_PAREN(self):
        if self.tokens[self.current].token_type == LEFT_PAREN:
            self.next_token()
            return True
        else:
            return False

    def is_LIST(self):
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

    def is_NUMBER(self):
        if self.tokens[self.current].token_type == NUMBER:
            self.next_token()
            return True
        else:
            return False

    def is_RIGHT_PAREN(self):
        if self.tokens[self.current].token_type == RIGHT_PAREN:
            self.next_token()
            return True
        else:
            return False

    def is_S_EXPRESSION(self):
        pass

    def is_STRING(self):
        if self.tokens[self.current].token_type == STRING:
            self.next_token()
            return True
        else:
            return False

    def next_token(self):
        self.current += 1

    def is_valid_lisp_syntax(self):
        if self.no_more_input():
            return False
        if not self.balanced_parentheses():
            return False
        if self.is_list() or self.is_identifier() or self.is_number() or self.is_string():
            return True
        else:
            return False

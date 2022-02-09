from scanner import Token
from scanner import TokenType

class Parser:
    def __init__(self, tokens):
        self.current = 0
        self.tokens = tokens

    def is_BODY(self):
        if self.is_S_EXPRESSION() and self.is_EOF():
            return True
        else:
            return False

    def is_EOF(self):
        if self.tokens[self.current].token_type == TokenType.EOF:
            return True
        else:
            return False

    def is_IDENTIFIER(self):
        if self.tokens[self.current].token_type == TokenType.IDENTIFIER:
            self.next_token()
            return True
        else:
            return False

    def is_LEFT_PAREN(self):
        if self.tokens[self.current].token_type == TokenType.LEFT_PAREN:
            self.next_token()
            return True
        else:
            return False

    def is_LIST(self):
        if self.is_LEFT_PAREN() and self.is_IDENTIFIER() and self.is_S_EXPRESSION() and self.is_RIGHT_PAREN():
            return True
        else:
            return False

    def is_NUMBER(self):
        if self.tokens[self.current].token_type == TokenType.NUMBER:
            self.next_token()
            return True
        else:
            return False

    def is_RIGHT_PAREN(self):
        if self.tokens[self.current].token_type == TokenType.RIGHT_PAREN:
            self.next_token()
            return True
        else:
            return False

    def is_S_EXPRESSION(self):
        if self.is_IDENTIFIER() or self.is_LIST() or self.is_NUMBER() or self.is_STRING() or (self.is_S_EXPRESSION() and self.is_S_EXPRESSION()):
            return True
        else:
            return False

    def is_STRING(self):
        if self.tokens[self.current].token_type == TokenType.STRING:
            self.next_token()
            return True
        else:
            return False

    def next_token(self):
        self.current += 1

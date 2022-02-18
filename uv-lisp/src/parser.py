from scanner import Token
from scanner import TokenType

# parser error codes
SUCCESS = 0
ERROR = 1

class Parser:
    def __init__(self, tokens):
        self.current = 0
        self.tokens = tokens

    def is_ATOM(self):
        print("atom")
        if self.is_NUMBER() or self.is_KEYWORD_IDENTIFIER() or self.is_IDENTIFIER() or self.is_STRING():
            return True
        else:
            return False

    def is_BODY(self):
        print("body")
        while True:
            print(self.current)
            result = self.is_S_EXPRESSION()
            if result == True and self.current < len(self.tokens) - 1:
                continue
            elif result == True and self.is_EOF():
                return True
            else:
                return False

    def is_EOF(self):
        print("eof")
        if self.tokens[self.current].token_type == TokenType.EOF:
            return True
        else:
            return False

    def is_IDENTIFIER(self):
        print("identifier")
        if self.tokens[self.current].token_type == TokenType.IDENTIFIER:
            self.next_token()
            return True
        else:
            return False

    def is_KEYWORD_IDENTIFIER(self):
        print("keyword")
        if self.tokens[self.current].token_type == TokenType.KEYWORD_IDENTIFIER:
            self.next_token()
            return True
        else:
            return False

    def is_LEFT_PAREN(self):
        print("left paren")
        if self.tokens[self.current].token_type == TokenType.LEFT_PAREN:
            print("LEFT PAREN TRUE")
            self.next_token()
            return True
        else:
            return False

    def is_LIST(self):
        print("list")
        if not self.is_LEFT_PAREN():
            return False
        if not self.is_ATOM():
            return False
        while True:
            result = self.is_S_EXPRESSION()
            if result == True:
                continue
            elif result == False:
                break
            else:
                return result
        if not self.is_RIGHT_PAREN():
            return False

        return True

    def is_NUMBER(self):
        print("number")
        if self.tokens[self.current].token_type == TokenType.NUMBER:
            print("IN TRUE")
            self.next_token()
            return True
        else:
            return False

    def is_RIGHT_PAREN(self):
        print("right paren")
        if self.tokens[self.current].token_type == TokenType.RIGHT_PAREN:
            self.next_token()
            return True
        else:
            return False

    def is_S_EXPRESSION(self):
        print("s expression")
        if self.is_ATOM() or self.is_LIST():
            return True
        else:
            return ResultHandler(ERROR, self.tokens[self.current])

    def is_STRING(self):
        print("string")
        if self.tokens[self.current].token_type == TokenType.STRING:
            self.next_token()
            return True
        else:
            return False

    def next_token(self):
        self.current += 1

class ResultHandler:
    def __init__(self, error, token):
        self.error = error
        self.token = token

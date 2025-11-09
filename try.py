import re

# 1. Define Token Types (Equivalent to JS TokenType Enum)
class TokenType:
    # Data Types
    NUMERO = "numero"
    LUTANG = "lutang"
    TEKSTO = "teksto"
    OOMALI = "oomali"
    TROPA = "tropa"
    SAKLAW = "saklaw"
    GRUPO = "grupo"
    IMBENTO = "imbento"
    ARAYKO = "arayko"
    # Control Flow
    KUNG = "kung"
    KUNGDIMAN = "kungdiman"
    EDIWOW = "ediwow"
    ETOSAYO = "etosayo"
    LOOPIT = "loopit"
    DO = "do"
    AWAT = "awat"
    OSIGE = "osige"
    MAGBALIK = "magbalik"
    KASO = "kaso"
    PILIIN = "piliin"
    IBA = "iba"
    IN = "in"
    # Boolean Literals/Keywords
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    OONGANI = "oongani" # True
    MALINGANI = "malingani" # False
    ALAWS = "alaws" # Null/None
    # Built-ins
    INPUT = "input"
    PRINT = "print"
    ANOBOI = "anoboi"
    CONS = "cons"
    # Operators
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    POWER = "**"
    DIVIDE = "/"
    FLOOR_DIV = "//"
    MODULO = "%"
    EQUAL = "=="
    NOT_EQUAL = "!="
    GREATER = ">"
    LESS = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    ASSIGN = "="
    PLUS_ASSIGN = "+="
    MINUS_ASSIGN = "-="
    MULTIPLY_ASSIGN = "*="
    DIVIDE_ASSIGN = "/="
    FLOOR_DIV_ASSIGN = "//="
    MODULO_ASSIGN = "%="
    POWER_ASSIGN = "**="
    # Punctuation
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    LBRACE = "{"
    RBRACE = "}"
    DOT = "."
    COMMA = ","
    SEMICOLON = ";"
    COLON = ":"
    # Literals & Others
    NUMERO_LIT = "numero_literal"
    LUTANG_LIT = "lutang_literal"
    TEKSTO_LIT = "teksto_literal"
    OOMALI_LIT = "oomali_literal"
    IDENTIFIER = "identifier"
    SINGLE_COMMENT = "single_comment"
    MULTI_COMMENT = "multi_comment"
    EOF = "eof"
    ERROR = "error"

# 2. Define States (Equivalent to JS State Enum)
class State:
    START = 0
    IN_IDENTIFIER = 1
    IN_NUMBER = 2
    IN_FLOAT = 3
    IN_STRING_DOUBLE = 4
    IN_STRING_SINGLE = 5
    IN_STRING_ESCAPE = 6
    IN_COMMENT_MULTI = 8 # State 7 (IN_COMMENT_SINGLE) is implied in IN_BANG for JS
    IN_LESS = 10
    IN_GREATER = 11
    IN_EQUAL = 12
    IN_BANG = 13
    IN_PLUS = 14
    IN_MINUS = 15
    IN_STAR = 16
    IN_SLASH = 17
    IN_PERCENT = 18
    IN_COMMENT_MULTI_END1 = 19 # Encountered one '<' after '>>>'
    IN_COMMENT_MULTI_END2 = 20 # Encountered two '<<' after '>>>'
    ACCEPT = 99
    ERROR = -1

# 3. Lexical Analyzer Class
class LexicalAnalyzer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # Reserved words mapping
        self.RESERVED_WORDS = {
            "numero": TokenType.NUMERO, "lutang": TokenType.LUTANG,
            "teksto": TokenType.TEKSTO, "oomali": TokenType.OOMALI,
            "tropa": TokenType.TROPA, "saklaw": TokenType.SAKLAW,
            "grupo": TokenType.GRUPO, "imbento": TokenType.IMBENTO,
            "arayko": TokenType.ARAYKO, "kung": TokenType.KUNG,
            "kungdiman": TokenType.KUNGDIMAN, "ediwow": TokenType.EDIWOW,
            "etosayo": TokenType.ETOSAYO, "loopit": TokenType.LOOPIT,
            "do": TokenType.DO, "awat": TokenType.AWAT,
            "osige": TokenType.OSIGE, "magbalik": TokenType.MAGBALIK,
            "AND": TokenType.AND, "OR": TokenType.OR, "NOT": TokenType.NOT,
            "oongani": TokenType.OONGANI, "malingani": TokenType.MALINGANI,
            "alaws": TokenType.ALAWS, "input": TokenType.INPUT,
            "print": TokenType.PRINT, "anoboi": TokenType.ANOBOI,
            "iba": TokenType.IBA, "in": TokenType.IN,
            "kaso": TokenType.KASO, "piliin": TokenType.PILIIN,
            "cons": TokenType.CONS
        }
        
    def _current_char(self):
        """Returns the character at the current position or None (EOF)."""
        return self.source[self.position] if self.position < len(self.source) else None

    def _peek(self, offset=1):
        """Returns the character at an offset relative to the current position."""
        pos = self.position + offset
        return self.source[pos] if pos < len(self.source) else None

    def _advance(self):
        """Moves the position forward and updates line/column."""
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1

    def get_next_token(self):
        """
        Implements the Lexer state machine using a while True loop and state
        variables to simulate the GOTO method.
        """
        state = State.START
        lexeme = ""
        start_line = self.line
        start_col = self.column
        token_type = None
        string_quote = None
        
        # Using a loop to simulate the GOTO flow (state transitions)
        while True:
            char = self._current_char()

            # --- GOTO START ---
            if state == State.START:
                start_line, start_col = self.line, self.column
                lexeme = ""
                
                # Skip whitespace
                if char in (' ', '\t', '\r', '\n'):
                    self._advance()
                    continue
                
                # EOF
                if char is None:
                    return {'type': TokenType.EOF, 'value': '', 'line': self.line, 'column': self.column}

                # Identifiers (a-z, A-Z, _)
                if char is not None and (char.isalpha() or char == '_'):
                    state = State.IN_IDENTIFIER
                    lexeme += char
                    self._advance()
                    continue
                
                # Numbers
                if char is not None and char.isdigit():
                    state = State.IN_NUMBER
                    lexeme += char
                    self._advance()
                    continue

                # Strings
                if char == '"':
                    state = State.IN_STRING_DOUBLE
                    string_quote = '"'
                    self._advance()
                    continue
                if char == "'":
                    state = State.IN_STRING_SINGLE
                    string_quote = "'"
                    self._advance()
                    continue

                # Multi-character/Compound operators
                if char == '!': state = State.IN_BANG
                elif char == '>': state = State.IN_GREATER
                elif char == '<': state = State.IN_LESS
                elif char == '=': state = State.IN_EQUAL
                elif char == '+': state = State.IN_PLUS
                elif char == '-': state = State.IN_MINUS
                elif char == '*': state = State.IN_STAR
                elif char == '/': state = State.IN_SLASH
                elif char == '%': state = State.IN_PERCENT
                
                # Handle single-character tokens (if not a compound op start)
                if state != State.START:
                    lexeme += char
                    self._advance()
                    continue

                single_char_map = {
                    '(': TokenType.LPAREN, ')': TokenType.RPAREN,
                    '[': TokenType.LBRACKET, ']': TokenType.RBRACKET,
                    '{': TokenType.LBRACE, '}': TokenType.RBRACE,
                    '.': TokenType.DOT, ',': TokenType.COMMA,
                    ';': TokenType.SEMICOLON, ':': TokenType.COLON
                }
                
                if char in single_char_map:
                    token_type = single_char_map[char]
                    lexeme = char
                    self._advance()
                    state = State.ACCEPT
                    continue
                
                # If none matched, it's an error
                state = State.ERROR
                lexeme = char if char is not None else ""
                self._advance()
                continue
            
            # --- GOTO IN_IDENTIFIER ---
            if state == State.IN_IDENTIFIER:
                if char is not None and (char.isalnum() or char == '_') and len(lexeme) < 15:
                    lexeme += char
                    self._advance()
                else:
                    token_type = self.RESERVED_WORDS.get(lexeme, TokenType.IDENTIFIER)
                    
                    # Handle boolean literals that look like reserved words
                    if lexeme in ["oongani", "malingani"]:
                         token_type = TokenType.OOMALI_LIT
                         
                    state = State.ACCEPT
                continue
            
            # --- GOTO IN_NUMBER ---
            if state == State.IN_NUMBER:
                if char is not None and char.isdigit():
                    lexeme += char
                    self._advance()
                elif char == '.' and self._peek() is not None and self._peek().isdigit():
                    state = State.IN_FLOAT
                    lexeme += char
                    self._advance()
                else:
                    token_type = TokenType.NUMERO_LIT
                    state = State.ACCEPT
                continue
            
            # --- GOTO IN_FLOAT ---
            if state == State.IN_FLOAT:
                if char is not None and char.isdigit():
                    lexeme += char
                    self._advance()
                else:
                    token_type = TokenType.LUTANG_LIT
                    state = State.ACCEPT
                continue
                
            # --- GOTO IN_STRING_DOUBLE / IN_STRING_SINGLE ---
            if state in (State.IN_STRING_DOUBLE, State.IN_STRING_SINGLE):
                end_quote = '"' if state == State.IN_STRING_DOUBLE else "'"
                
                if char is None:
                    token_type = TokenType.ERROR # Unclosed string
                    state = State.ACCEPT
                elif char == '\\':
                    state = State.IN_STRING_ESCAPE
                    self._advance()
                elif char == end_quote:
                    token_type = TokenType.TEKSTO_LIT
                    self._advance()
                    state = State.ACCEPT
                else:
                    lexeme += char
                    self._advance()
                continue

            # --- GOTO IN_STRING_ESCAPE ---
            if state == State.IN_STRING_ESCAPE:
                if char in ('n', 't', '\\', '{', '}', '"', "'"):
                    # Only append the escaped character to the lexeme
                    # The JS code appends '\\' + char, which is unusual for a lexer
                    # I'll stick to typical lexer behavior: unescape and append the result
                    # For a literal copy of the JS (which includes the backslash in the token value):
                    lexeme += '\\' + (char or '')
                else:
                    # Invalid escape sequence, just include the backslash and the char
                    lexeme += '\\' + (char or '')
                    
                if char is not None:
                    self._advance()
                    
                state = State.IN_STRING_DOUBLE if string_quote == '"' else State.IN_STRING_SINGLE
                continue
            
            # --- GOTO IN_BANG ('!') ---
            if state == State.IN_BANG:
                if char == '=': # !=
                    lexeme += char
                    token_type = TokenType.NOT_EQUAL
                    self._advance()
                    state = State.ACCEPT
                elif char == '>' and self._peek() == '>': # !>> (Single comment)
                    self._advance() # Consume '>'
                    self._advance() # Consume second '>'
                    lexeme = "" # Reset lexeme for comment content
                    
                    # Capture comment text until newline or EOF
                    while self._current_char() is not None and self._current_char() != '\n':
                        lexeme += self._current_char()
                        self._advance()
                        
                    token_type = TokenType.SINGLE_COMMENT
                    state = State.ACCEPT
                else:
                    token_type = TokenType.ERROR # Unexpected '!'
                    state = State.ACCEPT
                continue

            # --- GOTO IN_GREATER ('>') ---
            if state == State.IN_GREATER:
                if char == '=': # >=
                    lexeme += char
                    token_type = TokenType.GREATER_EQUAL
                    self._advance()
                    state = State.ACCEPT
                elif char == '>' and self._peek() == '>': # >>> (Multi-comment start)
                    self._advance() # Consume first '>'
                    self._advance() # Consume second '>'
                    lexeme = "" # Start collecting comment body
                    state = State.IN_COMMENT_MULTI
                else:
                    token_type = TokenType.GREATER
                    state = State.ACCEPT
                continue
            
            # --- GOTO IN_COMMENT_MULTI ---
            if state == State.IN_COMMENT_MULTI:
                if char is None:
                    token_type = TokenType.ERROR # Unclosed multi-comment is an error in some lexers, but here it accepts what it has.
                    state = State.ACCEPT
                elif char == '<':
                    state = State.IN_COMMENT_MULTI_END1
                    self._advance()
                else:
                    lexeme += char
                    self._advance()
                continue
            
            # --- GOTO IN_COMMENT_MULTI_END1 ('<') ---
            if state == State.IN_COMMENT_MULTI_END1:
                if char == '<':
                    state = State.IN_COMMENT_MULTI_END2
                    self._advance()
                else:
                    # Not '<<', so the previous '<' was part of the comment body
                    lexeme += '<' + (char if char is not None else '')
                    if char is not None:
                        self._advance()
                    state = State.IN_COMMENT_MULTI
                continue

            # --- GOTO IN_COMMENT_MULTI_END2 ('<<') ---
            if state == State.IN_COMMENT_MULTI_END2:
                if char == '<': # <<< (Multi-comment end)
                    self._advance()
                    token_type = TokenType.MULTI_COMMENT
                    state = State.ACCEPT
                else:
                    # Not '<<<', so '<<' is part of the comment body
                    lexeme += '<<' + (char if char is not None else '')
                    if char is not None:
                        self._advance()
                    state = State.IN_COMMENT_MULTI
                continue

            # --- GOTO IN_LESS ('<') ---
            if state == State.IN_LESS:
                if char == '=': # <=
                    lexeme += char
                    token_type = TokenType.LESS_EQUAL
                    self._advance()
                    state = State.ACCEPT
                else:
                    token_type = TokenType.LESS
                    state = State.ACCEPT
                continue
            
            # --- GOTO IN_EQUAL ('=') ---
            if state == State.IN_EQUAL:
                if char == '=': # ==
                    lexeme += char
                    token_type = TokenType.EQUAL
                    self._advance()
                    state = State.ACCEPT
                else:
                    token_type = TokenType.ASSIGN
                    state = State.ACCEPT
                continue
            
            # --- GOTO IN_PLUS ('+') ---
            if state == State.IN_PLUS:
                if char == '=': # +=
                    lexeme += char
                    token_type = TokenType.PLUS_ASSIGN
                    self._advance()
                    state = State.ACCEPT
                else:
                    token_type = TokenType.PLUS
                    state = State.ACCEPT
                continue
            
            # --- GOTO IN_MINUS ('-') ---
            if state == State.IN_MINUS:
                if char == '=': # -=
                    lexeme += char
                    token_type = TokenType.MINUS_ASSIGN
                    self._advance()
                    state = State.ACCEPT
                elif char is not None and char.isdigit(): # Start of negative number
                    lexeme += char
                    self._advance()
                    state = State.IN_NUMBER
                else:
                    token_type = TokenType.MINUS
                    state = State.ACCEPT
                continue
            
            # --- GOTO IN_STAR ('*') ---
            if state == State.IN_STAR:
                if char == '*':
                    lexeme += char
                    self._advance()
                    if self._current_char() == '=': # **=
                        lexeme += '='
                        token_type = TokenType.POWER_ASSIGN
                        self._advance()
                    else: # **
                        token_type = TokenType.POWER
                    state = State.ACCEPT
                elif char == '=': # *=
                    lexeme += char
                    token_type = TokenType.MULTIPLY_ASSIGN
                    self._advance()
                    state = State.ACCEPT
                else:
                    token_type = TokenType.MULTIPLY
                    state = State.ACCEPT
                continue

            # --- GOTO IN_SLASH ('/') ---
            if state == State.IN_SLASH:
                if char == '/':
                    lexeme += char
                    self._advance()
                    if self._current_char() == '=': # //=
                        lexeme += '='
                        token_type = TokenType.FLOOR_DIV_ASSIGN
                        self._advance()
                    else: # //
                        token_type = TokenType.FLOOR_DIV
                    state = State.ACCEPT
                elif char == '=': # /=
                    lexeme += char
                    token_type = TokenType.DIVIDE_ASSIGN
                    self._advance()
                    state = State.ACCEPT
                else:
                    token_type = TokenType.DIVIDE
                    state = State.ACCEPT
                continue
            
            # --- GOTO IN_PERCENT ('%') ---
            if state == State.IN_PERCENT:
                if char == '=': # %=
                    lexeme += char
                    token_type = TokenType.MODULO_ASSIGN
                    self._advance()
                    state = State.ACCEPT
                else:
                    token_type = TokenType.MODULO
                    state = State.ACCEPT
                continue

            # --- GOTO ACCEPT ---
            if state == State.ACCEPT:
                # Trimming comment content only, not literals
                value = lexeme
                if token_type in (TokenType.SINGLE_COMMENT, TokenType.MULTI_COMMENT):
                     value = lexeme.strip()

                return {
                    'type': token_type,
                    'value': value,
                    'line': start_line,
                    'column': start_col
                }
            
            # --- GOTO ERROR ---
            if state == State.ERROR:
                return {
                    'type': TokenType.ERROR,
                    'value': lexeme,
                    'line': start_line,
                    'column': start_col
                }

    def tokenize(self):
        """Tokenizes the entire source string."""
        self.tokens = []
        while True:
            token = self.get_next_token()
            self.tokens.append(token)
            if token['type'] == TokenType.EOF:
                break
        return self.tokens

# Example Usage:
if __name__ == '__main__':
    source_code = """
    numero a = 123;
    lutang b = -4.5;
    teksto message = "Hello, world!";
    oomali truth = oongani;
    
    kung a >= 10:
        a += 1;
        !>> This is a single line comment
    kungdiman:
        loopit i in tropa:
            print("Looping...");
    
    grupo myFunc(numero x):
        magbalik x ** 2;

    >>>
    This is a multi-line comment
    It can contain anything, like special characters < or >>
    It should end with <<<
    <<<
    
    y //= 2;
    z != 5;
    """
    
    lexer = LexicalAnalyzer(source_code)
    tokens = lexer.tokenize()

    print(f"{'TYPE':<25} | {'VALUE':<20} | LINE:COL")
    print("-" * 50)
    for token in tokens:
        print(f"{token['type']:<25} | {token['value']:<20} | {token['line']}:{token['column']}")
    
    # Test error condition (Unrecognized character)
    source_code_error = "a = 10 $ b = 20"
    lexer_error = LexicalAnalyzer(source_code_error)
    tokens_error = lexer_error.tokenize()
    
    print("\n" + "="*50)
    print("Test Case: Unrecognized Character Error")
    print("="*50)
    for token in tokens_error:
        print(f"{token['type']:<25} | {token['value']:<20} | {token['line']}:{token['column']}")
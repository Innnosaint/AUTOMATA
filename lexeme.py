class TokenType:
    """Token types for MaluPython"""
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
    KUNGZ = "kungz"
    KUNGDIMAN = "kungdiman"
    EDIWOW = "ediwow"
    ETOSAYO = "etosayo"
    LOOPIT = "loopit"
    DO = "do"
    AWAT = "awat"
    OSIGE = "osige"
    MAGBALIK = "magbalik"
    
    # Boolean & Logical
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    OONGANI = "oongani"
    MALINGANI = "malingani"
    ALAWS = "alaws"
    
    # I/O
    INPUT = "input"
    PRINT = "print"
    
    # Others
    ANOBOI = "anoboi"
    IBA = "iba"
    KASO = "kaso"
    PILIIN = "piliin"
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
    
    # Symbols (Delimiters)
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
    
    # Literals
    NUMERO_LIT = "numero_literal"
    LUTANG_LIT = "lutang_literal"
    TEKSTO_LIT = "teksto_literal"
    OOMALI_LIT = "oomali_literal"
    
    # Others
    IDENTIFIER = "identifier"
    SINGLE_COMMENT = "single_comment"
    MULTI_COMMENT = "multi_comment"
    EOF = "eof"
    ERROR = "error"


class State:
    """States for the finite automaton"""
    START = 0
    IN_IDENTIFIER = 1
    IN_NUMBER = 2
    IN_FLOAT = 3
    IN_STRING_DOUBLE = 4
    IN_STRING_SINGLE = 5
    IN_STRING_ESCAPE = 6
    IN_COMMENT_SINGLE = 7
    IN_COMMENT_MULTI = 8
    IN_OPERATOR = 9
    IN_LESS = 10
    IN_GREATER = 11
    IN_EQUAL = 12
    IN_BANG = 13
    IN_PLUS = 14
    IN_MINUS = 15
    IN_STAR = 16
    IN_SLASH = 17
    IN_PERCENT = 18
    IN_COMMENT_MULTI_END1 = 19
    IN_COMMENT_MULTI_END2 = 20
    ACCEPT = 99
    ERROR = -1


class LexicalAnalyzer:
    """MaluPython Lexical Analyzer using GOTO method"""
    
    RESERVED_WORDS = {
        "numero": TokenType.NUMERO,
        "lutang": TokenType.LUTANG,
        "teksto": TokenType.TEKSTO,
        "oomali": TokenType.OOMALI,
        "tropa": TokenType.TROPA,
        "saklaw": TokenType.SAKLAW,
        "grupo": TokenType.GRUPO,
        "imbento": TokenType.IMBENTO,
        "arayko": TokenType.ARAYKO,
        "kungz": TokenType.KUNGZ,
        "kungdiman": TokenType.KUNGDIMAN,
        "ediwow": TokenType.EDIWOW,
        "etosayo": TokenType.ETOSAYO,
        "loopit": TokenType.LOOPIT,
        "do": TokenType.DO,
        "awat": TokenType.AWAT,
        "osige": TokenType.OSIGE,
        "magbalik": TokenType.MAGBALIK,
        "AND": TokenType.AND,
        "OR": TokenType.OR,
        "NOT": TokenType.NOT,
        "oongani": TokenType.OONGANI,
        "malingani": TokenType.MALINGANI,
        "alaws": TokenType.ALAWS,
        "input": TokenType.INPUT,
        "print": TokenType.PRINT,
        "anoboi": TokenType.ANOBOI,
        "iba": TokenType.IBA,
        "kaso": TokenType.KASO,
        "piliin": TokenType.PILIIN,
        "cons": TokenType.CONS
    }
    
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def current_char(self):
        """Get current character"""
        return self.source[self.position] if self.position < len(self.source) else None
    
    def peek(self, offset=1):
        """Look ahead at character"""
        pos = self.position + offset
        return self.source[pos] if pos < len(self.source) else None
    
    def advance(self):
        """Move to next character"""
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def get_next_token(self):
        """Get next token using GOTO method (finite automaton)"""
        state = State.START
        lexeme = ""
        start_line = self.line
        start_col = self.column
        token_type = None
        string_quote = None
        
        # State machine loop
        while True:
            char = self.current_char()
            
            # START STATE
            if state == State.START:
                # End of file
                if char is None:
                    return {
                        'type': TokenType.EOF,
                        'value': '',
                        'line': self.line,
                        'column': self.column
                    }

                # Skip whitespace
                if char in ' \t\r':
                    self.advance()
                    start_col = self.column
                    continue

                # Skip newline
                if char == '\n':
                    self.advance()
                    start_line = self.line
                    start_col = self.column
                    continue
                
                # Identifier or keyword
                if char.isalpha() or char == '_':
                    state = State.IN_IDENTIFIER
                    lexeme += char
                    self.advance()
                    continue
                
                # Number
                if char.isdigit():
                    state = State.IN_NUMBER
                    lexeme += char
                    self.advance()
                    continue
                
                # String (double quote)
                if char == '"':
                    state = State.IN_STRING_DOUBLE
                    string_quote = '"'
                    self.advance()
                    continue
                
                # String (single quote)
                if char == "'":
                    state = State.IN_STRING_SINGLE
                    string_quote = "'"
                    self.advance()
                    continue
                
                # Comment or operators starting with !
                if char == '!':
                    state = State.IN_BANG
                    lexeme += char
                    self.advance()
                    continue
                
                # Operators starting with >
                if char == '>':
                    state = State.IN_GREATER
                    lexeme += char
                    self.advance()
                    continue
                
                # Operators starting with <
                if char == '<':
                    state = State.IN_LESS
                    lexeme += char
                    self.advance()
                    continue
                
                # Operators starting with =
                if char == '=':
                    state = State.IN_EQUAL
                    lexeme += char
                    self.advance()
                    continue
                
                # Operators starting with +
                if char == '+':
                    state = State.IN_PLUS
                    lexeme += char
                    self.advance()
                    continue
                
                # Operators starting with - (or negative number)
                if char == '-':
                    state = State.IN_MINUS
                    lexeme += char
                    self.advance()
                    continue
                
                # Operators starting with *
                if char == '*':
                    state = State.IN_STAR
                    lexeme += char
                    self.advance()
                    continue
                
                # Operators starting with /
                if char == '/':
                    state = State.IN_SLASH
                    lexeme += char
                    self.advance()
                    continue
                
                # Operators starting with %
                if char == '%':
                    state = State.IN_PERCENT
                    lexeme += char
                    self.advance()
                    continue
                
                # Single character tokens
                single_char = {
                    '(': TokenType.LPAREN,
                    ')': TokenType.RPAREN,
                    '[': TokenType.LBRACKET,
                    ']': TokenType.RBRACKET,
                    '{': TokenType.LBRACE,
                    '}': TokenType.RBRACE,
                    '.': TokenType.DOT,
                    ',': TokenType.COMMA,
                    ';': TokenType.SEMICOLON,
                    ':': TokenType.COLON
                }
                
                if char in single_char:
                    token_type = single_char[char]
                    lexeme = char
                    self.advance()
                    state = State.ACCEPT
                    continue
                
                # Unknown character
                state = State.ERROR
                lexeme = char
                self.advance()
                continue
            
            # IN_IDENTIFIER STATE
            elif state == State.IN_IDENTIFIER:
                if char and (char.isalnum() or char == '_'):
                    lexeme += char
                    self.advance()
                else:
                    # Check identifier rules: must start with capital letter
                    if lexeme[0].isupper():
                        token_type = TokenType.IDENTIFIER
                    elif lexeme in self.RESERVED_WORDS:
                        token_type = self.RESERVED_WORDS[lexeme]
                        # Boolean literals
                        if lexeme in ("oongani", "malingani"):
                            token_type = TokenType.OOMALI_LIT
                    else:
                        token_type = TokenType.ERROR
                    state = State.ACCEPT
                continue
            
            # IN_NUMBER STATE
            elif state == State.IN_NUMBER:
                if char and char.isdigit():
                    lexeme += char
                    self.advance()
                elif char == '.' and self.peek() and self.peek().isdigit():
                    state = State.IN_FLOAT
                    lexeme += char
                    self.advance()
                else:
                    token_type = TokenType.NUMERO_LIT
                    state = State.ACCEPT
                continue
            
            # IN_FLOAT STATE
            elif state == State.IN_FLOAT:
                if char and char.isdigit():
                    lexeme += char
                    self.advance()
                else:
                    token_type = TokenType.LUTANG_LIT
                    state = State.ACCEPT
                continue
            
            # IN_STRING_DOUBLE STATE
            elif state == State.IN_STRING_DOUBLE:
                if char is None:
                    token_type = TokenType.ERROR
                    state = State.ACCEPT
                elif char == '\\':
                    state = State.IN_STRING_ESCAPE
                    self.advance()
                elif char == '"':
                    token_type = TokenType.TEKSTO_LIT
                    self.advance()
                    state = State.ACCEPT
                else:
                    lexeme += char
                    self.advance()
                continue
            
            # IN_STRING_SINGLE STATE
            elif state == State.IN_STRING_SINGLE:
                if char is None:
                    token_type = TokenType.ERROR
                    state = State.ACCEPT
                elif char == '\\':
                    state = State.IN_STRING_ESCAPE
                    self.advance()
                elif char == "'":
                    token_type = TokenType.TEKSTO_LIT
                    self.advance()
                    state = State.ACCEPT
                else:
                    lexeme += char
                    self.advance()
                continue
            
            # IN_STRING_ESCAPE STATE
            elif state == State.IN_STRING_ESCAPE:
                if char in 'nt\\{}"\'':
                    lexeme += '\\' + char
                else:
                    lexeme += '\\'
                self.advance()
                # Return to appropriate string state
                state = State.IN_STRING_DOUBLE if string_quote == '"' else State.IN_STRING_SINGLE
                continue
            
            # IN_BANG STATE (! or != or !>>)
            elif state == State.IN_BANG:
                if char == '=':
                    lexeme += char
                    token_type = TokenType.NOT_EQUAL
                    self.advance()
                    state = State.ACCEPT
                elif char == '>' and self.peek() == '>':
                    # Single line comment !>>
                    self.advance()  # skip >
                    self.advance()  # skip >
                    lexeme = ""
                    while self.current_char() and self.current_char() != '\n':
                        lexeme += self.current_char()
                        self.advance()
                    token_type = TokenType.SINGLE_COMMENT
                    state = State.ACCEPT
                else:
                    token_type = TokenType.ERROR
                    state = State.ACCEPT
                continue
            
            # IN_GREATER STATE (> or >= or >> or >>>)
            elif state == State.IN_GREATER:
                if char == '=':
                    lexeme += char
                    token_type = TokenType.GREATER_EQUAL
                    self.advance()
                    state = State.ACCEPT
                elif char == '>' and self.peek() == '>':
                    # Multi-line comment >>>
                    self.advance()  # skip >
                    self.advance()  # skip >
                    lexeme = ""
                    state = State.IN_COMMENT_MULTI
                else:
                    token_type = TokenType.GREATER
                    state = State.ACCEPT
                continue
            
            # IN_COMMENT_MULTI STATE
            elif state == State.IN_COMMENT_MULTI:
                if char is None:
                    token_type = TokenType.MULTI_COMMENT
                    state = State.ACCEPT
                elif char == '<':
                    state = State.IN_COMMENT_MULTI_END1
                    self.advance()
                else:
                    lexeme += char
                    self.advance()
                continue
            
            # IN_COMMENT_MULTI_END1 STATE
            elif state == State.IN_COMMENT_MULTI_END1:
                if char == '<':
                    state = State.IN_COMMENT_MULTI_END2
                    self.advance()
                else:
                    lexeme += '<' + (char if char else '')
                    if char:
                        self.advance()
                    state = State.IN_COMMENT_MULTI
                continue
            
            # IN_COMMENT_MULTI_END2 STATE
            elif state == State.IN_COMMENT_MULTI_END2:
                if char == '<':
                    # Found <<<
                    self.advance()
                    token_type = TokenType.MULTI_COMMENT
                    state = State.ACCEPT
                else:
                    lexeme += '<<' + (char if char else '')
                    if char:
                        self.advance()
                    state = State.IN_COMMENT_MULTI
                continue
            
            # IN_LESS STATE (< or <=)
            elif state == State.IN_LESS:
                if char == '=':
                    lexeme += char
                    token_type = TokenType.LESS_EQUAL
                    self.advance()
                    state = State.ACCEPT
                else:
                    token_type = TokenType.LESS
                    state = State.ACCEPT
                continue
            
            # IN_EQUAL STATE (= or ==)
            elif state == State.IN_EQUAL:
                if char == '=':
                    lexeme += char
                    token_type = TokenType.EQUAL
                    self.advance()
                    state = State.ACCEPT
                else:
                    token_type = TokenType.ASSIGN
                    state = State.ACCEPT
                continue
            
            # IN_PLUS STATE (+ or +=)
            elif state == State.IN_PLUS:
                if char == '=':
                    lexeme += char
                    token_type = TokenType.PLUS_ASSIGN
                    self.advance()
                    state = State.ACCEPT
                else:
                    token_type = TokenType.PLUS
                    state = State.ACCEPT
                continue
            
            # IN_MINUS STATE (- or -= or negative number)
            elif state == State.IN_MINUS:
                if char == '=':
                    lexeme += char
                    token_type = TokenType.MINUS_ASSIGN
                    self.advance()
                    state = State.ACCEPT
                elif char and char.isdigit():
                    # Negative number
                    lexeme += char
                    self.advance()
                    state = State.IN_NUMBER
                else:
                    token_type = TokenType.MINUS
                    state = State.ACCEPT
                continue
            
            # IN_STAR STATE (* or ** or *= or **=)
            elif state == State.IN_STAR:
                if char == '*':
                    lexeme += char
                    self.advance()
                    if self.current_char() == '=':
                        lexeme += '='
                        token_type = TokenType.POWER_ASSIGN
                        self.advance()
                    else:
                        token_type = TokenType.POWER
                    state = State.ACCEPT
                elif char == '=':
                    lexeme += char
                    token_type = TokenType.MULTIPLY_ASSIGN
                    self.advance()
                    state = State.ACCEPT
                else:
                    token_type = TokenType.MULTIPLY
                    state = State.ACCEPT
                continue
            
            # IN_SLASH STATE (/ or // or /= or //=)
            elif state == State.IN_SLASH:
                if char == '/':
                    lexeme += char
                    self.advance()
                    if self.current_char() == '=':
                        lexeme += '='
                        token_type = TokenType.FLOOR_DIV_ASSIGN
                        self.advance()
                    else:
                        token_type = TokenType.FLOOR_DIV
                    state = State.ACCEPT
                elif char == '=':
                    lexeme += char
                    token_type = TokenType.DIVIDE_ASSIGN
                    self.advance()
                    state = State.ACCEPT
                else:
                    token_type = TokenType.DIVIDE
                    state = State.ACCEPT
                continue
            
            # IN_PERCENT STATE (% or %=)
            elif state == State.IN_PERCENT:
                if char == '=':
                    lexeme += char
                    token_type = TokenType.MODULO_ASSIGN
                    self.advance()
                    state = State.ACCEPT
                else:
                    token_type = TokenType.MODULO
                    state = State.ACCEPT
                continue
            
            # ACCEPT STATE
            elif state == State.ACCEPT:
                return {
                    'type': token_type,
                    'value': lexeme.strip() if token_type in (TokenType.SINGLE_COMMENT, TokenType.MULTI_COMMENT) else lexeme,
                    'line': start_line,
                    'column': start_col
                }
            
            # ERROR STATE
            elif state == State.ERROR:
                return {
                    'type': TokenType.ERROR,
                    'value': lexeme,
                    'line': start_line,
                    'column': start_col
                }
    
    def tokenize(self):
        """Tokenize entire source code"""
        self.tokens = []
        while True:
            token = self.get_next_token()
            self.tokens.append(token)
            if token['type'] == TokenType.EOF:
                break
        return self.tokens


# Example usage
if __name__ == "__main__":
    source_code = '''anoboi() {
    numero X = 10;
    lutang Pi = 3.14;
    teksto Name = "Juan";
    oomali Flag = oongani;
    numero _var = 5;

    kungz (X > 5) {
        print("x is greater");
    } ediwow {
        print("x is smaller");
    }

    magbalik X;
};'''
    
    lexer = LexicalAnalyzer(source_code)
    tokens = lexer.tokenize()
    
    print("=" * 70)
    print("MALUPYTHON LEXICAL ANALYZER - GOTO METHOD (Finite Automaton)")
    print("=" * 70)
    
    for token in tokens:
        if token['type'] != TokenType.EOF:
            print(f"{token['type']:20} | {token['value']:20} | [{token['line']}:{token['column']}]")
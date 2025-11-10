import string
import tkinter as tk
from tkinter import scrolledtext, messagebox

########## DEFINITIONS ##########
DIGITS = '0123456789'
ALPHABET = string.ascii_letters
ALPHADIG = DIGITS + ALPHABET
WHITESPACE = '\n\t '

########## DELIMITERS ##########
SPACE_DLM = {' ', '\t', '\n'}
ARITH_OPER = {'+', '-', '*', '/', '%'}
RELAT_OPER = {'>', '<', '=', '!'}
ASSIGN_OPER = {'='}

# Delimiter sets for each token type
COMMA_DLM = set(ALPHADIG) | SPACE_DLM | {'_', '.', '[', '"', '-', '('}
PERIOD_DLM = set(ALPHADIG) | {'_'}
LPAREN_DLM = set(ALPHADIG) | {'_'} | SPACE_DLM | {'(', ')', '"', '-', }
RPAREN_DLM = SPACE_DLM | ARITH_OPER | RELAT_OPER | {'{', '}', ')', ']', ',', '.', ';', ':'}
LBRACKET_DLM = set(ALPHADIG) | {'_'} | SPACE_DLM | {'.', ']', '-', '(', '"'}
RBRACKET_DLM = SPACE_DLM | {'[', '=', ';', ':'}
LCURLY_DLM = SPACE_DLM | set(ALPHADIG) | {'_', '{', '(', '"'}
RCURLY_DLM = SPACE_DLM | {'}', ';', ':'}
SEMICOLON_DLM = SPACE_DLM | set(ALPHADIG)
QUOTE_DLM = SPACE_DLM | set(ALPHADIG) | {'_', ',', '\\', ':', '[', ']', '(', ')', '}', ';', ':'}
ARITH_DLM = SPACE_DLM | {'(', '-'} | set(DIGITS)
RELAT_DLM = SPACE_DLM | set(ALPHADIG) | {'(', '"'}
ASSIGN_DLM = SPACE_DLM | {'(', '-', '"'}
LOGIC_DLM = SPACE_DLM | {'('}
IO_DLM = SPACE_DLM | {'(', '"'}
BLOCK_DLM = SPACE_DLM | {'{'}
DEC_DLM = SPACE_DLM
CONDI_DLM = SPACE_DLM | {'(', '{', ';'}
SELECT_DLM = SPACE_DLM | {'(', ':'}
CTRL_DLM = SPACE_DLM | {'(', ';'}
NUM_DLM = SPACE_DLM | ARITH_OPER | RELAT_OPER | {',', ')', '{', '}', ':', ']', ';'}
ID_DLM = SPACE_DLM | {'_'} | ARITH_OPER | RELAT_OPER | {'(', ')', '[', ']', '{', '}', ':', '.', ';', "'", '"', '\\', '!', '>'}

########## TOKENS ##########
# KEYWORDS - Data types
TKN_NUMERO = 'numero'
TKN_LUTANG = 'lutang'
TKN_TEKSTO = 'teksto'
TKN_OOMALI = 'oomali'
TKN_TROPA = 'tropa'
TKN_SAKLAW = 'saklaw'
TKN_GRUPO = 'grupo'
TKN_IMBENTO = 'imbento'
TKN_ARAYKO = 'arayko'

# Control Flow
TKN_KUNG = 'kung'
TKN_KUNGDIMAN = 'kungdiman'
TKN_EDIWOW = 'ediwow'
TKN_ETOSAYO = 'etosayo'
TKN_LOOPIT = 'loopit'
TKN_DO = 'do'
TKN_AWAT = 'awat'
TKN_OSIGE = 'osige'
TKN_MAGBALIK = 'magbalik'
TKN_KASO = 'kaso'
TKN_PILIIN = 'piliin'
TKN_IBA = 'iba'
TKN_IN = 'in'

# Logical operators
TKN_AND = 'AND'
TKN_OR = 'OR'
TKN_NOT = 'NOT'

# Boolean literals
TKN_OONGANI = 'oongani'
TKN_MALINGANI = 'malingani'
TKN_ALAWS = 'alaws'

# Input/Output
TKN_INPUT = 'input'
TKN_PRINT = 'print'

# Others
TKN_ANOBOI = 'anoboi'
TKN_CONS = 'cons'

# RESERVED SYMBOLS
# Arithmetic operators
TKN_PLUS = '+'
TKN_MINUS = '-'
TKN_MULTIPLY = '*'
TKN_POWER = '**'
TKN_DIVIDE = '/'
TKN_FLOOR_DIV = '//'
TKN_MODULO = '%'

# Assignment operators
TKN_ASSIGN = '='
TKN_PLUS_ASSIGN = '+='
TKN_MINUS_ASSIGN = '-='
TKN_MULTIPLY_ASSIGN = '*='
TKN_DIVIDE_ASSIGN = '/='
TKN_FLOOR_DIV_ASSIGN = '//='
TKN_MODULO_ASSIGN = '%='
TKN_POWER_ASSIGN = '**='

# Relational operators
TKN_EQUAL = '=='
TKN_NOT_EQUAL = '!='
TKN_GREATER = '>'
TKN_LESS = '<'
TKN_GREATER_EQUAL = '>='
TKN_LESS_EQUAL = '<='

# Other symbols
TKN_LPAREN = '('
TKN_RPAREN = ')'
TKN_LBRACKET = '['
TKN_RBRACKET = ']'
TKN_LBRACE = '{'
TKN_RBRACE = '}'
TKN_SEMICOLON = ';'
TKN_COLON = ':'
TKN_COMMA = ','
TKN_DOT = '.'

# Comments
TKN_SINGLE_COMMENT = 'single comment'
TKN_MULTI_COMMENT = 'multi comment'

# LITERALS
TKN_NUMERO_LIT = 'numero literal'
TKN_LUTANG_LIT = 'lutang literal'
TKN_TEKSTO_LIT = 'teksto literal'
TKN_OOMALI_LIT = 'oomali literal'

# IDENTIFIER
TKN_IDENTIFIER = 'id'

# SPECIAL
TKN_SPACE = 'space'
TKN_TAB = '\\t'
TKN_NEWLINE = '\\n'
TKN_EOF = 'EOF'

########## POSITION CLASS ##########
class Position:
    def __init__(self, idx, ln, col, fullText):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fullText = fullText
    
    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fullText)

########## ERROR CLASS ##########
class Error:
    def __init__(self, pos_start, pos_end, error_name, info):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.info = info

    def __repr__(self):
        result = f'{self.error_name}: {self.info} \n'
        result += f'Line {self.pos_start.ln + 1}, Column {self.pos_start.col + 1}\n'
        return result

class LexicalError(Error):
    def __init__(self, pos_start, pos_end, info):
        super().__init__(pos_start, pos_end, 'Lexical Error', info)

########## TOKEN CLASS ##########
class Token:
    def __init__(self, type, value=None, pos_start=None, pos_end=None):
        self.type = type
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        
        if pos_end:
            self.pos_end = pos_end
    
    def __repr__(self):
        if self.value:
            return f'{self.value}: {self.type}'
        return f'{self.type}'

########## MAIN LEXER CLASS ##########
class Lexer:
    # Main States
    STATE_START = 0
    STATE_NUMBER = 1
    STATE_DECIMAL = 2
    STATE_STRING_DOUBLE = 3
    STATE_STRING_SINGLE = 4
    STATE_OPERATOR = 5
    STATE_SINGLE_COMMENT = 6
    STATE_MULTI_COMMENT = 7
    STATE_MULTI_COMMENT_END1 = 8
    
    # Keyword/Identifier States
    STATE_IDENTIFIER_CONTINUE = 300
    
    # Letter-specific starting states
    STATE_A = 101
    STATE_C = 120
    STATE_D = 124
    STATE_E = 126
    STATE_G = 138
    STATE_I = 143
    STATE_K = 156
    STATE_L = 168
    STATE_M = 179
    STATE_N = 194
    STATE_O = 202
    STATE_P = 218
    STATE_S = 228
    STATE_T = 234
    
    # Define all keyword states (shortened for brevity - full implementation below)
    # 'a' branch
    STATE_AN, STATE_AND, STATE_ANO, STATE_ANOB, STATE_ANOBO, STATE_ANOBOI = 102, 103, 104, 105, 106, 107
    STATE_AL, STATE_ALA, STATE_ALAW, STATE_ALAWS = 108, 109, 110, 111
    STATE_AR, STATE_ARA, STATE_ARAY, STATE_ARAYK, STATE_ARAYKO = 112, 113, 114, 115, 116
    STATE_AW, STATE_AWA, STATE_AWAT = 117, 118, 119
    
    # 'c' branch
    STATE_CO, STATE_CON, STATE_CONS = 121, 122, 123
    
    # 'd' branch
    STATE_DO = 125
    
    # 'e' branch
    STATE_ED, STATE_EDI, STATE_EDIW, STATE_EDIWO, STATE_EDIWOW = 127, 128, 129, 130, 131
    STATE_ET, STATE_ETO, STATE_ETOS, STATE_ETOSA, STATE_ETOSAY, STATE_ETOSAYO = 132, 133, 134, 135, 136, 137
    
    # 'g' branch
    STATE_GR, STATE_GRU, STATE_GRUP, STATE_GRUPO = 139, 140, 141, 142
    
    # 'i' branch
    STATE_IM, STATE_IMB, STATE_IMBE, STATE_IMBEN, STATE_IMBENT, STATE_IMBENTO = 144, 145, 146, 147, 148, 149
    STATE_IN, STATE_INP, STATE_INPU, STATE_INPUT = 150, 151, 152, 153
    STATE_IB, STATE_IBA = 154, 155
    
    # 'k' branch
    STATE_KU, STATE_KUN, STATE_KUNG = 157, 158, 159
    STATE_KUNGD, STATE_KUNGDI, STATE_KUNGDIM, STATE_KUNGDIMA, STATE_KUNGDIMAN = 160, 161, 162, 163, 164
    STATE_KA, STATE_KAS, STATE_KASO = 165, 166, 167
    
    # 'l' branch
    STATE_LU, STATE_LUT, STATE_LUTA, STATE_LUTAN, STATE_LUTANG = 169, 170, 171, 172, 173
    STATE_LO, STATE_LOO, STATE_LOOP, STATE_LOOPI, STATE_LOOPIT = 174, 175, 176, 177, 178
    
    # 'm' branch
    STATE_MA = 180
    STATE_MAG, STATE_MAGB, STATE_MAGBA, STATE_MAGBAL, STATE_MAGBALI, STATE_MAGBALIK = 181, 182, 183, 184, 185, 186
    STATE_MAL, STATE_MALI, STATE_MALIN, STATE_MALING, STATE_MALINGA, STATE_MALINGAN, STATE_MALINGANI = 187, 188, 189, 190, 191, 192, 193
    
    # 'n' branch
    STATE_NU, STATE_NUM, STATE_NUME, STATE_NUMER, STATE_NUMERO = 195, 196, 197, 198, 199
    STATE_NO, STATE_NOT = 200, 201
    
    # 'o' branch
    STATE_OO = 203
    STATE_OON, STATE_OONG, STATE_OONGA, STATE_OONGAN, STATE_OONGANI = 204, 205, 206, 207, 208
    STATE_OOM, STATE_OOMA, STATE_OOMAL, STATE_OOMALI = 209, 210, 211, 212
    STATE_OR = 213
    STATE_OS, STATE_OSI, STATE_OSIG, STATE_OSIGE = 214, 215, 216, 217
    
    # 'p' branch
    STATE_PR, STATE_PRI, STATE_PRIN, STATE_PRINT = 219, 220, 221, 222
    STATE_PI, STATE_PIL, STATE_PILI, STATE_PILII, STATE_PILIIN = 223, 224, 225, 226, 227
    
    # 's' branch
    STATE_SA, STATE_SAK, STATE_SAKL, STATE_SAKLA, STATE_SAKLAW = 229, 230, 231, 232, 233
    
    # 't' branch
    STATE_TE, STATE_TEK, STATE_TEKS, STATE_TEKST, STATE_TEKSTO = 235, 236, 237, 238, 239
    STATE_TR, STATE_TRO, STATE_TROP, STATE_TROPA = 240, 241, 242, 243
    
    def __init__(self, source):
        self.source = source
        self.pos = Position(0, 0, 0, source)
        
        if len(source) > 0:
            self.current_char = self.source[0]
        else:
            self.current_char = None

    def advance(self):
        self.pos.advance(self.current_char)
        
        if self.pos.idx < len(self.source):
            self.current_char = self.source[self.pos.idx]
        else:
            self.current_char = None

    def check_delimiter(self, delimiter_set, token_name, pos_start, pos_end):
        """Check if current character is a valid delimiter"""
        if self.current_char is None:
            return True
        if self.current_char in delimiter_set:
            return True
        return False

    def is_identifier_char(self, char):
        """Check if character can be part of an identifier"""
        return char is not None and (char in ALPHADIG or char == '_')

    def tokenize(self):
        tokens = []
        errors = []
        
        state = self.STATE_START
        buffer = ''
        pos_start = None
        int_dig_count = 0
        dec_dig_count = 0
        
        while True:
            char = self.current_char
            
            # STATE_START
            if state == self.STATE_START:
                if char is None:
                    tokens.append(Token(TKN_EOF, '', self.pos.copy(), self.pos.copy()))
                    break
                
                elif char == '\n':
                    pos_start = self.pos.copy()
                    tokens.append(Token(TKN_NEWLINE, '\\n', pos_start, self.pos.copy()))
                    self.advance()
                    
                elif char == ' ':
                    pos_start = self.pos.copy()
                    tokens.append(Token(TKN_SPACE, 'space', pos_start, self.pos.copy()))
                    self.advance()
                    
                elif char == '\t':
                    pos_start = self.pos.copy()
                    tokens.append(Token(TKN_TAB, '\\t', pos_start, self.pos.copy()))
                    self.advance()
                
                elif char in ALPHABET or char == '_':
                    buffer = char
                    pos_start = self.pos.copy()
                    self.advance()
                    
                    if char == 'a':
                        state = self.STATE_A
                    elif char == 'c':
                        state = self.STATE_C
                    elif char == 'd':
                        state = self.STATE_D
                    elif char == 'e':
                        state = self.STATE_E
                    elif char == 'g':
                        state = self.STATE_G
                    elif char == 'i':
                        state = self.STATE_I
                    elif char == 'k':
                        state = self.STATE_K
                    elif char == 'l':
                        state = self.STATE_L
                    elif char == 'm':
                        state = self.STATE_M
                    elif char == 'n':
                        state = self.STATE_N
                    elif char == 'o':
                        state = self.STATE_O
                    elif char == 'p':
                        state = self.STATE_P
                    elif char == 's':
                        state = self.STATE_S
                    elif char == 't':
                        state = self.STATE_T
                    else:
                        state = self.STATE_IDENTIFIER_CONTINUE
                
                elif char in DIGITS:
                    buffer = ''
                    int_dig_count = 0
                    dec_dig_count = 0
                    pos_start = self.pos.copy()
                    state = self.STATE_NUMBER
                
                elif char == '"':
                    buffer = ''
                    pos_start = self.pos.copy()
                    self.advance()
                    state = self.STATE_STRING_DOUBLE
                    
                elif char == "'":
                    buffer = ''
                    pos_start = self.pos.copy()
                    self.advance()
                    state = self.STATE_STRING_SINGLE
                
                elif char in '+-*/%=!><':
                    buffer = ''
                    pos_start = self.pos.copy()
                    state = self.STATE_OPERATOR
                
                elif char == '(':
                    pos_start = self.pos.copy()
                    self.advance()
                    if self.check_delimiter(LPAREN_DLM, '(', pos_start, self.pos.copy()):
                        tokens.append(Token(TKN_LPAREN, '(', pos_start, self.pos.copy()))
                    else:
                        errors.append(LexicalError(pos_start, self.pos.copy(),
                            info=f'Invalid delimiter after "("'))
                    
                elif char == ')':
                    pos_start = self.pos.copy()
                    self.advance()
                    if self.check_delimiter(RPAREN_DLM, ')', pos_start, self.pos.copy()):
                        tokens.append(Token(TKN_RPAREN, ')', pos_start, self.pos.copy()))
                    else:
                        errors.append(LexicalError(pos_start, self.pos.copy(),
                            info=f'Invalid delimiter after ")"'))
                    
                elif char == '[':
                    pos_start = self.pos.copy()
                    self.advance()
                    if self.check_delimiter(LBRACKET_DLM, '[', pos_start, self.pos.copy()):
                        tokens.append(Token(TKN_LBRACKET, '[', pos_start, self.pos.copy()))
                    else:
                        errors.append(LexicalError(pos_start, self.pos.copy(),
                            info=f'Invalid delimiter after "["'))
                    
                elif char == ']':
                    pos_start = self.pos.copy()
                    self.advance()
                    if self.check_delimiter(RBRACKET_DLM, ']', pos_start, self.pos.copy()):
                        tokens.append(Token(TKN_RBRACKET, ']', pos_start, self.pos.copy()))
                    else:
                        errors.append(LexicalError(pos_start, self.pos.copy(),
                            info=f'Invalid delimiter after "]"'))
                    
                elif char == '{':
                    pos_start = self.pos.copy()
                    self.advance()
                    if self.check_delimiter(LCURLY_DLM, '{', pos_start, self.pos.copy()):
                        tokens.append(Token(TKN_LBRACE, '{', pos_start, self.pos.copy()))
                    else:
                        errors.append(LexicalError(pos_start, self.pos.copy(),
                            info=f'Invalid delimiter after "{{"'))
                    
                elif char == '}':
                    pos_start = self.pos.copy()
                    self.advance()
                    if self.check_delimiter(RCURLY_DLM, '}', pos_start, self.pos.copy()):
                        tokens.append(Token(TKN_RBRACE, '}', pos_start, self.pos.copy()))
                    else:
                        errors.append(LexicalError(pos_start, self.pos.copy(),
                            info=f'Invalid delimiter after "}}"'))
                    
                elif char == ';':
                    pos_start = self.pos.copy()
                    self.advance()
                    if self.check_delimiter(SEMICOLON_DLM, ';', pos_start, self.pos.copy()):
                        tokens.append(Token(TKN_SEMICOLON, ';', pos_start, self.pos.copy()))
                    else:
                        errors.append(LexicalError(pos_start, self.pos.copy(),
                            info=f'Invalid delimiter after ";"'))
                    
                elif char == ':':
                    pos_start = self.pos.copy()
                    self.advance()
                    tokens.append(Token(TKN_COLON, ':', pos_start, self.pos.copy()))
                    
                elif char == ',':
                    pos_start = self.pos.copy()
                    self.advance()
                    if self.check_delimiter(COMMA_DLM, ',', pos_start, self.pos.copy()):
                        tokens.append(Token(TKN_COMMA, ',', pos_start, self.pos.copy()))
                    else:
                        errors.append(LexicalError(pos_start, self.pos.copy(),
                            info=f'Invalid delimiter after ","'))
                    
                elif char == '.':
                    pos_start = self.pos.copy()
                    self.advance()
                    if self.check_delimiter(PERIOD_DLM, '.', pos_start, self.pos.copy()):
                        tokens.append(Token(TKN_DOT, '.', pos_start, self.pos.copy()))
                    else:
                        errors.append(LexicalError(pos_start, self.pos.copy(),
                            info=f'Invalid delimiter after "."'))
                
                else:
                    pos_start = self.pos.copy()
                    invalid_char = char
                    self.advance()
                    errors.append(LexicalError(pos_start, self.pos.copy(), 
                                              info=f'Invalid character "{invalid_char}"'))
            
            # NUMBER STATE
            elif state == self.STATE_NUMBER:
                if char in DIGITS:
                    buffer += char
                    int_dig_count += 1
                    self.advance()
                elif char == '.':
                    buffer += char
                    self.advance()
                    state = self.STATE_DECIMAL
                else:
                    pos_end = self.pos.copy()
                    if not self.check_delimiter(NUM_DLM, buffer, pos_start, pos_end):
                        errors.append(LexicalError(pos_start, pos_end,
                            info=f'Invalid delimiter after number "{buffer}"'))
                    else:
                        tokens.append(Token(TKN_NUMERO_LIT, buffer, pos_start, pos_end))
                    buffer = ''
                    int_dig_count = 0
                    state = self.STATE_START

            # DECIMAL STATE
            elif state == self.STATE_DECIMAL:
                if char in DIGITS:
                    buffer += char
                    dec_dig_count += 1
                    self.advance()
                else:
                    pos_end = self.pos.copy()
                    if dec_dig_count == 0:
                        errors.append(LexicalError(pos_start, pos_end,
                            info=f'Invalid number format: no digits after decimal point'))
                    elif not self.check_delimiter(NUM_DLM, buffer, pos_start, pos_end):
                        errors.append(LexicalError(pos_start, pos_end,
                            info=f'Invalid delimiter after number "{buffer}"'))
                    else:
                        tokens.append(Token(TKN_LUTANG_LIT, buffer, pos_start, pos_end))
                    buffer = ''
                    int_dig_count = 0
                    dec_dig_count = 0
                    state = self.STATE_START

            # STRING STATES
            elif state == self.STATE_STRING_DOUBLE:
                if char is None:
                    pos_end = self.pos.copy()
                    errors.append(LexicalError(pos_start, pos_end,
                        info='Unterminated string literal'))
                    buffer = ''
                    state = self.STATE_START
                elif char == '"':
                    pos_end = self.pos.copy()
                    self.advance()
                    if self.check_delimiter(QUOTE_DLM, buffer, pos_start, self.pos.copy()):
                        tokens.append(Token(TKN_TEKSTO_LIT, buffer, pos_start, self.pos.copy()))
                    else:
                        errors.append(LexicalError(pos_start, self.pos.copy(),
                            info=f'Invalid delimiter after string'))
                    buffer = ''
                    state = self.STATE_START
                elif char == '\\':
                    buffer += char
                    self.advance()
                    if self.current_char is not None:
                        buffer += self.current_char
                        self.advance()
                else:
                    buffer += char
                    self.advance()

            elif state == self.STATE_STRING_SINGLE:
                if char is None:
                    pos_end = self.pos.copy()
                    errors.append(LexicalError(pos_start, pos_end,
                        info='Unterminated string literal'))
                    buffer = ''
                    state = self.STATE_START
                elif char == "'":
                    pos_end = self.pos.copy()
                    self.advance()
                    if self.check_delimiter(QUOTE_DLM, buffer, pos_start, self.pos.copy()):
                        tokens.append(Token(TKN_TEKSTO_LIT, buffer, pos_start, self.pos.copy()))
                    else:
                        errors.append(LexicalError(pos_start, self.pos.copy(),
                            info=f'Invalid delimiter after string'))
                    buffer = ''
                    state = self.STATE_START
                elif char == '\\':
                    buffer += char
                    self.advance()
                    if self.current_char is not None:
                        buffer += self.current_char
                        self.advance()
                else:
                    buffer += char
                    self.advance()

            # OPERATOR STATE  
            elif state == self.STATE_OPERATOR:
                if char == '+':
                    buffer += char
                    self.advance()
                    if self.current_char == '=':
                        buffer += self.current_char
                        self.advance()
                        pos_end = self.pos.copy()
                        tokens.append(Token(TKN_PLUS_ASSIGN, buffer, pos_start, pos_end))
                        buffer = ''
                        state = self.STATE_START
                    else:
                        pos_end = self.pos.copy()
                        if self.check_delimiter(ARITH_DLM, buffer, pos_start, pos_end):
                            tokens.append(Token(TKN_PLUS, buffer, pos_start, pos_end))
                        else:
                            errors.append(LexicalError(pos_start, pos_end,
                                info=f'Invalid delimiter after operator "{buffer}"'))
                        buffer = ''
                        state = self.STATE_START
                
                elif char == '-':
                    buffer += char
                    self.advance()
                    if self.current_char == '=':
                        buffer += self.current_char
                        self.advance()
                        pos_end = self.pos.copy()
                        tokens.append(Token(TKN_MINUS_ASSIGN, buffer, pos_start, pos_end))
                        buffer = ''
                        state = self.STATE_START
                    else:
                        pos_end = self.pos.copy()
                        if self.check_delimiter(ARITH_DLM, buffer, pos_start, pos_end):
                            tokens.append(Token(TKN_MINUS, buffer, pos_start, pos_end))
                        else:
                            errors.append(LexicalError(pos_start, pos_end,
                                info=f'Invalid delimiter after operator "{buffer}"'))
                        buffer = ''
                        state = self.STATE_START
                
                elif char == '*':
                    buffer += char
                    self.advance()
                    if self.current_char == '*':
                        buffer += self.current_char
                        self.advance()
                        if self.current_char == '=':
                            buffer += self.current_char
                            self.advance()
                            pos_end = self.pos.copy()
                            tokens.append(Token(TKN_POWER_ASSIGN, buffer, pos_start, pos_end))
                            buffer = ''
                            state = self.STATE_START
                        else:
                            pos_end = self.pos.copy()
                            if self.check_delimiter(ARITH_DLM, buffer, pos_start, pos_end):
                                tokens.append(Token(TKN_POWER, buffer, pos_start, pos_end))
                            else:
                                errors.append(LexicalError(pos_start, pos_end,
                                    info=f'Invalid delimiter after operator "{buffer}"'))
                            buffer = ''
                            state = self.STATE_START
                    elif self.current_char == '=':
                        buffer += self.current_char
                        self.advance()
                        pos_end = self.pos.copy()
                        tokens.append(Token(TKN_MULTIPLY_ASSIGN, buffer, pos_start, pos_end))
                        buffer = ''
                        state = self.STATE_START
                    elif self.current_char == '/':
                        buffer = ''
                        self.advance()
                        state = self.STATE_MULTI_COMMENT
                    else:
                        pos_end = self.pos.copy()
                        if self.check_delimiter(ARITH_DLM, buffer, pos_start, pos_end):
                            tokens.append(Token(TKN_MULTIPLY, buffer, pos_start, pos_end))
                        else:
                            errors.append(LexicalError(pos_start, pos_end,
                                info=f'Invalid delimiter after operator "{buffer}"'))
                        buffer = ''
                        state = self.STATE_START
                
                elif char == '/':
                    buffer += char
                    self.advance()
                    if self.current_char == '/':
                        buffer += self.current_char
                        self.advance()
                        if self.current_char == '=':
                            buffer += self.current_char
                            self.advance()
                            pos_end = self.pos.copy()
                            tokens.append(Token(TKN_FLOOR_DIV_ASSIGN, buffer, pos_start, pos_end))
                            buffer = ''
                            state = self.STATE_START
                        else:
                            pos_end = self.pos.copy()
                            if self.check_delimiter(ARITH_DLM, buffer, pos_start, pos_end):
                                tokens.append(Token(TKN_FLOOR_DIV, buffer, pos_start, pos_end))
                            else:
                                errors.append(LexicalError(pos_start, pos_end,
                                    info=f'Invalid delimiter after operator "{buffer}"'))
                            buffer = ''
                            state = self.STATE_START
                    elif self.current_char == '=':
                        buffer += self.current_char
                        self.advance()
                        pos_end = self.pos.copy()
                        tokens.append(Token(TKN_DIVIDE_ASSIGN, buffer, pos_start, pos_end))
                        buffer = ''
                        state = self.STATE_START
                    elif self.current_char == '*':
                        buffer = ''
                        self.advance()
                        state = self.STATE_SINGLE_COMMENT
                    else:
                        pos_end = self.pos.copy()
                        if self.check_delimiter(ARITH_DLM, buffer, pos_start, pos_end):
                            tokens.append(Token(TKN_DIVIDE, buffer, pos_start, pos_end))
                        else:
                            errors.append(LexicalError(pos_start, pos_end,
                                info=f'Invalid delimiter after operator "{buffer}"'))
                        buffer = ''
                        state = self.STATE_START
                
                elif char == '%':
                    buffer += char
                    self.advance()
                    if self.current_char == '=':
                        buffer += self.current_char
                        self.advance()
                        pos_end = self.pos.copy()
                        tokens.append(Token(TKN_MODULO_ASSIGN, buffer, pos_start, pos_end))
                        buffer = ''
                        state = self.STATE_START
                    else:
                        pos_end = self.pos.copy()
                        if self.check_delimiter(ARITH_DLM, buffer, pos_start, pos_end):
                            tokens.append(Token(TKN_MODULO, buffer, pos_start, pos_end))
                        else:
                            errors.append(LexicalError(pos_start, pos_end,
                                info=f'Invalid delimiter after operator "{buffer}"'))
                        buffer = ''
                        state = self.STATE_START
                
                elif char == '=':
                    buffer += char
                    self.advance()
                    if self.current_char == '=':
                        buffer += self.current_char
                        self.advance()
                        pos_end = self.pos.copy()
                        if self.check_delimiter(RELAT_DLM, buffer, pos_start, pos_end):
                            tokens.append(Token(TKN_EQUAL, buffer, pos_start, pos_end))
                        else:
                            errors.append(LexicalError(pos_start, pos_end,
                                info=f'Invalid delimiter after operator "{buffer}"'))
                        buffer = ''
                        state = self.STATE_START
                    else:
                        pos_end = self.pos.copy()
                        if self.check_delimiter(ASSIGN_DLM, buffer, pos_start, pos_end):
                            tokens.append(Token(TKN_ASSIGN, buffer, pos_start, pos_end))
                        else:
                            errors.append(LexicalError(pos_start, pos_end,
                                info=f'Invalid delimiter after operator "{buffer}"'))
                        buffer = ''
                        state = self.STATE_START
                
                elif char == '!':
                    buffer += char
                    self.advance()
                    if self.current_char == '=':
                        buffer += self.current_char
                        self.advance()
                        pos_end = self.pos.copy()
                        if self.check_delimiter(RELAT_DLM, buffer, pos_start, pos_end):
                            tokens.append(Token(TKN_NOT_EQUAL, buffer, pos_start, pos_end))
                        else:
                            errors.append(LexicalError(pos_start, pos_end,
                                info=f'Invalid delimiter after operator "{buffer}"'))
                        buffer = ''
                        state = self.STATE_START
                    else:
                        pos_end = self.pos.copy()
                        errors.append(LexicalError(pos_start, pos_end,
                            info=f'Invalid operator "!"'))
                        buffer = ''
                        state = self.STATE_START
                
                elif char == '>':
                    buffer += char
                    self.advance()
                    if self.current_char == '=':
                        buffer += self.current_char
                        self.advance()
                        pos_end = self.pos.copy()
                        if self.check_delimiter(RELAT_DLM, buffer, pos_start, pos_end):
                            tokens.append(Token(TKN_GREATER_EQUAL, buffer, pos_start, pos_end))
                        else:
                            errors.append(LexicalError(pos_start, pos_end,
                                info=f'Invalid delimiter after operator "{buffer}"'))
                        buffer = ''
                        state = self.STATE_START
                    else:
                        pos_end = self.pos.copy()
                        if self.check_delimiter(RELAT_DLM, buffer, pos_start, pos_end):
                            tokens.append(Token(TKN_GREATER, buffer, pos_start, pos_end))
                        else:
                            errors.append(LexicalError(pos_start, pos_end,
                                info=f'Invalid delimiter after operator "{buffer}"'))
                        buffer = ''
                        state = self.STATE_START
                
                elif char == '<':
                    buffer += char
                    self.advance()
                    if self.current_char == '=':
                        buffer += self.current_char
                        self.advance()
                        pos_end = self.pos.copy()
                        if self.check_delimiter(RELAT_DLM, buffer, pos_start, pos_end):
                            tokens.append(Token(TKN_LESS_EQUAL, buffer, pos_start, pos_end))
                        else:
                            errors.append(LexicalError(pos_start, pos_end,
                                info=f'Invalid delimiter after operator "{buffer}"'))
                        buffer = ''
                        state = self.STATE_START
                    else:
                        pos_end = self.pos.copy()
                        if self.check_delimiter(RELAT_DLM, buffer, pos_start, pos_end):
                            tokens.append(Token(TKN_LESS, buffer, pos_start, pos_end))
                        else:
                            errors.append(LexicalError(pos_start, pos_end,
                                info=f'Invalid delimiter after operator "{buffer}"'))
                        buffer = ''
                        state = self.STATE_START

            # COMMENT STATES
            elif state == self.STATE_SINGLE_COMMENT:
                if char == '\n' or char is None:
                    tokens.append(Token(TKN_SINGLE_COMMENT, buffer, pos_start, self.pos.copy()))
                    buffer = ''
                    state = self.STATE_START
                else:
                    buffer += char
                    self.advance()

            elif state == self.STATE_MULTI_COMMENT:
                if char is None:
                    pos_end = self.pos.copy()
                    errors.append(LexicalError(pos_start, pos_end,
                        info='Unterminated multi-line comment'))
                    buffer = ''
                    state = self.STATE_START
                elif char == '*':
                    buffer += char
                    self.advance()
                    state = self.STATE_MULTI_COMMENT_END1
                else:
                    buffer += char
                    self.advance()

            elif state == self.STATE_MULTI_COMMENT_END1:
                if char is None:
                    pos_end = self.pos.copy()
                    errors.append(LexicalError(pos_start, pos_end,
                        info='Unterminated multi-line comment'))
                    buffer = ''
                    state = self.STATE_START
                elif char == '/':
                    buffer += char
                    self.advance()
                    tokens.append(Token(TKN_MULTI_COMMENT, buffer, pos_start, self.pos.copy()))
                    buffer = ''
                    state = self.STATE_START
                elif char == '*':
                    buffer += char
                    self.advance()
                else:
                    buffer += char
                    self.advance()
                    state = self.STATE_MULTI_COMMENT

            # IDENTIFIER CONTINUATION STATE
            elif state == self.STATE_IDENTIFIER_CONTINUE:
                if self.is_identifier_char(char):
                    buffer += char
                    self.advance()
                else:
                    pos_end = self.pos.copy()
                    if len(buffer) > 15:
                        errors.append(LexicalError(pos_start, pos_end, 
                            info=f'Identifier "{buffer}" is too long (max 15 characters)'))
                    elif not buffer[0].isupper():
                        errors.append(LexicalError(pos_start, pos_end, 
                            info=f'Identifier "{buffer}" must start with a capital letter'))
                    elif not self.check_delimiter(ID_DLM, buffer, pos_start, pos_end):
                        errors.append(LexicalError(pos_start, pos_end,
                            info=f'Invalid delimiter after identifier "{buffer}"'))
                    else:
                        tokens.append(Token(TKN_IDENTIFIER, buffer, pos_start, pos_end))
                    buffer = ''
                    state = self.STATE_START
            
            # KEYWORD STATES - Helper method to handle keywords
            else:
                # Use helper method for keyword states
                result = self._handle_keyword_state(state, char, buffer, pos_start, tokens, errors)
                if result:
                    state, buffer = result
                else:
                    # Unknown state
                    pos_end = self.pos.copy()
                    errors.append(LexicalError(pos_start, pos_end,
                        info=f'Unexpected state: {state}'))
                    buffer = ''
                    state = self.STATE_START
        
        return tokens, errors
    
    def _handle_keyword_state(self, state, char, buffer, pos_start, tokens, errors):
        """Handle all keyword states with character-by-character transitions"""
        
        # Helper function for common identifier fallback
        def handle_identifier_or_continue(next_char, expected_char, next_state):
            if next_char == expected_char:
                buffer_new = buffer + next_char
                self.advance()
                return (next_state, buffer_new)
            elif self.is_identifier_char(next_char):
                buffer_new = buffer + next_char
                self.advance()
                return (self.STATE_IDENTIFIER_CONTINUE, buffer_new)
            else:
                # End identifier
                pos_end = self.pos.copy()
                if not buffer[0].isupper():
                    errors.append(LexicalError(pos_start, pos_end, 
                        info=f'Identifier "{buffer}" must start with a capital letter'))
                elif not self.check_delimiter(ID_DLM, buffer, pos_start, pos_end):
                    errors.append(LexicalError(pos_start, pos_end,
                        info=f'Invalid delimiter after identifier "{buffer}"'))
                else:
                    tokens.append(Token(TKN_IDENTIFIER, buffer, pos_start, pos_end))
                return (self.STATE_START, '')
        
        def finalize_keyword(token_type, delimiter_set):
            if self.is_identifier_char(char):
                buffer_new = buffer + char
                self.advance()
                return (self.STATE_IDENTIFIER_CONTINUE, buffer_new)
            else:
                pos_end = self.pos.copy()
                if self.check_delimiter(delimiter_set, buffer, pos_start, pos_end):
                    tokens.append(Token(token_type, buffer, pos_start, pos_end))
                else:
                    errors.append(LexicalError(pos_start, pos_end,
                        info=f'Invalid delimiter after keyword "{buffer}"'))
                return (self.STATE_START, '')
        
        # 'a' branch
        if state == self.STATE_A:
            if char == 'n': return (self.STATE_AN, buffer + char) if (self.advance() or True) else None
            elif char == 'l': return (self.STATE_AL, buffer + char) if (self.advance() or True) else None
            elif char == 'r': return (self.STATE_AR, buffer + char) if (self.advance() or True) else None
            elif char == 'w': return (self.STATE_AW, buffer + char) if (self.advance() or True) else None
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_AN:
            if char == 'd': 
                self.advance()
                return (self.STATE_AND, buffer + char)
            elif char == 'o':
                self.advance()
                return (self.STATE_ANO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_AND:
            return finalize_keyword(TKN_AND, LOGIC_DLM)
        
        elif state == self.STATE_ANO:
            if char == 'b':
                self.advance()
                return (self.STATE_ANOB, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ANOB:
            if char == 'o':
                self.advance()
                return (self.STATE_ANOBO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ANOBO:
            if char == 'i':
                self.advance()
                return (self.STATE_ANOBOI, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ANOBOI:
            return finalize_keyword(TKN_ANOBOI, DEC_DLM)
        
        elif state == self.STATE_AL:
            if char == 'a':
                self.advance()
                return (self.STATE_ALA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ALA:
            if char == 'w':
                self.advance()
                return (self.STATE_ALAW, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ALAW:
            if char == 's':
                self.advance()
                return (self.STATE_ALAWS, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ALAWS:
            return finalize_keyword(TKN_ALAWS, CONDI_DLM)
        
        elif state == self.STATE_AR:
            if char == 'a':
                self.advance()
                return (self.STATE_ARA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ARA:
            if char == 'y':
                self.advance()
                return (self.STATE_ARAY, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ARAY:
            if char == 'k':
                self.advance()
                return (self.STATE_ARAYK, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ARAYK:
            if char == 'o':
                self.advance()
                return (self.STATE_ARAYKO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ARAYKO:
            return finalize_keyword(TKN_ARAYKO, DEC_DLM)
        
        elif state == self.STATE_AW:
            if char == 'a':
                self.advance()
                return (self.STATE_AWA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_AWA:
            if char == 't':
                self.advance()
                return (self.STATE_AWAT, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_AWAT:
            return finalize_keyword(TKN_AWAT, CTRL_DLM)
        
        # 'c' branch
        elif state == self.STATE_C:
            if char == 'o':
                self.advance()
                return (self.STATE_CO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_CO:
            if char == 'n':
                self.advance()
                return (self.STATE_CON, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_CON:
            if char == 's':
                self.advance()
                return (self.STATE_CONS, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_CONS:
            return finalize_keyword(TKN_CONS, DEC_DLM)
        
        # 'd' branch
        elif state == self.STATE_D:
            if char == 'o':
                self.advance()
                return (self.STATE_DO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_DO:
            return finalize_keyword(TKN_DO, BLOCK_DLM)
        
        # 'e' branch
        elif state == self.STATE_E:
            if char == 'd':
                self.advance()
                return (self.STATE_ED, buffer + char)
            elif char == 't':
                self.advance()
                return (self.STATE_ET, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ED:
            if char == 'i':
                self.advance()
                return (self.STATE_EDI, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_EDI:
            if char == 'w':
                self.advance()
                return (self.STATE_EDIW, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_EDIW:
            if char == 'o':
                self.advance()
                return (self.STATE_EDIWO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_EDIWO:
            if char == 'w':
                self.advance()
                return (self.STATE_EDIWOW, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_EDIWOW:
            return finalize_keyword(TKN_EDIWOW, BLOCK_DLM)
        
        elif state == self.STATE_ET:
            if char == 'o':
                self.advance()
                return (self.STATE_ETO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ETO:
            if char == 's':
                self.advance()
                return (self.STATE_ETOS, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ETOS:
            if char == 'a':
                self.advance()
                return (self.STATE_ETOSA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ETOSA:
            if char == 'y':
                self.advance()
                return (self.STATE_ETOSAY, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ETOSAY:
            if char == 'o':
                self.advance()
                return (self.STATE_ETOSAYO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_ETOSAYO:
            return finalize_keyword(TKN_ETOSAYO, BLOCK_DLM)
        
        # 'g' branch
        elif state == self.STATE_G:
            if char == 'r':
                self.advance()
                return (self.STATE_GR, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_GR:
            if char == 'u':
                self.advance()
                return (self.STATE_GRU, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_GRU:
            if char == 'p':
                self.advance()
                return (self.STATE_GRUP, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_GRUP:
            if char == 'o':
                self.advance()
                return (self.STATE_GRUPO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_GRUPO:
            return finalize_keyword(TKN_GRUPO, DEC_DLM)
        
        # 'i' branch
        elif state == self.STATE_I:
            if char == 'm':
                self.advance()
                return (self.STATE_IM, buffer + char)
            elif char == 'n':
                self.advance()
                return (self.STATE_IN, buffer + char)
            elif char == 'b':
                self.advance()
                return (self.STATE_IB, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_IM:
            if char == 'b':
                self.advance()
                return (self.STATE_IMB, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_IMB:
            if char == 'e':
                self.advance()
                return (self.STATE_IMBE, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_IMBE:
            if char == 'n':
                self.advance()
                return (self.STATE_IMBEN, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_IMBEN:
            if char == 't':
                self.advance()
                return (self.STATE_IMBENT, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_IMBENT:
            if char == 'o':
                self.advance()
                return (self.STATE_IMBENTO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_IMBENTO:
            return finalize_keyword(TKN_IMBENTO, DEC_DLM)
        
        elif state == self.STATE_IN:
            if char == 'p':
                self.advance()
                return (self.STATE_INP, buffer + char)
            else:
                return finalize_keyword(TKN_IN, CTRL_DLM)
        
        elif state == self.STATE_INP:
            if char == 'u':
                self.advance()
                return (self.STATE_INPU, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_INPU:
            if char == 't':
                self.advance()
                return (self.STATE_INPUT, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_INPUT:
            return finalize_keyword(TKN_INPUT, IO_DLM)
        
        elif state == self.STATE_IB:
            if char == 'a':
                self.advance()
                return (self.STATE_IBA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_IBA:
            return finalize_keyword(TKN_IBA, SELECT_DLM)
        
        # 'k' branch
        elif state == self.STATE_K:
            if char == 'u':
                self.advance()
                return (self.STATE_KU, buffer + char)
            elif char == 'a':
                self.advance()
                return (self.STATE_KA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_KU:
            if char == 'n':
                self.advance()
                return (self.STATE_KUN, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_KUN:
            if char == 'g':
                self.advance()
                return (self.STATE_KUNG, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_KUNG:
            if char == 'd':
                self.advance()
                return (self.STATE_KUNGD, buffer + char)
            else:
                return finalize_keyword(TKN_KUNG, CONDI_DLM)
        
        elif state == self.STATE_KUNGD:
            if char == 'i':
                self.advance()
                return (self.STATE_KUNGDI, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_KUNGDI:
            if char == 'm':
                self.advance()
                return (self.STATE_KUNGDIM, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_KUNGDIM:
            if char == 'a':
                self.advance()
                return (self.STATE_KUNGDIMA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_KUNGDIMA:
            if char == 'n':
                self.advance()
                return (self.STATE_KUNGDIMAN, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_KUNGDIMAN:
            return finalize_keyword(TKN_KUNGDIMAN, CONDI_DLM)
        
        elif state == self.STATE_KA:
            if char == 's':
                self.advance()
                return (self.STATE_KAS, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_KAS:
            if char == 'o':
                self.advance()
                return (self.STATE_KASO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_KASO:
            return finalize_keyword(TKN_KASO, SELECT_DLM)
        
        # 'l' branch
        elif state == self.STATE_L:
            if char == 'u':
                self.advance()
                return (self.STATE_LU, buffer + char)
            elif char == 'o':
                self.advance()
                return (self.STATE_LO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_LU:
            if char == 't':
                self.advance()
                return (self.STATE_LUT, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_LUT:
            if char == 'a':
                self.advance()
                return (self.STATE_LUTA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_LUTA:
            if char == 'n':
                self.advance()
                return (self.STATE_LUTAN, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_LUTAN:
            if char == 'g':
                self.advance()
                return (self.STATE_LUTANG, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_LUTANG:
            return finalize_keyword(TKN_LUTANG, DEC_DLM)
        
        elif state == self.STATE_LO:
            if char == 'o':
                self.advance()
                return (self.STATE_LOO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_LOO:
            if char == 'p':
                self.advance()
                return (self.STATE_LOOP, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_LOOP:
            if char == 'i':
                self.advance()
                return (self.STATE_LOOPI, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_LOOPI:
            if char == 't':
                self.advance()
                return (self.STATE_LOOPIT, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_LOOPIT:
            return finalize_keyword(TKN_LOOPIT, CONDI_DLM)
        
        # 'm' branch
        elif state == self.STATE_M:
            if char == 'a':
                self.advance()
                return (self.STATE_MA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_MA:
            if char == 'g':
                self.advance()
                return (self.STATE_MAG, buffer + char)
            elif char == 'l':
                self.advance()
                return (self.STATE_MAL, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_MAG:
            if char == 'b':
                self.advance()
                return (self.STATE_MAGB, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_MAGB:
            if char == 'a':
                self.advance()
                return (self.STATE_MAGBA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_MAGBA:
            if char == 'l':
                self.advance()
                return (self.STATE_MAGBAL, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_MAGBAL:
            if char == 'i':
                self.advance()
                return (self.STATE_MAGBALI, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_MAGBALI:
            if char == 'k':
                self.advance()
                return (self.STATE_MAGBALIK, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_MAGBALIK:
            return finalize_keyword(TKN_MAGBALIK, CTRL_DLM)
        
        elif state == self.STATE_MAL:
            if char == 'i':
                self.advance()
                return (self.STATE_MALI, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_MALI:
            if char == 'n':
                self.advance()
                return (self.STATE_MALIN, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_MALIN:
            if char == 'g':
                self.advance()
                return (self.STATE_MALING, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_MALING:
            if char == 'a':
                self.advance()
                return (self.STATE_MALINGA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_MALINGA:
            if char == 'n':
                self.advance()
                return (self.STATE_MALINGAN, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_MALINGAN:
            if char == 'i':
                self.advance()
                return (self.STATE_MALINGANI, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_MALINGANI:
            return finalize_keyword(TKN_MALINGANI, CONDI_DLM)
        
        # 'n' branch
        elif state == self.STATE_N:
            if char == 'u':
                self.advance()
                return (self.STATE_NU, buffer + char)
            elif char == 'o':
                self.advance()
                return (self.STATE_NO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_NU:
            if char == 'm':
                self.advance()
                return (self.STATE_NUM, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_NUM:
            if char == 'e':
                self.advance()
                return (self.STATE_NUME, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_NUME:
            if char == 'r':
                self.advance()
                return (self.STATE_NUMER, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_NUMER:
            if char == 'o':
                self.advance()
                return (self.STATE_NUMERO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_NUMERO:
            return finalize_keyword(TKN_NUMERO, DEC_DLM)
        
        elif state == self.STATE_NO:
            if char == 't':
                self.advance()
                return (self.STATE_NOT, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_NOT:
            return finalize_keyword(TKN_NOT, LOGIC_DLM)
        
        # 'o' branch
        elif state == self.STATE_O:
            if char == 'o':
                self.advance()
                return (self.STATE_OO, buffer + char)
            elif char == 'r':
                self.advance()
                return (self.STATE_OR, buffer + char)
            elif char == 's':
                self.advance()
                return (self.STATE_OS, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_OO:
            if char == 'n':
                self.advance()
                return (self.STATE_OON, buffer + char)
            elif char == 'm':
                self.advance()
                return (self.STATE_OOM, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_OON:
            if char == 'g':
                self.advance()
                return (self.STATE_OONG, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_OONG:
            if char == 'a':
                self.advance()
                return (self.STATE_OONGA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_OONGA:
            if char == 'n':
                self.advance()
                return (self.STATE_OONGAN, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_OONGAN:
            if char == 'i':
                self.advance()
                return (self.STATE_OONGANI, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_OONGANI:
            return finalize_keyword(TKN_OONGANI, CONDI_DLM)
        
        elif state == self.STATE_OOM:
            if char == 'a':
                self.advance()
                return (self.STATE_OOMA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_OOMA:
            if char == 'l':
                self.advance()
                return (self.STATE_OOMAL, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_OOMAL:
            if char == 'i':
                self.advance()
                return (self.STATE_OOMALI, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_OOMALI:
            return finalize_keyword(TKN_OOMALI, DEC_DLM)
        
        elif state == self.STATE_OR:
            return finalize_keyword(TKN_OR, LOGIC_DLM)
        
        elif state == self.STATE_OS:
            if char == 'i':
                self.advance()
                return (self.STATE_OSI, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_OSI:
            if char == 'g':
                self.advance()
                return (self.STATE_OSIG, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_OSIG:
            if char == 'e':
                self.advance()
                return (self.STATE_OSIGE, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_OSIGE:
            return finalize_keyword(TKN_OSIGE, CTRL_DLM)
        
        # 'p' branch
        elif state == self.STATE_P:
            if char == 'r':
                self.advance()
                return (self.STATE_PR, buffer + char)
            elif char == 'i':
                self.advance()
                return (self.STATE_PI, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_PR:
            if char == 'i':
                self.advance()
                return (self.STATE_PRI, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_PRI:
            if char == 'n':
                self.advance()
                return (self.STATE_PRIN, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_PRIN:
            if char == 't':
                self.advance()
                return (self.STATE_PRINT, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_PRINT:
            return finalize_keyword(TKN_PRINT, IO_DLM)
        
        elif state == self.STATE_PI:
            if char == 'l':
                self.advance()
                return (self.STATE_PIL, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_PIL:
            if char == 'i':
                self.advance()
                return (self.STATE_PILI, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_PILI:
            if char == 'i':
                self.advance()
                return (self.STATE_PILII, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_PILII:
            if char == 'n':
                self.advance()
                return (self.STATE_PILIIN, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_PILIIN:
            return finalize_keyword(TKN_PILIIN, CONDI_DLM)
        
        # 's' branch
        elif state == self.STATE_S:
            if char == 'a':
                self.advance()
                return (self.STATE_SA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_SA:
            if char == 'k':
                self.advance()
                return (self.STATE_SAK, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_SAK:
            if char == 'l':
                self.advance()
                return (self.STATE_SAKL, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_SAKL:
            if char == 'a':
                self.advance()
                return (self.STATE_SAKLA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_SAKLA:
            if char == 'w':
                self.advance()
                return (self.STATE_SAKLAW, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_SAKLAW:
            return finalize_keyword(TKN_SAKLAW, DEC_DLM)
        
        # 't' branch
        elif state == self.STATE_T:
            if char == 'e':
                self.advance()
                return (self.STATE_TE, buffer + char)
            elif char == 'r':
                self.advance()
                return (self.STATE_TR, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_TE:
            if char == 'k':
                self.advance()
                return (self.STATE_TEK, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_TEK:
            if char == 's':
                self.advance()
                return (self.STATE_TEKS, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_TEKS:
            if char == 't':
                self.advance()
                return (self.STATE_TEKST, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_TEKST:
            if char == 'o':
                self.advance()
                return (self.STATE_TEKSTO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_TEKSTO:
            return finalize_keyword(TKN_TEKSTO, DEC_DLM)
        
        elif state == self.STATE_TR:
            if char == 'o':
                self.advance()
                return (self.STATE_TRO, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_TRO:
            if char == 'p':
                self.advance()
                return (self.STATE_TROP, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_TROP:
            if char == 'a':
                self.advance()
                return (self.STATE_TROPA, buffer + char)
            else: return handle_identifier_or_continue(char, None, None)
        
        elif state == self.STATE_TROPA:
            return finalize_keyword(TKN_TROPA, DEC_DLM)
        
        # Continue with remaining branches (k, l, m, n, o, p, s, t) in similar fashion
        # Due to length, implementing remaining states with same pattern
        
        return None  # Unknown state


# Example usage and testing
def run_lexer(source_code):
    """Run the lexer on source code and display results"""
    lexer = Lexer(source_code)
    tokens, errors = lexer.tokenize()

    if errors:
        print("=== ERRORS ===")
        for error in errors:
            print(error)
        print()

    print("=== TOKENS ===")
    for token in tokens:
        print(token)

    return tokens, errors

###############################################################
# FOR TESTING PURPOSES ONLY
###############################################################
if __name__ == '__main__':
    test_inputs = [
        # Valid declarations
        'numero A = 123;',
        'lutang B = 4.5;',
        'teksto Message = "Hello, world!";',
        'oomali Truth = oongani;',
        'oomali Falsy = malingani;',
        
        # Control flow
        'kung C >= 10:',
        'kungdiman X < 5:',
        'ediwow {',
        'loopit I in Tropa {',
        
        # Assignment operators
        'A += 1;',
        'B -= 2;',
        'C *= 3;',
        'D /= 4;',
        'Y //= 2;',
        'E %= 5;',
        'F **= 2;',
        
        # Relational operators
        'Z != 5;',
        'X == 10;',
        'Y > 3;',
        'Z < 7;',
        'A >= 15;',
        'B <= 20;',
        
        # Logical operators
        'AND OR NOT',
        'oongani OR malingani',
        
        # Functions and I/O
        'anoboi MyFunc():',
        'print("test");',
        'input()',
        'in',
        'magbalik X;',
        
        # Valid identifiers
        'MyVar = 123.456;',
        'StudentName = "John";',
        'TotalCount = 100;',
        
        # Arrays and groups
        'arayko Numbers = [1, 2, 3];',
        'grupo Person = {Name: "Ana", Age: 25};',
        
        # Comments
        '/* This is a single line comment',
        '*/ This is a multi-line comment */',
        
        # Switch case
        'piliin X:',
        'kaso 1:',
        'iba:',
        
        # Other keywords
        'awat;',
        'osige;',
        'alaws',
        'cons Pi = 3.14;',
        'saklaw',
        'tropa',
        'imbento',
        'etosayo',
        'do {',
        
        # Error cases
        'numero A=123;',  # Test delimiter error (no space after =)
        'invalid_id',  # Test lowercase identifier
        'TooLongIdentifierName123456789',  # Test long identifier
        '123abc',  # Test invalid delimiter after number
        'A B',  # Test invalid delimiter between identifiers
        '!',  # Test invalid operator
        '3.;',  # Test decimal without digits
        '"unterminated',  # Test unterminated string
        '/* unterminated comment',  # Test unterminated multi-line comment
        '@#$',  # Test invalid characters
    ]
    
    print("=" * 70)
    print("LEXER TEST SUITE")
    print("=" * 70)
    print()
    
    for i, text in enumerate(test_inputs, 1):
        print(f"TEST {i}: {text}")
        print("-" * 70)
        tokens, errors = run_lexer(text)
        print()
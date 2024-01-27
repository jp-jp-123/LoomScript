# token table for lexer.py

KEYWORDS = {
    "BOOL": "BOOL_KW",
    "BOOLEAN": "BOOL_KW",
    "CHAR": "CHAR_KW",
    "CHARACTER": "CHAR_KW",
    "ELSE": "ELSE_KW",
    "FALSE": "FALSE_KW",
    "FILEOPERATE": "FILEOP_KW",
    "GET": "GET_KW",
    "IF": "IF_KW",
    "INPUT": "INP_KW",
    "LOOP": "LOOP_KW",
    "NUM": "NUM_KW",
    "NUMBER": "NUM_KW",
    "OUTPUT": "OUT_KW",
    "SET": "SET_KW",
    "THEN": "THEN_KW",
    "TO": "TO_KW",
    "TODO": "TODO_KW",
    "TRUE": "TRUE_KW",
    "TRUEFALSE": "TRUEFALSE_KW",
}

SPECIAL_CHARACTERS = {
    '.': "PERIOD_SC",
    '+': "PLUS_SC",
    '-': "HYPHEN_SC",
    '*': "ASTERISK_SC",
    '/': "SLASH_SC",
    '%': "PERCENT_SC",
    '<': "OP_ABRACK_SC",
    '>': "CLO_ABRACK_SC",
    '=': "EQUAL",
    '\"': "DQUOTE_SC",
    '\'': "SQUOTE_SC",
    ',': "COMMA_SC",
    ';': "SEMICOLON_SC",
    '|': "PIPE_SC",
    '!': "EXCLAMATION_SC",
    '(': "LPAREN_SC",
    ')': "RPAREN_SC",
    '[': "LSQBRACK_SC",
    ']': "RSQBRACK_SC",
    '{': "LCBRACK_SC",
    '}': "RCBRACK_SC",
    '_': "UNDERSCORE_SC",
    '^': "CARET_SC",
    '~': "TILDE_SC",
    '&': "AMPERSAND_SC",
    ' ': "SPACE"
}

OPERATORS = {
    '+': "ARITHMETIC_ADD",
    '-': "ARITHMETIC_SUBTRACT",
    '*': "ARITHMETIC_MULTIPLY",
    '/': "ARITHMETIC_DIVIDE",
    '%': "ARITHMETIC_MODULO",
    '~': "ARITHMETIC_INTEGER_DIVIDE",
    '^': "ARITHMETIC_EXPONENT",
    '=': "ASSIGN_OP",
    '>': "GREATER_THAN",
    '<': "LESS THAN",
    '!': "NOT_OP"
}

DOUBLE_OPERATORS = {
    '++': "UNARY_INCREMENT",
    '--': "UNARY_DECREMENT",
    '+=': "ASSIGN_OP_ADD",
    '-=': "ASSIGN_OP_SUBTRACT",
    '*=': "ASSIGN_OP_MULTIPLY",
    '/=': "ASSIGN_OP_DIVIDE",
    '%=': "ASSIGN_OP_MODULUS",
    '~=': "ASSIGN_OP_INTEGER_DIVIDE",
    '==': "EQUAL_TO",
    '!=': "NOT_EQUAL_TO",
    '>=': "GREATER_THAN_EQUAL",
    '<=': "LESS_THAN_EQUAL",
    '||': "OR_OP",
    '&&': "AND_OP"
}

UNARY_OPS = {
    '++': "UNARY_INCREMENT",
    '--': "UNARY_DECREMENT",
    '+': "UNARY_ADD",
    '-': "UNARY_SUBTRACT"
}
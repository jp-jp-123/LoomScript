# token table for lexerLegacy.py

KEYWORDS = {
    "BOOL": "BOOL_KW",
    "CHAR": "CHAR_KW",
    "ELSE": "ELSE_KW",
    "FALSE": "FALSE_KW",
    "FILEOPERATE": "FILEOP_KW",
    "GET": "GET_KW",
    "IF": "IF_KW",
    "INPUT": "INP_KW",
    "LOOP": "LOOP_KW",
    "NUM": "NUM_KW",
    "OUTPUT": "OUT_KW",
    "SET": "SET_KW",
    "THEN": "THEN_KW",
    "TO": "TO_KW",
    "TODO": "TODO_KW",
    "TRUE": "TRUE_KW",
    "TRUEFALSE": "TRUEFALSE_KW",
}

SPECIAL_CHARACTERS = {
    '.': "PERIOD",
    '+': "PLUS",
    '-': "HYPHEN",
    '*': "ASTERISK",
    '/': "SLASH",
    '%': "PERCENT",
    '<': "OPEN_ANGLE_BRACKET",
    '>': "CLOSE_ANGLED_BRACKET",
    '=': "EQUAL",
    '\"': "DOUBLE_QUOTATION",
    '\'': "SINGLE_QUOTATION",
    ',': "COMMA",
    ';': "SEMICOLON",
    '|': "PIPE",
    '!': "EXCLAMATION",
    '(': "OPEN_PARENTHESIS",
    ')': "CLOSE_PARENTHESIS",
    '[': "OPEN_SQUARE_BRACKET",
    ']': "CLOSE_SQUARE_BRACKET",
    '{': "OPEN_CURLY_BRACKET",
    '}': "CLOSE_CURLY_BRACKET",
    '_': "UNDERSCORE",
    '^': "CARET",
    '~': "TILDE",
    '&': "AMPERSAND",
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
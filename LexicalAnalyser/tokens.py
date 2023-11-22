# token table for lexerLegacy.py

KEYWORDS = {
    "BOOL": "kw",
    "CHAR": "kw",
    "ELSE": "kw",
    "FALSE": "kw",
    "GET": "kw",
    "IF": "kw",
    "INPUT": "kw",
    "LOOP": "kw",
    "NUM": "kw",
    "OUTPUT": "kw",
    "SET": "kw",
    "THEN": "kw",
    "TO": "kw",
    "TODO": "kw",
    "TRUE": "kw",
    "TRUEFALSE": "kw",
}

SPECIAL_CHARACTERS = {
    '.': "period",
    '+': "plus",
    '-': "hyphen",
    '*': "asterisk",
    '/': "slash",
    '%': "percent",
    '<': "open_angle_bracket",
    '>': "close_angled_bracket",
    '=': "equal",
    '\"': "double_quotation",
    '\'': "single_quotation",
    ',': "comma",
    ';': "semicolon",
    '|': "pipe",
    '!': "exclamation",
    '(': "open_parenthesis",
    ')': "close_parenthesis",
    '[': "open_square_bracket",
    ']': "close_square_bracket",
    '_': "underscore",
    '^': "caret",
    '~': "tilde",
    '&': "ampersand",
    ' ': "space"
}

OPERATORS = {
    '+': "arithmetic_add",
    '-': "arithmetic_subtract",
    '*': "arithmetic_multiply",
    '/': "arithmetic_divide",
    '%': "arithmetic_modulo",
    '~': "arithmetic_integer_divide",
    '^': "arithmetic_exponent",
    '=': "assign_op",
    '>': "greater_than",
    '<': "less than",
}

DOUBLE_OPERATORS = {
    '++': "unary_increment",
    '--': "unary_decrement",
    '+=': "assign_op_add",
    '-=': "assign_op_subtract",
    '*=': "assign_op_multiply",
    '/=': "assign_op_divide",
    '%=': "assign_op_modulus",
    '~=': "assign_op_integer_divide",
    '==': "equal_to",
    '!=': "not_equal_to",
    '>=': "greater_than_equal",
    '<=': "less_than_equal",
    '!': "NOT_op",
    '||': "OR_op",
    '&&': "AND_op"
}

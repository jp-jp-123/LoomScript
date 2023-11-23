UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

LOWERCASE = "abcdefghijklmnopqrstuvwxyz"

DIGITS = "0123456789"

NOT_IN_DECIMAL = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" + ' '

SPECIAL_CHARSET = {
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

DOUBLES = {
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

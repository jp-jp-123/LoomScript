# token: right_assoc, is_binary, precedence
math = {
    "ARITHMETIC_EXPONENT": [True, True, 3],
    "ARITHMETIC_MULTIPLY": [False, True, 2],
    "ARITHMETIC_DIVIDE": [False, True, 2],
    "ARITHMETIC_MODULO": [False, True, 2],
    "ARITHMETIC_INTEGER_DIVIDE": [False, True, 2],
    "ARITHMETIC_ADD": [False, True, 1],
    "ARITHMETIC_SUBTRACT": [False, True, 1]
}

# pre-fix
unary_pref = {
    "UNARY_INCREMENT": [False, False, 2],
    "UNARY_DECREMENT": [False, False, 2],
    "UNARY_ADD": [False, False, 2],
    "UNARY_SUBTRACT": [False, False, 2],
}

# post-fix
unary_posf = {
    "UNARY_INCREMENT": [True, False, 1],
    "UNARY_DECREMENT": [True, False, 1],
    "UNARY_ADD": [True, False, 1],
    "UNARY_SUBTRACT": [True, False, 1],
}

boolean = {
    "EQUAL_TO": [False, True, 1],  # 0
    "NOT_EQUAL_TO": [False, True, 1],  # 1
    "GREATER_THAN": [False, True, 1],  # 2
    "LESS THAN": [False, True, 1],  # 3
    "GREATER_THAN_EQUAL": [False, True, 1],  # 4
    "LESS_THAN_EQUAL": [False, True, 1],  # 5
    "NOT_OP": [False, True, 2],  # 6
    "AND_OP": [False, True, 3],  # 7
    "OR_OP": [False, True, 3],  # 8
    "ASSIGN_OP": [True, True, 4],  # 9
    "ASSIGN_OP_ADD": [True, True, 4],  # 10
    "ASSIGN_OP_SUBTRACT": [True, True, 4],  # 11
    "ASSIGN_OP_MULTIPLY": [True, True, 4],  # 12
    "ASSIGN_OP_DIVIDE": [True, True, 4],  # 13
    "ASSIGN_OP_MODULUS": [True, True, 4],  # 14
    "ASSIGN_OP_INTEGER_DIVID": [True, True, 4],  # 15
}
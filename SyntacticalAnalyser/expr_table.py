# token: [right_assoc, is_binary, precedence]
# higher precedence = higher number
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
    "EQUAL_TO": [False, True, 4],  # 0
    "NOT_EQUAL_TO": [False, True, 4],  # 1
    "GREATER_THAN": [False, True, 4],  # 2
    "LESS THAN": [False, True, 4],  # 3
    "GREATER_THAN_EQUAL": [False, True, 4],  # 4
    "LESS_THAN_EQUAL": [False, True, 4],  # 5
    "NOT_OP": [False, True, 3],  # 6
    "AND_OP": [False, True, 2],  # 7
    "OR_OP": [False, True, 2],  # 8
    "ASSIGN_OP": [True, True, 1],  # 9
    "ASSIGN_OP_ADD": [True, True, 1],  # 10
    "ASSIGN_OP_SUBTRACT": [True, True, 1],  # 11
    "ASSIGN_OP_MULTIPLY": [True, True, 1],  # 12
    "ASSIGN_OP_DIVIDE": [True, True, 1],  # 13
    "ASSIGN_OP_MODULUS": [True, True, 1],  # 14
    "ASSIGN_OP_INTEGER_DIVIDE": [True, True, 1],  # 15
}

all_op = {
    "POSF_UNARY_INCREMENT": [False, False, 9],
    "POSF_UNARY_DECREMENT": [False, False, 9],
    "POSF_UNARY_ADD": [False, False, 9],
    "POSF_UNARY_SUBTRACT": [False, False, 9],
    "PREF_UNARY_INCREMENT": [True, False, 8],
    "PREF_UNARY_DECREMENT": [True, False, 8],
    "PREF_UNARY_ADD": [True, False, 8],
    "PREF_UNARY_SUBTRACT": [True, False, 8],
    "ARITHMETIC_EXPONENT": [True, True, 7],
    "ARITHMETIC_MULTIPLY": [False, True, 6],
    "ARITHMETIC_DIVIDE": [False, True, 6],
    "ARITHMETIC_MODULO": [False, True, 6],
    "ARITHMETIC_INTEGER_DIVIDE": [False, True, 5],
    "ARITHMETIC_ADD": [False, True, 5],
    "ARITHMETIC_SUBTRACT": [False, True, 5],
    "EQUAL_TO": [False, True, 4],  # 0
    "NOT_EQUAL_TO": [False, True, 4],  # 1
    "GREATER_THAN": [False, True, 4],  # 2
    "LESS_THAN": [False, True, 4],  # 3
    "GREATER_THAN_EQUAL": [False, True, 4],  # 4
    "LESS_THAN_EQUAL": [False, True, 4],  # 5
    "NOT_OP": [False, True, 3], #6
    "AND_OP": [False, True, 2],  # 7
    "OR_OP": [False, True, 2],  # 8
    "ASSIGN_OP_ADD": [True, True, 1],  # 10
    "ASSIGN_OP_SUBTRACT": [True, True, 1],  # 11
    "ASSIGN_OP_MULTIPLY": [True, True, 1],  # 12
    "ASSIGN_OP_DIVIDE": [True, True, 1],  # 13
    "ASSIGN_OP_MODULUS": [True, True, 1],  # 14
    "ASSIGN_OP_INTEGER_DIVIDE": [True, True, 1],  # 15

}

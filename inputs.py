import gamehandler as gh

menu_items = [
    '(1) Regular Multiplication',
    '(2) Root finding (Result integer)',
    '(3) Regular root finding',
    '(4) Matrix Determinant',
    '(5) Regular Division',
    '(6) Random multiplication',
    '(7) Matrix multiplication',
]

GAMES = [
    gh.regMul,
    gh.introot,
    gh.regroot,
    gh.detgame,
    gh.regDiv,
    gh.funMul,
    gh.matMul,
]

GAME_PARAMS = [
    [
        ['Number of digits', 'ndigits'],
    ],
    [
        ['Number of digits', 'ndigits'],
        ['nth Root', 'n'],
    ],
    [
        ['Number of digits', 'ndigits'],
        ['nth Root', 'n'],
        ['Accurate to how many digits?', 'resdig']
    ],
    [
        ['Dimensions', 'dim'],
        ['Number of digits in each entry', 'ndigits']
    ],
    [
        ['Numerator Digits', 'ndigitsnum'],
        ['Denominator Digits', 'ndigitsdenom'],
        ['Result Digits', 'resdig']    
    ],
    [
        ['Rough number of digits', 'ndigits'],
    ],
    [
        ['Dimensions', 'dim'],
        ['Number of matrices to multiply', 'num'],
        ['Number of digits in each entry', 'ndigits'],
        
    ],
]

GAME_SETTING_PARAMS = [
    [
        ['Mode', 'mode'],
        ['Rounds', 'rounds'],
    ],
]

inpt_dict = {
    'ndigits' : 5
}

game_settings = {
    'mode' : 1,
    'rounds' : 3,
    'game' : 0,
    'countdown' : True
}


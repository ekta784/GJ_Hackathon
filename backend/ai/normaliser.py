import re

# Mapping based on position demands (alpha vs digit)
ALPHA_CORRECTIONS = {
    '0': 'O',
    '1': 'I',
    '8': 'B',
    '5': 'S',
    '2': 'Z',
    '6': 'G',
    '4': 'A',
    '7': 'T',
    'D': 'O', # Optional additional confusions
    'Q': 'O'
}

DIGIT_CORRECTIONS = {
    'O': '0',
    'D': '0',
    'Q': '0',
    'I': '1',
    'L': '1',
    'B': '8',
    'S': '5',
    'Z': '2',
    'G': '6',
    'A': '4',
    'T': '7'
}

VALID_STATES = [
    "AP", "AR", "AS", "BR", "CG", "GA", "GJ", "HR", "HP", "JH",
    "KA", "KL", "MP", "MH", "MN", "ML", "MZ", "NL", "OD", "PB",
    "RJ", "SK", "TN", "TG", "TR", "UP", "UK", "WB", "AN", "CH",
    "DN", "DD", "DL", "JK", "LA", "LD", "PY"
]

STATE_CONFUSIONS = {
    "HH": "MH",
    "NN": "MH",
    "NH": "MH",
    "HN": "MH",
    "GH": "GJ",
    "CJ": "GJ",
    "G3": "GJ",
    "BJ": "GJ",
    "P8": "PB",
    "FB": "PB",
    "0L": "DL",
    "OL": "DL",
    "DI": "DL",
    "K4": "KA",
    "R3": "RJ"
}

def correct_char(c: str, expected_type: str) -> str:
    """Corrects character based on expected type ('alpha' or 'digit')."""
    if expected_type == 'alpha':
        return ALPHA_CORRECTIONS.get(c, c) if c.isdigit() else c
    elif expected_type == 'digit':
        return DIGIT_CORRECTIONS.get(c, c) if c.isalpha() else c
    return c

def normalize_plate(plate_text: str) -> str:
    """
    Attempts to normalize a raw OCR string to the Indian plate grammar:
    [2 alpha state][1-2 digit RTO][0-3 alpha series][4 digit number]
    """
    plate_text = plate_text.upper().replace(" ", "").replace("-", "")
    
    # Needs at least State + RTO + Number (e.g., GJ011234) = 8 chars
    # Max is State + RTO + 3 Series + Number = 11 chars
    if len(plate_text) < 8 or len(plate_text) > 11:
        return plate_text # Return as is if format is wildly wrong

    normalized = list(plate_text)

    # 1. First 2 characters must be ALPHA (State)
    for i in range(2):
        normalized[i] = correct_char(normalized[i], 'alpha')
    
    state_code = "".join(normalized[0:2])
    if state_code not in VALID_STATES:
        if state_code in STATE_CONFUSIONS:
            normalized[0:2] = list(STATE_CONFUSIONS[state_code])
        elif state_code[1] == 'H' and state_code[0] in ['H', 'N', 'W']:
            normalized[0:2] = ['M', 'H']
        elif state_code[0] == 'G' and state_code[1] in ['3', 'H', 'I', '1']:
            normalized[0:2] = ['G', 'J']
        elif state_code[1] == 'L' and state_code[0] in ['0', 'O', 'D']:
            normalized[0:2] = ['D', 'L']
    
    # 2. Last 4 characters must be DIGITS (Number)
    for i in range(len(normalized)-4, len(normalized)):
        normalized[i] = correct_char(normalized[i], 'digit')

    # 3. Middle part (RTO + Series)
    middle = normalized[2:-4]
    
    # RTO is 1-2 digits. Let's assume 2 digits for most cases unless middle is very short.
    # We will enforce first 2 chars of middle to be DIGITS, rest to be ALPHA
    if len(middle) >= 2:
        middle[0] = correct_char(middle[0], 'digit')
        middle[1] = correct_char(middle[1], 'digit')
        
        for i in range(2, len(middle)):
            middle[i] = correct_char(middle[i], 'alpha')
    elif len(middle) == 1:
        middle[0] = correct_char(middle[0], 'digit')
        
    normalized[2:-4] = middle
    return "".join(normalized)

KNOWN_CONFUSIONS = {
    ('0', 'O'), ('0', 'D'), ('0', 'Q'),
    ('1', 'I'), ('1', 'L'),
    ('8', 'B'), ('5', 'S'),
    ('2', 'Z'), ('6', 'G'),
    ('4', 'A'), ('7', 'T')
}

def sub_cost(a: str, b: str) -> float:
    """Weighted Levenshtein substitution cost"""
    if a == b:
        return 0.0
    if (a, b) in KNOWN_CONFUSIONS or (b, a) in KNOWN_CONFUSIONS:
        return 0.3
    if a.isdigit() == b.isdigit():
        return 0.7
    return 1.0

def weighted_levenshtein(s1: str, s2: str) -> float:
    """Computes the distance between two strings using weighted substitution costs."""
    if len(s1) < len(s2):
        return weighted_levenshtein(s2, s1)
    
    if len(s2) == 0:
        return float(len(s1))
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + sub_cost(c1, c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

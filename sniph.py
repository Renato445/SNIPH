#!/bin/python
# Sniph test version 0.5

import sys, random

# Returns list of indices where c is in S.
def findOccurences(S, c):
    return [i for i, letter in enumerate(S) if letter == c]
    
def cipher(char_set, phrase, msg, N, R, C, offset):
    
    encoding = ''
    key = 0 # Current index in passhprase.
    shift = 0 # Holds shift value for each character's path.
    
    for i in range(0, len(msg)):
        shift = 0 # Comment out for continuous shift value.
        for j in range(0, N-2):
            pos = char_set.index(phrase[key % len(phrase)]) % size 
            # Character's position in set.
            # Mod by table size to wrap in table.
            # Key mod len(phrase) gives each character of passphrase in sequence
            # and goes back to the 1st character after all are used.
            
            # Get coord.
            row_loc = pos // C + 1
            col_loc = pos % C + 1
            if row_loc == 10: row_loc = 0
            if col_loc == 10: col_loc = 0
            
            shift += (row_loc - col_loc) # x-y or row - col
            key += 1 # Index for next character in passphrase.
        
        # Shift character set by previously calculated value.
        shifted_set = char_set[shift:len(char_set)] + char_set[0:shift]
        
        # Index holds all locations of character to be encoded within the
        # shifted character set.
        index = findOccurences(shifted_set, msg[i])
        
        # 'Randomly' select one of those locations.
        rand_loc = random.randint(0, sys.maxsize) % len(index)
        rand_choice = index[rand_loc]
        
        # Get coord for which Nth table to go to
        # d2 represents depth 1 above leaves aka N-1.
        d2 = rand_choice // size
        d2_row = d2 // C + 1
        d2_col = d2 % C + 1
        if d2_row == 10: d2_row = 0
        if d2_col == 10: d2_col = 0
        s = str(d2_row) + str(d2_col)
        
        # Get coord char in Nth table.
        # dN represents depth of N.
        dN = rand_choice % size
        dN_row = dN // C + 1
        dN_col = dN % C + 1
        if dN_row == 10: dN_row = 0
        if dN_col == 10: dN_col = 0
        s += str(dN_row) + str(dN_col)
        # s now holds 4 integers representing a character's location in the last.
        # 2 tables taking into account the shift.
        
        encoding += s # Cipher text is the concatenation of the 4 values for each character.
        
    cipher_text = ''
    # 'Random' path wrapping.
    # Decides to alter each value in path by row/col size or leave it alone.
    for i in range(len(encoding)):
        x = int(encoding[i]) # Each value in encoding.
        r = random.randint(0, sys.maxsize) # Random integer.
        w = 1 # Number of possible wraps in row or column.
        t = x # Temp val to determine w.
        
        if i % 2 == 0: # Row.
            t += R
            while t < 10: # This loop gets wrap number.
                w += 1
                t += R
            if x == R: # If val = # of rows, 0 is also a possible index.
                x = 0
                w += 1
            # 'Randomly' alter character mapping values.
            # Note: does not affect actual location, obscures
            # table size in analysis.
            x += (r % w) * R
            
        else: # Column.
            t += C
            while t < 10:
                w += 1
                t += C
            if x == C:
                x = 0
                w += 1
            x += (r % w) * C
            
        cipher_text += str(x) # Add new value to final output.
        
    
    # Return final text with a shift determined by input.
    cipher_text = cipher_text[offset:] + cipher_text[0:offset]
    return cipher_text

def decipher(char_set, phrase, msg, N, R, C):
    
    # Revert values to fit table dimensions and place in code string.
    code = ''
    for i in range(len(msg)):
        t = 0
        if i % 2 == 0: 
            t = int(msg[i]) % R
            if t == 0:
                t = R
        else: 
            t = int(msg[i]) % C
            if t == 0:
                t = C
        if t == 10:
            t = 0
        code += str(t)
    
    # Split values of code into groups of four representing each character.
    characters = []
    for i in range(len(code) // 4):
        characters.append(code[4*i:4*(i+1)])
        
    decoding = ''
    key = 0 # Current index in passphrase.
    for i in range(len(characters)):
        shift = 0
        for j in range(0, N-2): # Get path to (N-2)th table to calculate shift.
            # Same as in cipher above.
            pos = char_set.index(phrase[key % len(phrase)]) % size 
            c = phrase[key % len(phrase)]
            
            # Get coord.
            row_loc = pos // C + 1
            col_loc = pos % C + 1
            if row_loc == 10: row_loc = 0
            if col_loc == 10: col_loc = 0
            
            shift += (row_loc - col_loc) # x-y or row - col
            key += 1 # Index for next character in passphrase.
        
        # Shift character set by previously calculated value.
        shifted_set = char_set[shift:len(char_set)] + char_set[0:shift]
        
        # Reverse coordinates of encoded message.
        
        # Each character is encoded in string row1col1row2col2.
        row1 = int(characters[i][0])
        if row1 == 0: row1 = 10 # Check for tens.
        col1 = int(characters[i][1])
        if col1 == 0: col1 = 10
        row2 = int(characters[i][2])
        if row2 == 0: row2 = 10
        col2 = int(characters[i][3])
        if col2 == 0: col2 = 10
        
        # This equation pinpoints the position of the character with
        # the path of the last 2 tables.
        char_pos = size * (C * (row1 - 1) + col1 - 1) + (C * (row2 - 1) + col2)
    
        # Add this character to our decoded message.
        # -1 to go from pos to index.
        decoding += shifted_set[char_pos - 1] 
        
    return decoding # Return decoded message.
    
if len(sys.argv) == 1:
    print('\n  :: SNIPH Version 0.5 ::\n')
    
    N = 4 # table depth
    R = 0 # table rows
    C = 0 # table columns
    print('Input Table Dimensions')
    R = input('Number of rows (empty for default): ')
    if len(R) == 0: R = 4
    else: R = int(R)
    if R < 4: 
        print('Value must be greater than or equal to 4. Defaulting to 4.\n')
        R = 4
    elif R > 10: 
        print('Value must be less than or equal to 10. Defaulting to 10.\n')
        R = 10
        
    C = input('Number of columns (empty for default): ')
    if len(C) == 0: C = 4
    else: C = int(C)
    if C < 4: 
        print('Value must be greater than or equal to 4. Defaulting to 4.\n')
        C = 4
    elif C > 10: 
        print('Value must be less than or equal to 10. Defaulting to 10.\n')
        C = 10
        
    inp = input('Number of seated dimensions (empty for default): ')
    if len(inp) == 0:
        N = 4
    else:
        N = int(inp)
    if N < 4:
        N = 4
    
    # # Verify input was parsed correctly.
    # print('Depth = {} \nTable size = {} x {}'.format(N, R, C))
    
    size = R * C # table size, area of the table
    
    char_set = ('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,?!:;\'\"/\\|<>+-=(){}[]`'
    '~@#$%^&*1234567890 \n')
    # Repeat char set to fill (R*C)^2 spaces.
    # i.e 3x3 = 9 tables slots with 9 tables holding characters in last level
    # = 9^2 = 81 characters
    while len(char_set) < pow(size, 2):
        char_set += char_set
    char_set = char_set[0:pow(size,2)]
    
    # Offset shifts output.
    off_in = input('Offset variable to shift text (empty = 0): ')
    offset = 0
    if len(off_in) != 0: offset = int(off_in)
    
    # Phrase = passphrase.
    phrase = ''
    phrase = input('\nEnter passphrase: ')
    while len(phrase) == 0: # Check phrase.
        phrase = input('You must enter a passphrase: ')
        
    phrase = phrase.upper()
    
    flag = input('Cipher (C) or Decipher (D): ')
    if not(flag == 'd' or flag == 'D' or flag == 'c' or flag == 'C'):
        flag = ''
    while len(flag) == 0: # Check option.
        print('I need to know if I\'m ciphering or deciphering.')
        flag = input('Cipher (C) or Decipher (D)?: ')
        if not(flag == 'd' or flag == 'D' or flag == 'c' or flag == 'C'):
            flag = ''
    flag = flag.lower()
    
    # Message is either plain-text or ciphertext.
    msg = ''
    if flag == 'd':
        msg = input('Enter ciphertext:\n')
        while len(msg) == 0:
            print('Text cannot be empty')
            msg = input('Enter ciphertext:\n')
    else:
        msg = input('Enter plaintext:\n')
        while len(msg) == 0:
            print('Text cannot be empty')
            msg = input('Enter plaintext:\n')
    # msg = msg.upper();
    
    if flag == 'c':
        encoding = cipher(char_set, phrase, msg, N, R, C, offset)
        print('\nResult:\n', encoding)
        
    elif flag == 'd':
        msg = msg[-1*offset:] + msg[0:-1*offset] # Reverse offset before decoding.
        decoded = decipher(char_set, phrase, msg, N, R, C)
        print('\nResult:\n', decoded)
    
else:
    if '--help' in sys.argv:
        print('For more information go to: https://snerx.com/sniph')

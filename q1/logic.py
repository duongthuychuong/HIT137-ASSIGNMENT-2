# This program implements a custom encryption and decryption system using two shift values.
# Each character is transformed based on its range (a–m, n–z, A–M, N–Z) with different rules.
#
# The decryption function reverses each rule by applying the opposite shift using the same
# values of shift1 and shift2. However, it cannot always recover the exact original text.
#
# This is because the encryption rule depends on the original character’s range, which is
# not known during decryption. If the encrypted character falls into a different range,
# the wrong reverse rule may be applied.
#
# In addition, collisions may occur where different characters produce the same encrypted
# result. In such cases, it is mathematically impossible to determine the original character.
#
# Therefore, the decryption process is not fully reversible in all situations.
# logic.py
def shift_char(char, amount, base):
    pos = ord(char) - base
    new_pos = (pos + amount) % 26
    return chr(new_pos + base)

def encrypt_char(char, shift1, shift2):
    if char.islower():
        if 'a' <= char <= 'm':
            return shift_char(char, shift1 * shift2, ord('a')), 'L'
        else:
            return shift_char(char, -(shift1 + shift2), ord('a')), 'U'
    elif char.isupper():
        if 'A' <= char <= 'M':
            return shift_char(char, -shift1, ord('A')), 'L'
        else:
            return shift_char(char, shift2 ** 2, ord('A')), 'U'
    else:
        return char, 'O'

def decrypt_char(char, tag, shift1, shift2):
    if char.islower():
        if tag == 'L':
            return shift_char(char, -(shift1 * shift2), ord('a'))
        elif tag == 'U':
            return shift_char(char, shift1 + shift2, ord('a'))
    elif char.isupper():
        if tag == 'L':
            return shift_char(char, shift1, ord('A'))
        elif tag == 'U':
            return shift_char(char, -(shift2 ** 2), ord('A'))
    return char

def encrypt_text(text, shift1, shift2):
    chars = []
    tags = []
    for c in text:
        ec, tag = encrypt_char(c, shift1, shift2)
        chars.append(ec)
        tags.append(tag)
    return ''.join(chars), ''.join(tags)

def decrypt_text(text, shift1, shift2, tags):
    result = []
    for c, tag in zip(text, tags):
        result.append(decrypt_char(c, tag, shift1, shift2))
    return ''.join(result)

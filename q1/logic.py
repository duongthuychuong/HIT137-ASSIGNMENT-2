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
    """
    This function shifts a single letter.
    
    char   = the letter to shift (e.g. 'a')
    amount = how many positions to shift (positive = forward, negative = backward)
    base   = starting point of the alphabet (ord('a')=97 for lowercase, ord('A')=65 for uppercase)
    
    Steps:
    Convert letter to number → add/subtract → use %26 to stay in range → convert back to letter
    """
    pos = ord(char) - base          # Convert letter to a number 0~25
    new_pos = (pos + amount) % 26   # Shift it, use %26 to prevent going out of range
    return chr(new_pos + base)      # Convert back to a letter


def encrypt_char(char, shift1, shift2):
    """
    Encrypt a single character.
    """
    # ---- Lowercase letters ----
    if char.islower():
        if 'a' <= char <= 'm':        # First half: a-m
            amount = shift1 * shift2  # Shift forward
            return shift_char(char, amount, ord('a'))
        else:                          # Second half: n-z
            amount = -(shift1 + shift2)  # Shift backward (negative = backward)
            return shift_char(char, amount, ord('a'))

    # ---- Uppercase letters ----
    elif char.isupper():
        if 'A' <= char <= 'M':        # First half: A-M
            amount = -shift1          # Shift backward
            return shift_char(char, amount, ord('A'))
        else:                          # Second half: N-Z
            amount = shift2 ** 2      # Shift forward by shift2 squared
            return shift_char(char, amount, ord('A'))

    # ---- Everything else (numbers, spaces, punctuation) ----
    else:
        return char  # Return unchanged


def decrypt_char(char, shift1, shift2):
    """
    Decrypt a single character (exact reverse of encryption!)
    """
    # ---- Lowercase letters ----
    if char.islower():
        if 'a' <= char <= 'm':
            # Encryption shifted forward by shift1*shift2, so decrypt shifts backward
            amount = -(shift1 * shift2)
            return shift_char(char, amount, ord('a'))
        else:
            # Encryption shifted backward by shift1+shift2, so decrypt shifts forward
            amount = shift1 + shift2
            return shift_char(char, amount, ord('a'))

    elif char.isupper():
        if 'A' <= char <= 'M':
            # Encryption shifted backward by shift1, so decrypt shifts forward
            amount = shift1
            return shift_char(char, amount, ord('A'))
        else:
            # Encryption shifted forward by shift2², so decrypt shifts backward
            amount = -(shift2 ** 2)
            return shift_char(char, amount, ord('A'))

    else:
        return char


def encrypt_text(text, shift1, shift2):
    """
    Encrypt an entire block of text.
    Simply applies encrypt_char to every single character.
    """
    result = ""
    for char in text:
        result += encrypt_char(char, shift1, shift2)
    return result


def decrypt_text(text, shift1, shift2):
    """
    Decrypt an entire block of text.
    """
    result = ""
    for char in text:
        result += decrypt_char(char, shift1, shift2)
    return result

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
def encrypt_char(c, shift1, shift2):
    if c.islower():
        if 'a' <= c <= 'm':
            shift = shift1 * shift2
            new_index = (ord(c) - ord('a') + shift) % 26
        else:
            shift = shift1 + shift2
            new_index = (ord(c) - ord('a') - shift) % 26
        return chr(new_index + ord('a'))

    elif c.isupper():
        if 'A' <= c <= 'M':
            shift = shift1
            new_index = (ord(c) - ord('A') - shift) % 26
        else:
            shift = shift2 ** 2
            new_index = (ord(c) - ord('A') + shift) % 26
        return chr(new_index + ord('A'))

    else:
        return c


def decrypt_char(c, shift1, shift2):
    if c.islower():
        if 'a' <= c <= 'm':
            shift = shift1 * shift2
            new_index = (ord(c) - ord('a') - shift) % 26
        else:
            shift = shift1 + shift2
            new_index = (ord(c) - ord('a') + shift) % 26
        return chr(new_index + ord('a'))

    elif c.isupper():
        if 'A' <= c <= 'M':
            shift = shift1
            new_index = (ord(c) - ord('A') + shift) % 26
        else:
            shift = shift2 ** 2
            new_index = (ord(c) - ord('A') - shift) % 26
        return chr(new_index + ord('A'))

    else:
        return c

def encrypt_text(text, shift1, shift2):
    return ''.join(encrypt_char(c, shift1, shift2) for c in text)


def decrypt_text(text, shift1, shift2):
    return ''.join(decrypt_char(c, shift1, shift2) for c in text)
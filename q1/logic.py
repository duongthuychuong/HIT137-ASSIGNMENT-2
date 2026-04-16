# This program implements a custom encryption and decryption system using two shift values.
# Each character is transformed based on its range (a–m, n–z, A–M, N–Z) with different rules.
#
# The decryption function reverses each rule by applying the opposite shift using the same
# values of shift1 and shift2. However, it cannot always recover the exact original text.
#
# LIMITATION 1: BOUNDARY CROSSING
#   The encryption rule depends on the original character's range (a–m or n–z).
#   After encryption, the character may land in a different range.
#   During decryption, the wrong reverse rule is applied because the range check
#   sees the encrypted character's position, not the original.
#
#   Example with shift1=1, shift2=3:
#     'o' is in n–z (index 14), shift = 1+3 = 4
#     encrypt: (14 - 4) % 26 = 10 → 'k'  (now in a–m!)
#     decrypt 'k' using a–m rule: (10 - 3) % 26 = 7 → 'h'  ✗ expected 'o'
#
# LIMITATION 2: COLLISIONS
#   Two different source characters can encrypt to the same result.
#   It is then mathematically impossible to determine the original character.
#
#   Example with shift1=3, shift2=4:
#     'g' is in a–m (index 6),  shift = 3*4 = 12
#     encrypt: (6 + 12) % 26 = 18 → 's'
#
#     'z' is in n–z (index 25), shift = 3+4 = 7
#     encrypt: (25 - 7) % 26 = 18 → 's'
#
#     Both 'g' and 'z' encrypt to 's' — decryption cannot recover both correctly.
#
# ROOT CAUSE:
#   Both limitations arise because the two halves use different shift amounts
#   and directions, allowing their output ranges to overlap. A fully invertible
#   cipher requires a one-to-one mapping between input and output characters.
#
# WHEN IT WORKS CORRECTLY:
#   The cipher is fully reversible when shift values are small enough that no
#   character crosses the half-alphabet boundary after encryption.
#   Safe example: shift1=1, shift2=2
#     shift1 * shift2 = 2  (a–m moves at most 2 positions forward)
#     shift1 + shift2 = 3  (n–z moves at most 3 positions backward)
#     shift2 ** 2    = 4   (N–Z moves at most 4 positions forward)
#   These are small enough that no character crosses the m/n or M/N boundary.

def encrypt_char(c, shift1, shift2):
    # Encrypt one character based on its group

    if c.islower():
        if 'a' <= c <= 'm':
            # First half lowercase → shift forward
            shift = shift1 * shift2
            new_index = (ord(c) - ord('a') + shift) % 26
        else:
            # Second half lowercase → shift backward
            shift = shift1 + shift2
            new_index = (ord(c) - ord('a') - shift) % 26
        return chr(new_index + ord('a'))

    elif c.isupper():
        if 'A' <= c <= 'M':
            # First half uppercase → shift backward
            shift = shift1
            new_index = (ord(c) - ord('A') - shift) % 26
        else:
            # Second half uppercase → stronger forward shift
            shift = shift2 ** 2
            new_index = (ord(c) - ord('A') + shift) % 26
        return chr(new_index + ord('A'))

    # Keep symbols, numbers unchanged
    return c


def decrypt_char(c, shift1, shift2):
    # Try to reverse the encryption

    # IMPORTANT:
    # This assumes the encrypted character is still in the same group.
    # If it moved to another group, the result may be wrong.

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
    # Apply encryption to the whole string
    return ''.join(encrypt_char(c, shift1, shift2) for c in text)


def decrypt_text(text, shift1, shift2):
    # Apply decryption to the whole string
    return ''.join(decrypt_char(c, shift1, shift2) for c in text)
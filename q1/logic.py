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
    pass


def decrypt_text(text, shift1, shift2):
    pass
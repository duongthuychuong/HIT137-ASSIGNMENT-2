from logic import encrypt_text, decrypt_text


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def verify_files(original_file, decrypted_file):
    original = read_file(original_file)
    decrypted = read_file(decrypted_file)
    return original == decrypted


def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    text = read_file("raw_text.txt")

    encrypted, tags = encrypt_text(text, shift1, shift2)
    write_file("encrypted_text.txt", encrypted)
    write_file("tags.txt", tags)
    print("Encryption complete! Saved to encrypted_text.txt")

    decrypted = decrypt_text(encrypted, shift1, shift2, tags)
    write_file("decrypted_text.txt", decrypted)
    print("Decryption complete! Saved to decrypted_text.txt")

    if verify_files("raw_text.txt", "decrypted_text.txt"):
        print("Verification result: SUCCESS - Content matches perfectly!")
    else:
        print("Verification result: FAILED - Content does not match!")


if __name__ == "__main__":
    main()

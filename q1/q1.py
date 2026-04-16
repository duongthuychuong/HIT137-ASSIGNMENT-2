from logic import encrypt_text, decrypt_text


# This file handles reading/writing files and running the program


def read_file(filename):
    # Read text from file
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(filename, content):
    # Write text to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def verify_files(original_file, decrypted_file):
    # Compare original and decrypted content

    # NOTE:
    # This may fail even if logic is correct,
    # because the encryption method is not fully reversible
    original = read_file(original_file)
    decrypted = read_file(decrypted_file)
    return original == decrypted


def main():
    # Get shift values from user
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    # Read original text
    text = read_file("raw_text.txt")

    # Encrypt and save
    encrypted = encrypt_text(text, shift1, shift2)
    write_file("encrypted_text.txt", encrypted)
    print("Encryption complete!")

    # Decrypt and save
    decrypted = decrypt_text(encrypted, shift1, shift2)
    write_file("decrypted_text.txt", decrypted)
    print("Decryption complete!")

    # Check if decrypted text matches original
    if verify_files("raw_text.txt", "decrypted_text.txt"):
        print("SUCCESS - Content matches")
    else:
        print("FAILED - Content does not match")


if __name__ == "__main__":
    main()
from logic import encrypt_text, decrypt_text


def read_file(filename):
    pass


def write_file(filename, content):
    pass


def verify_files(original_file, decrypted_file):
    pass


def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    text = read_file("raw_text.txt")

    encrypted = encrypt_text(text, shift1, shift2)
    write_file("encrypted_text.txt", encrypted)

    decrypted = decrypt_text(encrypted, shift1, shift2)
    write_file("decrypted_text.txt", decrypted)

    if verify_files("raw_text.txt", "decrypted_text.txt"):
        print("SUCCESS")
    else:
        print("FAILED")


if __name__ == "__main__":
    main()
import secrets
import string
import time

NUM_ROUNDS = 20

def matrix(lst):
    return [[lst[i] for i in range(x, x + 16)] for x in range(0, 256, 16)]

def pad(str):
    if len(str) > 256:
        raise Exception("Plaintext length too long")
    if len(str) % 256 != 0:
        while len(str) % 256 != 0:
            str += "`"
    return str

def reverse_byte(byte):
    return byte[::-1]

def reverse_bits(byte):
    out = ""
    for i in byte:
        if i == "1":
            out += "0"
        elif i == "0":
            out += "1"
    return out

def encrypt():
    key = ""
    plain_text = input("Enter Plaintext: ")
    choice = input("Generate a key(0) or use your own(1): ")
    if choice == "0":
        key_choices = string.ascii_letters + string.digits + string.punctuation
        key = "".join([secrets.choice(key_choices) for _ in range(256)])
        print("Your key is:")
        print(key)
    elif choice == "1":
        key = input("Enter your 256 character (2048 bit) key: ")
    bitted_key = [format(ord(i), "08b") for i in key]
    matrix_key = matrix(bitted_key)
    plain_text = pad(plain_text)
    bitted_text = [format(ord(i), "08b") for i in plain_text]
    matrix_text = matrix(bitted_text)

    # combine orig key and orig text
    for i in range(16):
        for j in range(16):
            matrix_text[i][j] = format(int(matrix_text[i][j], 2) ^ int(matrix_key[i][j], 2), "08b")

    # round function
    for i in range(NUM_ROUNDS):
        # reversing each bit of each char
        for j in range(16):
            for e in range(16):
                matrix_text[j][e] = reverse_bits(matrix_text[j][e])

        # reversing bytes of each char
        for j in range(16):
            for e in range(16):
                matrix_text[j][e] = reverse_byte(matrix_text[j][e])

        # combine key
        for j in range(16):
            for e in range(16):
                matrix_text[j][e] = format(int(matrix_text[j][e], 2) ^ int(matrix_key[j][e], 2), "08b")

        time.sleep(0.1)

    ending = []
    for i in matrix_text:
        ending.append(' '.join(i))

    ending = ' '.join(ending)
    final_hex = ''.join([format(int(i, 2), "02x") for i in ending.split(" ")])
    print("Ciphertext:")
    print(final_hex)

def decrypt():
    cipher_text = input("Enter \"hexified\" ciphertext: ")
    key = input("Enter key: ")
    bytess = [cipher_text[i: i+2] for i in range(0, len(cipher_text), 2)]
    binary_bytes = [format(int(i, 16), "08b") for i in bytess]
    matrix_bytes = matrix(binary_bytes)
    bytes_key = [format(ord(i), "08b") for i in key]
    matrix_key = matrix(bytes_key)

    # inverse round function
    for i in range(NUM_ROUNDS):
        # combine key
        for j in range(16):
            for e in range(16):
                matrix_bytes[j][e] = format(int(matrix_bytes[j][e], 2) ^ int(matrix_key[j][e], 2), "08b")

        # reversing bytes
        for j in range(16):
            for e in range(16):
                matrix_bytes[j][e] = reverse_byte(matrix_bytes[j][e])

        # reversing bits
        for j in range(16):
            for e in range(16):
                matrix_bytes[j][e] = reverse_bits(matrix_bytes[j][e])

        time.sleep(0.1)

    # combine key
    for i in range(16):
        for j in range(16):
            matrix_bytes[i][j] = format(int(matrix_bytes[i][j], 2) ^ int(matrix_key[i][j], 2), "08b")

    ending = []
    for i in matrix_bytes:
        ending.append(' '.join(i))

    ending = ' '.join(ending)
    final_text = "".join([chr(int(i, 2)) for i in ending.split(" ")])

    final_text = final_text.replace("`", "")
    print("Plaintext:")
    print(final_text)



def main():
    a = input("Encrypt(0) or Decrypt(1): ")
    if a == "0":
        encrypt()
    elif a == "1":
        decrypt()

if __name__ == "__main__":
    main()


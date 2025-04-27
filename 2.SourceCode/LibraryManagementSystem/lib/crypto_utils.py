from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

key = "uitlib@2025rocks"

def encrypt_password(plaintext: str) -> str:
    key_bytes = key.encode('utf-8')
    if len(key_bytes) < 16:
        key_bytes = key_bytes.ljust(16, b'\0')
    elif len(key_bytes) > 16:
        key_bytes = key_bytes[:16]

    cipher = AES.new(key_bytes, AES.MODE_ECB)
    padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def decrypt_password(ciphertext_base64: str) -> str:
    key_bytes = key.encode('utf-8')
    if len(key_bytes) < 16:
        key_bytes = key_bytes.ljust(16, b'\0')
    elif len(key_bytes) > 16:
        key_bytes = key_bytes[:16]

    cipher = AES.new(key_bytes, AES.MODE_ECB)
    encrypted_bytes = base64.b64decode(ciphertext_base64)
    decrypted_padded = cipher.decrypt(encrypted_bytes)
    decrypted = unpad(decrypted_padded, AES.block_size)
    return decrypted.decode('utf-8')



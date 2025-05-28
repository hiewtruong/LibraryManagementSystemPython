from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64

key = "uitlib@2025rocks"

def encrypt_password(plaintext: str) -> str:
    # Chuẩn bị khóa
    key_bytes = key.encode('utf-8')
    if len(key_bytes) < 16:
        key_bytes = key_bytes.ljust(16, b'\0')
    elif len(key_bytes) > 16:
        key_bytes = key_bytes[:16]

    # Tạo cipher với AES-ECB
    cipher = Cipher(algorithms.AES(key_bytes), modes.ECB())
    encryptor = cipher.encryptor()

    # Padding dữ liệu
    padder = padding.PKCS7(128).padder()  # 128-bit cho AES
    padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()

    # Mã hóa
    encrypted_bytes = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def decrypt_password(ciphertext_base64: str) -> str:
    # Chuẩn bị khóa
    key_bytes = key.encode('utf-8')
    if len(key_bytes) < 16:
        key_bytes = key_bytes.ljust(16, b'\0')
    elif len(key_bytes) > 16:
        key_bytes = key_bytes[:16]

    # Tạo cipher với AES-ECB
    cipher = Cipher(algorithms.AES(key_bytes), modes.ECB())
    decryptor = cipher.decryptor()

    # Giải mã
    encrypted_bytes = base64.b64decode(ciphertext_base64)
    decrypted_padded = decryptor.update(encrypted_bytes) + decryptor.finalize()

    # Loại bỏ padding
    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
    return decrypted.decode('utf-8')
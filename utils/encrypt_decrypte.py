# from cryptography.fernet import Fernet
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.hazmat.primitives.asymmetric import ec
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.backends import default_backend
# import os
# import base64



# def kryptography(private_key : ec.EllipticCurvePrivateKey, public_key :ec.EllipticCurvePublicKey, message : str):
#     # تولید یک سولت تصادفی برای PBKDF2
#     salt = os.urandom(16)

#     message_bytes = message.encode('utf-8')

#     # تولید کلید مشترک بین فرستنده و گیرنده
#     shared_key = private_key.exchange(ec.ECDH(), public_key)

#     # تولید کلید تشکیل دهنده از PBKDF2 برای رمزنگاری
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA512(),
#         iterations=100000,
#         salt=salt,
#         length=32,
#         backend=default_backend()
#     )

#     key = base64.urlsafe_b64encode(kdf.derive(shared_key))
#     fernet = Fernet(key)

#     encrypted_message = fernet.encrypt(message_bytes)
#     print("encrypted message : " + encrypted_message.decode())

#     decrypted_message_bytes = fernet.decrypt(encrypted_message.decode())
#     decrypted_message = eval(decrypted_message_bytes.decode('utf-8'))
#     print(type(decrypted_message))
#     print(decrypted_message)



# from cryptography.hazmat.primitives.asymmetric import ec
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import padding
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.primitives.asymmetric import utils
# from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
# from cryptography.hazmat.primitives.asymmetric import ec
# import os
# import base64


# def encrypt_message(private_key, public_key, message):
#     shared_key = private_key.exchange(ec.ECDH(), public_key)
#     key = shared_key[:16]  # Use the first 16 bytes of the shared key

#     iv = os.urandom(16)
#     cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
#     encryptor = cipher.encryptor()
    
#     padder = padding.PKCS7(128).padder()
#     padded_data = padder.update(message.encode('utf-8'))
#     padded_data += padder.finalize()
    
#     encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
    
#     encrypted_message = iv + encrypted_message
#     # # تبدیل داده به متن با استفاده از Base64
#     # encrypted_message_text = base64.b64encode(encrypted_message).decode('utf-8')
#     return encrypted_message

# def decrypt_message(private_key, public_key, encrypted_message):
#     #     # تبدیل متن به داده باینری با استفاده از Base64
#     # encrypted_message = base64.b64decode(encrypted_message.encode('utf-8'))
    
#     shared_key = private_key.exchange(ec.ECDH(), public_key)
#     key = shared_key[:16]  # Use the first 16 bytes of the shared key

#     iv = encrypted_message[:16]
#     ciphertext = encrypted_message[16:]
#     cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
#     decryptor = cipher.decryptor()

#     decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
#     unpadder = padding.PKCS7(128).unpadder()
#     decrypted_data = unpadder.update(decrypted_padded_data)
#     decrypted_data += unpadder.finalize()
    
#     return decrypted_data.decode('utf-8')



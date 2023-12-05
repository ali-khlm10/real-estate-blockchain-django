from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import hashlib

# # تابع برای ایجاد آدرس کیف پول
# def generate_wallet_address(public_key: ec.EllipticCurvePublicKey):
#     address = public_key.public_bytes(
#         Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
#     return {
#         "address": str(address),
#         '0x_address': "0x"+str(address),
#     }


def generate_wallet_address(public_key: ec.EllipticCurvePublicKey):
    # تبدیل کلید عمومی به داده‌های بایتی و حذف PEM Header
    pub_key_bytes = public_key.public_bytes(
        Encoding.DER, PublicFormat.SubjectPublicKeyInfo)

    # ایجاد هش SHA-512 از کلید عمومی
    sha512 = hashlib.sha512()
    sha512.update(pub_key_bytes)
    sha512_digest = sha512.digest()

    # برداشتن 20 بایت آخر (یا هر قسمت دیگری که نیاز دارید) به عنوان آدرس کیف پول
    wallet_address = sha512_digest[-20:].hex()

    # اضافه کردن پیشوند '0x' به آدرس کیف پول
    return f'0x{wallet_address}'

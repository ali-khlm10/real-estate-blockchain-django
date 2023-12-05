from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat


# تابع برای ایجاد آدرس کیف پول
def generate_wallet_address(public_key: ec.EllipticCurvePublicKey):
    address = public_key.public_bytes(
        Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
    return {
        "address": address,
        '0x_address': "0x"+address,
    }

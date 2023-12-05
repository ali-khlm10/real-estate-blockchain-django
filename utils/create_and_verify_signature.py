from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


# تابع برای ایجاد امضای دیجیتال
def create_signature(private_key: ec.EllipticCurvePrivateKey, message: str):
    signature = private_key.sign(
        message.encode('utf-8'),
        ec.ECDSA(hashes.SHA256())
    )
    return {
        'signature_hex': signature.hex(),
        'signature': signature,
    }


# تابع برای تایید امضای دیجیتال
def verify_signature(public_key: ec.EllipticCurvePublicKey, signature, message: str):
    try:
        public_key.verify(
            signature,
            message.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature as error:
        print(f'new error : {error}')
        return False

# //////////////////////////////////////////////////////

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


pr = str('-----BEGIN PRIVATE KEY-----\nMIHuAgEAMBAGByqGSM49AgEGBSuBBAAjBIHWMIHTAgEBBEIBJBFTAIxyu4TY2aJE\nf6oq2X8O84k007uVHHIkuSwtBe7u9jqmVVJ8ly5x90wqQWe62aNnIaVPnseXLPue\noQ/9GIKhgYkDgYYABABlDjn9d0oAXLRtkwcrw7Rqk+fYRj68CcdmDA/+l5VrxHwJ\nFYBJhMSFjmRscnnC7vUMn9xpLzcgjvFxXkHSlQEukwGxU61KlE2pg5f57hywOGIy\n4/iyFqCJRSvgec1jlmWFHxUarjO6W0f3WCOXUjS51BG75sMntZT1so1/gFjqh2aJ\nDw==\n-----END PRIVATE KEY-----\n')
pu = str('-----BEGIN PUBLIC KEY-----\nMIGbMBAGByqGSM49AgEGBSuBBAAjA4GGAAQAZQ45/XdKAFy0bZMHK8O0apPn2EY+\nvAnHZgwP/peVa8R8CRWASYTEhY5kbHJ5wu71DJ/caS83II7xcV5B0pUBLpMBsVOt\nSpRNqYOX+e4csDhiMuP4shagiUUr4HnNY5ZlhR8VGq4zultH91gjl1I0udQRu+bD\nJ7WU9bKNf4BY6odmiQ8=\n-----END PUBLIC KEY-----\n')

from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

# بازیابی کلید خصوصی
private_key = load_pem_private_key(
    pr.encode(),
    password=None,
)


# بازیابی کلید عمومی
public_key = load_pem_public_key(
     pu.encode(),
)


# a =create_signature(private_key=private_key,message="hello")
# print(a)


s = b"0\x81\x88\x02B\x01].\xeb\xe2\xa9\x94(\xf6l\xb0U\xd4\x04\x0f\xfbM\xfd\xd5\x18jg\x93\xfc\xf4Ec\x8b\xbb\x95\t\xf4\x0f\x7f\xc7\xecESW_\x1b\x1d\x8d\xf7\xea,\x8c\x85\x0cji\x87\x8fC\xc9\xeb\x8cZ\xe9?>\xd9\xce\xf9b2\x02B\x00\xdc't\x8e\xb0\x04}7\xc0<\x9dp\x8bM?\xfc@\xab\xe4\xd5|\xce\x9b9[S \xc8_i( \xc4Q\xe8O3)\x19<\xc6\xc0\xdd\xdbZ\x86u\x8c\x99\x92\xc8\xd8\xf5\xef\x8b\x972\x1f\xcb\x81*\t\xfe\xa7k"
print(verify_signature(public_key=public_key,signature=s,message="hello"))
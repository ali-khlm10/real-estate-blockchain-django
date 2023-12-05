from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils



# create pair key with SECP521R1
def generate_pair_key():
    # تولید جفت کلید با SECP521R1
    private_key = ec.generate_private_key(ec.SECP521R1())
    public_key = private_key.public_key()

    # تبدیل کلید خصوصی به فرمت PEM
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # تبدیل کلید عمومی به فرمت PEM
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return {
        'private_key': private_key,
        'private_pem': private_pem,
        'public_key': public_key,
        'public_pem': public_pem,
    }




# ///////////////////////////////////////////////////////////////



keys = generate_pair_key()
private_key_pem = keys['private_pem']
public_key_pem = keys['public_pem']



from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

# بازیابی کلید خصوصی
private_key = load_pem_private_key(
    private_key_pem,
    password=None,
)

# بازیابی کلید عمومی
public_key = load_pem_public_key(
    public_key_pem,
)



print(private_key_pem)
print(public_key_pem)
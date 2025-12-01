from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import pathlib

pub = serialization.load_pem_public_key(pathlib.Path("compliance_public.pem").read_bytes())
data = pathlib.Path("CHECKSUMS.txt").read_bytes()
sig = base64.b64decode(open("SIGNATURE.txt").read().splitlines()[1])
pub.verify(sig, data, padding.PKCS1v15(), hashes.SHA256())
print("Signature OK")

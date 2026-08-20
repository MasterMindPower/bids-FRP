import os
import sys
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def execute_app():
    script_key_hex = os.environ.get("SCRIPT_KEY", "").strip()
    if not script_key_hex:
        sys.exit(1)

    enc_file = os.path.join(os.path.dirname(__file__), "app.enc")
    if not os.path.exists(enc_file):
        enc_file = "app.enc"

    with open(enc_file, "r", encoding="utf-8") as f:
        enc_b64 = f.read().strip()

    raw = base64.b64decode(enc_b64)
    iv = raw[:12]
    ciphertext = raw[12:]

    key = bytes.fromhex(script_key_hex)
    aesgcm = AESGCM(key)
    decrypted_code = aesgcm.decrypt(iv, ciphertext, None).decode("utf-8")

    exec(decrypted_code, globals())

if __name__ == "__main__":
    execute_app()

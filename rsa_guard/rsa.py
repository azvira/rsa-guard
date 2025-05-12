from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import base64


def generate_keys(secret_word: str) -> tuple[str, RSA.RsaKey]:
    key = RSA.generate(2048)

    enc_priv_key_b64 = key.export_key(
        passphrase=secret_word,  # пароль (секретное слово), которым будет зашифрован приватный ключ
        pkcs=8,  # формат контейнера для приватного ключа, который позволяет шифровать его.
        protection="scryptAndAES128-CBC"
    )
    public_key = key.publickey()

    enc_priv_key = base64.b64encode(enc_priv_key_b64).decode()

    return enc_priv_key, public_key


def encrypt_password(password: str, public_key: RSA.RsaKey) -> str:
    cipher = PKCS1_OAEP.new(public_key)
    encrypted = cipher.encrypt(password.encode())
    enc_password = base64.b64encode(encrypted).decode()
    return enc_password


def decrypt_password(enc_password: str, enc_priv_key: str, secret_word: str) -> str:
    try:
        enc_priv_key_b64 = base64.b64decode(enc_priv_key).decode()
        private_key = RSA.import_key(
            enc_priv_key_b64.encode(),
            passphrase=secret_word
        )
    except Exception as e:
        print("Ошибка при import_key:", str(e))
        raise e

    cipher = PKCS1_OAEP.new(private_key)
    password = cipher.decrypt(base64.b64decode(enc_password)).decode()
    return password


    
    






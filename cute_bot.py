#!/usr/bin/env python3

"""A local demonstration of X25519 key agreement and AES-GCM messages."""

import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def derive_ciphers() -> tuple[AESGCM, AESGCM]:
    """Simulate two participants agreeing on a key in this process."""
    sender = x25519.X25519PrivateKey.generate()
    receiver = x25519.X25519PrivateKey.generate()

    def derive(secret: bytes) -> AESGCM:
        key = HKDF(
            algorithm=hashes.SHA256(), length=32, salt=None, info=b"purrbot-demo"
        ).derive(secret)
        return AESGCM(key)

    return (
        derive(sender.exchange(receiver.public_key())),
        derive(receiver.exchange(sender.public_key())),
    )


def encrypt_message(cipher: AESGCM, message: str) -> str:
    """Encode nonce and authenticated ciphertext as one portable hex string."""
    nonce = os.urandom(12)
    return (nonce + cipher.encrypt(nonce, message.encode("utf-8"), None)).hex()


def decrypt_message(cipher: AESGCM, packet: str) -> str:
    data = bytes.fromhex(packet)
    if len(data) < 28:  # 12-byte nonce plus at least a 16-byte GCM tag
        raise ValueError("Encrypted message is too short")
    return cipher.decrypt(data[:12], data[12:], None).decode("utf-8")


def main() -> None:
    print("Meet PurrBot!")
    print(r"""     /\_/\
    ( o.o )
     > ^ <""")
    try:
        name = input("What's your name? ")
    except EOFError:
        print("\nGoodbye!")
        return

    sender, receiver = derive_ciphers()
    print(f"Local encryption demo ready, {name}!")
    print("Both simulated participants run here; no server or remote chat is involved.")

    while True:
        try:
            message = input("Type a message to encrypt (or 'exit' to quit): ")
        except EOFError:
            break
        if message.lower() == "exit":
            break
        packet = encrypt_message(sender, message)
        print("Encrypted packet (nonce + ciphertext + tag):", packet)
        print("Decrypted locally:", decrypt_message(receiver, packet))
    print("Goodbye!")


if __name__ == "__main__":
    main()

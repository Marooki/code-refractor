#!/usr/bin/env python3

"""Cute encrypted chat bot."""

from __future__ import annotations

import os
import time
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derive_shared_key() -> AESGCM:
    """Derive a shared AESGCM key using X25519."""
    user_private = x25519.X25519PrivateKey.generate()
    server_private = x25519.X25519PrivateKey.generate()
    shared_secret = user_private.exchange(server_private.public_key())

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"purrbot",
    )
    key = hkdf.derive(shared_secret)
    return AESGCM(key)


def main() -> None:
    cute_character = r"""
     /\_/\
    ( o.o )
     > ^ <
    """
    print("Meet PurrBot!")
    print(cute_character)

    name = input("What's your name? ")
    age = input("How old are you? ")
    country = input("Which country would you like to connect to? ")
    print(
        f"Scanning for nearby servers in {country} for end-to-end encrypted communication..."
    )
    for i in range(3):
        print("Scanning" + "." * (i + 1))
        time.sleep(1)

    cipher = derive_shared_key()
    print("Secure channel ready!")

    while True:
        message = input("Type a message to encrypt (or 'exit' to quit): ")
        if message.lower() == "exit":
            break
        nonce = os.urandom(12)
        encrypted = cipher.encrypt(nonce, message.encode(), None)
        print("Encrypted:", encrypted.hex())
        decrypted = cipher.decrypt(nonce, encrypted, None)
        print("Decrypted on the other side:", decrypted.decode())
    print("Goodbye!")


if __name__ == "__main__":
    main()

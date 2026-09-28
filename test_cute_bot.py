"""Run with: python -m unittest -v"""

import unittest

from cryptography.exceptions import InvalidTag

from cute_bot import decrypt_message, derive_ciphers, encrypt_message


class EncryptionTests(unittest.TestCase):
    def test_round_trip_and_fresh_nonces(self):
        sender, receiver = derive_ciphers()
        message = "Hello, مرحبا 🐈"
        first = encrypt_message(sender, message)
        second = encrypt_message(sender, message)
        self.assertNotEqual(first[:24], second[:24])
        self.assertEqual(decrypt_message(receiver, first), message)
        self.assertEqual(decrypt_message(receiver, second), message)

    def test_modified_ciphertext_is_rejected(self):
        sender, receiver = derive_ciphers()
        packet = bytearray.fromhex(encrypt_message(sender, "hello"))
        packet[-1] ^= 1
        with self.assertRaises(InvalidTag):
            decrypt_message(receiver, packet.hex())

    def test_truncated_packet_is_rejected(self):
        _, receiver = derive_ciphers()
        with self.assertRaises(ValueError):
            decrypt_message(receiver, "00" * 27)


if __name__ == "__main__":
    unittest.main()

# PurrBot local encryption demo

PurrBot demonstrates X25519 key agreement, HKDF-SHA256, and AES-GCM in a single Python process. It simulates two participants, encrypts each message, and decrypts it locally. It does not scan for servers, connect to anyone, or provide end-to-end chat.

Requires Python 3.10 or later. To make a test environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest -v
python cute_bot.py
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` (or run `.venv\Scripts\python.exe` directly for each command). Enter a name and messages; type `exit` or send EOF to finish. The printed hex packet combines a fresh 12-byte nonce and authenticated ciphertext, including the GCM tag. The packet can be passed to `decrypt_message` with the matching cipher during the current run; keys are not persisted.

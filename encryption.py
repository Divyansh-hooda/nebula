import os
import threading
from dataclasses import dataclass
from typing import Callable, Optional

from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes
)

from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.kdf.pbkdf2 import (
    PBKDF2HMAC
)

from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives import padding
@dataclass
class EncryptionResult:

    source: str

    destination: str

    success: bool

    message: str
class EncryptionManager:

    def __init__(self):

        self.running = False

        self.cancelled = False

        self.thread = None

        self.on_progress: Optional[
            Callable[[int], None]
        ] = None

        self.on_finish: Optional[
            Callable[[EncryptionResult], None]
        ] = None

        self.chunk_size = 64 * 1024
    def cancel(self):

        self.cancelled = True

    def reset(self):

        self.cancelled = False

    def is_running(self):

        return self.running
    def derive_key(
        self,
        password,
        salt
    ):

        kdf = PBKDF2HMAC(

            algorithm=hashes.SHA256(),

            length=32,

            salt=salt,

            iterations=390000,

            backend=default_backend()

        )

        return kdf.derive(
            password.encode()
        )
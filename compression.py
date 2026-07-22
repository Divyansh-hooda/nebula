import os
import zipfile
import threading
from pathlib import Path
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class CompressionResult:
    source: str
    destination: str
    success: bool
    message: str


class CompressionManager:

    def __init__(self):

        self.cancelled = False

        self.running = False

        self.thread = None

        self.on_progress: Optional[Callable[[str], None]] = None

        self.on_finish: Optional[
            Callable[[CompressionResult], None]
        ] = None


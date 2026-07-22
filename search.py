import os
import threading
import queue
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional


@dataclass
class SearchResult:
    name: str
    path: str
    is_dir: bool
    size: int
    extension: str


class SearchEngine:
    def __init__(self):
        self._thread = None
        self._cancel = threading.Event()
        self._queue = queue.Queue()

        self.running = False

        self.on_result: Optional[Callable[[SearchResult], None]] = None
        self.on_progr
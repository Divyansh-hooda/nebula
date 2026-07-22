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
        self.on_progress: Optional[Callable[[str], None]] = None
        self.on_finish: Optional[Callable[[], None]] = None

    def is_running(self):
        return self.running

    def stop(self):
        self._cancel.set()

    def start(
        self,
        root,
        keyword,
        recursive=True,
        extensions=None,
        min_size=None,
        max_size=None
    ):
        if self.running:
            return False

        self._cancel.clear()

        self.running = True

        self._thread = threading.Thread(
            target=self._worker,
            args=(
                root,
                keyword,
                recursive,
                extensions,
                min_size,
                max_size
            ),
            daemon=True
        )

        self._thread.start()

        return True
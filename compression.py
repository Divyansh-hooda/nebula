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
    def is_running(self):
        return self.running
    def cancel(self):
        self.cancelled = True
    def reset(self):
        self.cancelled = False
    def compress(
        self,
        source,
        destination
    ):
        if self.running:
            return False
        self.reset()
        self.thread = threading.Thread(
            target=self._compress_worker,
            args=(
                source,
                destination
            ),
            daemon=True
        )
        self.running = True
        self.thread.start()
        return True
    def wait(self):
        if self.thread:
            self.thread.join()
    def _compress_worker(
        self,
        source,
        destination
    ):
        try:
            source = os.path.abspath(source)
            destination = os.path.abspath(destination)
            if os.path.isdir(source):
                self._compress_directory(
                    source,
                    destination
                )
            else:
                self._compress_file(
                    source,
                    destination
                )
            result = CompressionResult(
                source=source,
                destination=destination,
                success=True,
                message="Compression completed successfully."
            )
        except Exception as e:
            result = CompressionResult(
                source=source,
                destination=destination,
                success=False,
                message=str(e)
            )
        self.running = False
        if self.on_finish:
            self.on_finish(result)
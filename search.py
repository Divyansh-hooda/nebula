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
    def _worker(
        self,
        root,
        keyword,
        recursive,
        extensions,
        min_size,
        max_size
    ):
        keyword = keyword.lower()

        if extensions:
            extensions = {
                ext.lower().strip()
                for ext in extensions
            }

        try:
            if recursive:
                iterator = os.walk(root)
            else:
                iterator = [(root, [], os.listdir(root))]

            for current, _, files in iterator:

                if self._cancel.is_set():
                    break

                if self.on_progress:
                    self.on_progress(current)

                for filename in files:

                    if self._cancel.is_set():
                        break

                    full = os.path.join(current, filename)

                    self._process_file(
                        full,
                        filename,
                        keyword,
                        extensions,
                        min_size,
                        max_size
                    )

        except Exception:
            pass

        self.running = False

        if self.on_finish:
            self.on_finish()
    def _process_file(
        self,
        full_path,
        filename,
        keyword,
        extensions,
        min_size,
        max_size
    ):

        if keyword and keyword not in filename.lower():
            return

        try:
            is_dir = os.path.isdir(full_path)

            if is_dir:
                size = 0
            else:
                size = os.path.getsize(full_path)

        except Exception:
            return

        extension = Path(full_path).suffix.lower()

        if extensions:

            if extension not in extensions:
                return

        if min_size is not None:

            if size < min_size:
                return

        if max_size is not None:

            if size > max_size:
                return

        result = SearchResult(
            name=filename,
            path=full_path,
            is_dir=is_dir,
            size=size,
            extension=extension
        )

        self._queue.put(result)

        if self.on_result:
            self.on_result(result)
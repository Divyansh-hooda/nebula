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
    def _compress_file(
        self,
        source,
        destination
    ):
        with zipfile.ZipFile(
            destination,
            "w",
            zipfile.ZIP_DEFLATED
        ) as archive:
            if self.cancelled:
                return
            if self.on_progress:
                self.on_progress(
                    os.path.basename(source)
                )
            archive.write(
                source,
                arcname=os.path.basename(source)
            )
    def _compress_directory(
        self,
        source,
        destination
    ):
        with zipfile.ZipFile(
            destination,
            "w",
            zipfile.ZIP_DEFLATED
        ) as archive:
            for root, dirs, files in os.walk(source):
                if self.cancelled:
                    return
                for file in files:
                    if self.cancelled:
                        return
                    full = os.path.join(
                        root,
                        file
                    )
                    relative = os.path.relpath(
                        full,
                        source
                    )
                    if self.on_progress:
                        self.on_progress(
                            relative
                        )
                    archive.write(
                        full,
                        arcname=relative
                    )
    def extract(
        self,
        archive,
        destination
    ):
        if self.running:
            return False
        self.reset()
        self.thread = threading.Thread(
            target=self._extract_worker,
            args=(
                archive,
                destination
            ),
            daemon=True
        )
        self.running = True
        self.thread.start()
        return True
    def _extract_worker(
        self,
        archive,
        destination
    ):
        try:
            with zipfile.ZipFile(
                archive,
                "r"
            ) as zip_file:
                members = zip_file.infolist()
                for member in members:
                    if self.cancelled:
                        break
                    if self.on_progress:
                        self.on_progress(
                            member.filename
                        )
                    zip_file.extract(
                        member,
                        destination
                    )
            result = CompressionResult(
                source=archive,
                destination=destination,
                success=True,
                message="Extraction completed successfully."
            )
        except Exception as e:
            result = CompressionResult(
                source=archive,
                destination=destination,
                success=False,
                message=str(e)
            )
        self.running = False
        if self.on_finish:
            self.on_finish(result)
    @staticmethod
    def is_zip(path):

        return zipfile.is_zipfile(path)

    @staticmethod
    def list_files(path):

        with zipfile.ZipFile(
            path,
            "r"
        ) as archive:

            return archive.namelist()

    @staticmethod
    def archive_size(path):

        return os.path.getsize(path)

    @staticmethod
    def file_count(path):

        with zipfile.ZipFile(
            path,
            "r"
        ) as archive:

            return len(
                archive.infolist()
            )

    @staticmethod
    def compressed_size(path):

        total = 0

        with zipfile.ZipFile(
            path,
            "r"
        ) as archive:

            for info in archive.infolist():

                total += info.compress_size

        return total

    @staticmethod
    def original_size(path):

        total = 0

        with zipfile.ZipFile(
            path,
            "r"
        ) as archive:

            for info in archive.infolist():

                total += info.file_size

        return total

    @staticmethod
    def compression_ratio(path):

        original = CompressionManager.original_size(path)

        compressed = CompressionManager.compressed_size(path)

        if original == 0:
            return 0.0

        return round(
            (1 - compressed / original) * 100,
            2
        )
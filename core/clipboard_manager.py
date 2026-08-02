import os
from posixpath import splitext
import shutil

class ClipboardManager:
    def __init__(self):
        self.clipboard = None
        self.operation = None

    def copy(self, path):
        self.clipboard = path
        self.operation = "copy"

    def cut(self, path):
        self.clipboard = path
        self.operation = "cut"

    def clear(self):
        self.clipboard = None
        self.operation = None

    def has_item(self):
        return self.clipboard is not None
    
    def paste(self, destination):
        if not self.has_item():
            return False, "Clipboard Empty"
        src = self.clipboard
        if not os.path.exists(src):
            self.clear()
            return False, "source does not exist"
        name = os.path.basename(src)
        dst = os.path.join(destination, name)
        if os.path.exists(dst):
            base, ext = os.path,splitext(name)
            count = 1
            while os.path.exists(dst):
                dst = os.path.join(destination, f"{base}_{count}{ext}")
                count += 1
        try:

            if self.operation == "copy":

                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

            else:

                shutil.move(src, dst)

            if self.operation == "cut":
                self.clear()

            return True, dst

        except Exception as e:

            return False, str(e)
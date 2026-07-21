import os
import shutil
import time

def bytes_to_size(size):
    power = 1024
    n = 0
    labels=["B", "KB", "MB", "GB", "TB"]
    while size>power:
        size/=power
        n+=1
    return f"{round(size,2)} {labels[n]}"

def folder_size(folder):
    total = 0
    for root,dirs,files in os.walk(folder):
        for file in files:
            fp = os.path.join(root,file)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total


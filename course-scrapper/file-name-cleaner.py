import os
import re
from urllib.parse import unquote

DOWNLOAD_DIR = "downloads"

for old_name in os.listdir(DOWNLOAD_DIR):

    new_name = unquote(old_name)

    # Remove special characters except . _ -
    stem, ext = os.path.splitext(new_name)
    stem = re.sub(r'[^A-Za-z0-9._ -]', '', stem)
    stem = re.sub(r'\s+', ' ', stem).strip()

    new_name = stem + ext

    if old_name != new_name:
        old_path = os.path.join(DOWNLOAD_DIR, old_name)
        new_path = os.path.join(DOWNLOAD_DIR, new_name)

        if not os.path.exists(new_path):
            os.rename(old_path, new_path)
            print(f"{old_name} -> {new_name}")

print("Done")
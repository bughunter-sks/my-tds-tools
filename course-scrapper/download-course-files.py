from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import os
from pathlib import Path

BASE_URL = "https://courses.grainger.illinois.edu/cs543/sp2017/"
DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

session = requests.Session()

# --------------------------------------------------
# Step 1: Collect files
# --------------------------------------------------
html = session.get(BASE_URL, timeout=30).text
soup = BeautifulSoup(html, "lxml")

files = []

for a in soup.find_all("a", href=True):
    href = a["href"]

    if href.lower().endswith((".ppt", ".pptx", ".pdf")):
        file_url = urljoin(BASE_URL, href)
        filename = file_url.split("/")[-1]

        size = 0

        try:
            head = session.head(file_url, allow_redirects=True, timeout=30)
            size = int(head.headers.get("Content-Length", 0))
        except Exception:
            pass

        files.append({
            "url": file_url,
            "filename": filename,
            "size": size
        })

# --------------------------------------------------
# Step 2: Sort small -> large
# --------------------------------------------------
files.sort(key=lambda x: x["size"] if x["size"] > 0 else float("inf"))

print(f"\nTotal files found: {len(files)}\n")

# --------------------------------------------------
# Step 3: Status overview
# --------------------------------------------------
print("Files discovered:")
for idx, f in enumerate(files, 1):
    mb = f["size"] / (1024 * 1024)
    print(
        f"{idx:3d}. "
        f"{f['filename']:<50} "
        f"{mb:8.2f} MB "
        f"[PENDING]"
    )

print("\nStarting downloads...\n")

# --------------------------------------------------
# Step 4: Download (resume supported)
# --------------------------------------------------
for idx, f in enumerate(files, 1):

    url = f["url"]
    filename = f["filename"]
    total_size = f["size"]

    filepath = Path(DOWNLOAD_DIR) / filename

    existing_size = filepath.stat().st_size if filepath.exists() else 0

    # Already complete
    if total_size > 0 and existing_size >= total_size:
        print(
            f"[{idx}/{len(files)}] "
            f"SKIPPED   {filename} "
            f"({existing_size/(1024*1024):.2f} MB)"
        )
        continue

    headers = {}

    if existing_size > 0:
        headers["Range"] = f"bytes={existing_size}-"
        print(
            f"[{idx}/{len(files)}] "
            f"RESUMING  {filename} "
            f"({existing_size/(1024*1024):.2f} MB downloaded)"
        )
    else:
        print(
            f"[{idx}/{len(files)}] "
            f"DOWNLOADING {filename}"
        )

    try:
        r = session.get(
            url,
            headers=headers,
            stream=True,
            timeout=60
        )
        r.raise_for_status()

        mode = "ab" if existing_size > 0 else "wb"

        with open(filepath, mode) as fp:
            downloaded = existing_size

            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue

                fp.write(chunk)
                downloaded += len(chunk)

                if total_size > 0:
                    pct = downloaded * 100 / total_size
                    print(
                        f"\r    {pct:6.2f}% "
                        f"({downloaded/(1024*1024):.2f}/"
                        f"{total_size/(1024*1024):.2f} MB)",
                        end=""
                    )

        print("\n    COMPLETED")

    except Exception as e:
        print(f"\n    FAILED: {e}")

# --------------------------------------------------
# Step 5: Final summary
# --------------------------------------------------
print("\n" + "=" * 100)
print("DOWNLOAD SUMMARY")
print("=" * 100)

completed = 0

for f in files:

    filepath = Path(DOWNLOAD_DIR) / f["filename"]

    downloaded = filepath.stat().st_size if filepath.exists() else 0
    total = f["size"]

    if total > 0 and downloaded >= total:
        status = "COMPLETED"
        completed += 1
    elif downloaded > 0:
        status = "PARTIAL"
    else:
        status = "NOT DOWNLOADED"

    print(
        f"{f['filename']:<50} "
        f"{downloaded/(1024*1024):8.2f} MB / "
        f"{total/(1024*1024):8.2f} MB "
        f"{status}"
    )

print("\nCompleted:", completed, "/", len(files))
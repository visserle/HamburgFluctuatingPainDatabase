#!/usr/bin/env python3
"""Download the Hamburg Fluctuating Pain DuckDB database from Figshare."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

ARTICLE_ID = 32112442
ARTICLE_URL = f"https://api.figshare.com/v2/articles/{ARTICLE_ID}"
DATABASE_NAME = "pain-measurement.duckdb"
ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / DATABASE_NAME
CHUNK_SIZE = 1024 * 1024
PROGRESS_BAR_WIDTH = 32


def build_request(url: str) -> urllib.request.Request:
    return urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "HamburgFluctuatingPainDatabase downloader",
        },
    )


def fetch_article_metadata(timeout: float) -> dict:
    with urllib.request.urlopen(
        build_request(ARTICLE_URL), timeout=timeout
    ) as response:
        return json.load(response)


def select_database_file(metadata: dict) -> dict:
    for file_info in metadata.get("files", []):
        if file_info.get("name") == DATABASE_NAME:
            return file_info

    raise RuntimeError(
        f"Could not find {DATABASE_NAME!r} in Figshare article {ARTICLE_ID}."
    )


def compute_md5(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def format_size(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(num_bytes)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} {unit}"
        value /= 1024
    return f"{num_bytes} B"


def print_metadata(metadata: dict, file_info: dict) -> None:
    checksum = file_info.get("supplied_md5") or "unknown"
    print(f"Figshare article: {metadata['title']} ({metadata['doi']})")
    print(f"Database file: {file_info['name']}")
    print(f"Destination: {OUTPUT}")
    print(f"Size: {format_size(file_info['size'])}")
    print(f"MD5: {checksum}")
    print(f"Source: {file_info['download_url']}")


def verify_existing_file(expected_md5: str | None) -> bool:
    if not OUTPUT.exists():
        return False
    if expected_md5 is None:
        return True
    return compute_md5(OUTPUT) == expected_md5


def render_progress(bytes_downloaded: int, total_size: int) -> str:
    if total_size <= 0:
        return f"\rDownloaded {format_size(bytes_downloaded)}"

    ratio = min(bytes_downloaded / total_size, 1.0)
    filled = int(PROGRESS_BAR_WIDTH * ratio)
    bar = "#" * filled + "-" * (PROGRESS_BAR_WIDTH - filled)
    return (
        f"\r[{bar}] {ratio * 100:5.1f}% "
        f"{format_size(bytes_downloaded)} / {format_size(total_size)}"
    )


def download_file(url: str, destination: Path, timeout: float) -> None:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "HamburgFluctuatingPainDatabase downloader"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        total_size = int(response.headers.get("Content-Length", "0"))
        bytes_downloaded = 0
        last_reported = 0.0

        with destination.open("wb") as handle:
            while True:
                chunk = response.read(CHUNK_SIZE)
                if not chunk:
                    break

                handle.write(chunk)
                bytes_downloaded += len(chunk)

                now = time.monotonic()
                if now - last_reported >= 0.2:
                    print(
                        render_progress(bytes_downloaded, total_size),
                        file=sys.stderr,
                        end="",
                        flush=True,
                    )
                    last_reported = now

        print(
            render_progress(bytes_downloaded, total_size),
            file=sys.stderr,
            flush=True,
        )

        if total_size > 0 and bytes_downloaded != total_size:
            raise RuntimeError(
                f"Download incomplete: expected {total_size} bytes, got {bytes_downloaded}."
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download the DuckDB database from the Hamburg Fluctuating Pain "
            "Database Figshare record into the repository root."
        )
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the local database file if it already exists.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="Network timeout in seconds for each HTTP request (default: 60).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        metadata = fetch_article_metadata(timeout=args.timeout)
        file_info = select_database_file(metadata)
    except urllib.error.URLError as exc:
        print(f"Failed to resolve the Figshare record: {exc}", file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    expected_md5 = file_info.get("supplied_md5")

    if OUTPUT.exists():
        if not args.force and verify_existing_file(expected_md5):
            print(f"Database already present and verified at {OUTPUT}.")
            return 0
        if not args.force:
            print(
                f"{OUTPUT} already exists but was not replaced. Use --force to overwrite it.",
                file=sys.stderr,
            )
            return 1

    temp_file: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=f".{OUTPUT.name}.",
            suffix=".part",
            dir=OUTPUT.parent,
            delete=False,
        ) as handle:
            temp_file = Path(handle.name)

        print_metadata(metadata, file_info)
        download_file(file_info["download_url"], temp_file, timeout=args.timeout)

        if expected_md5 is not None:
            print("Verifying checksum...", file=sys.stderr)
            actual_md5 = compute_md5(temp_file)
            if actual_md5 != expected_md5:
                raise RuntimeError(
                    "Checksum mismatch after download: "
                    f"expected {expected_md5}, got {actual_md5}."
                )

        temp_file.replace(OUTPUT)
        print(f"Database downloaded successfully to {OUTPUT}.")
        return 0
    except KeyboardInterrupt:
        print("\nDownload interrupted.", file=sys.stderr)
        return 130
    except (RuntimeError, urllib.error.URLError) as exc:
        print(f"Download failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if temp_file is not None and temp_file.exists():
            temp_file.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
PyTools v2.0.0 - Downloads Module
YouTube video/audio download and file download utilities
"""

import os
import sys
import re
from typing import Optional, Dict, List, Any
from pathlib import Path

from core.base import BaseModule, SystemInfo, format_bytes, ensure_directory
from core.utils import get_logger, get_config
from ui.display import Display


class YouTubeDownloadModule(BaseModule):
    """Download YouTube videos and audio"""

    def __init__(self, display: Display):
        super().__init__(
            name="YouTube Downloader",
            description="Download YouTube videos or audio (MP3)",
            category="downloads",
        )
        self.display = display
        self.config = get_config()
        self.icon = "📺"

    def execute(self) -> bool:
        try:
            # Check for yt-dlp or pytube
            has_ytdlp = self._check_ytdlp()
            has_pytube = self._check_pytube()

            if not has_ytdlp and not has_pytube:
                self.display.show_error("No YouTube download library available")
                self.display.console.print()
                self.display.show_info("Install one of the following:")
                self.display.console.print(
                    "  • yt-dlp (recommended): pip install yt-dlp"
                )
                self.display.console.print("  • pytube: pip install pytube")
                return False

            url = self.display.prompt("Enter YouTube URL")
            if not url:
                self.display.show_warning("No URL provided")
                return False

            self.display.console.print()
            self.display.console.print("1. Download Video (MP4)")
            self.display.console.print("2. Download Audio (MP3)")
            self.display.console.print()

            choice = self.display.prompt("Choose option", default="1")

            if choice not in ["1", "2"]:
                self.display.show_warning("Invalid choice")
                return False

            download_type = "video" if choice == "1" else "audio"

            self.display.console.print()

            if has_ytdlp:
                return self._download_with_ytdlp(url, download_type)
            else:
                return self._download_with_pytube(url, download_type)

        except Exception as e:
            self.log_error("YouTube download failed", e)
            self.display.show_error(f"Download failed: {str(e)}")
            return False

    def _check_ytdlp(self) -> bool:
        """Check if yt-dlp is available"""
        try:
            import yt_dlp

            return True
        except ImportError:
            return False

    def _check_pytube(self) -> bool:
        """Check if pytube is available"""
        try:
            from pytube import YouTube

            return True
        except ImportError:
            return False

    def _download_with_ytdlp(self, url: str, download_type: str) -> bool:
        """Download using yt-dlp"""
        import yt_dlp

        # Get download directory
        if download_type == "video":
            output_dir = self.config.get("downloads.video_path", "VideosDownloads")
        else:
            output_dir = self.config.get("downloads.audio_path", "AudiosDownloads")

        ensure_directory(output_dir)

        # Configure yt-dlp options
        ydl_opts = {
            "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
            "progress_hooks": [self._progress_hook],
        }

        if download_type == "audio":
            ydl_opts["format"] = "bestaudio/best"
            ydl_opts["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]
        else:
            ydl_opts["format"] = "best[ext=mp4]/best"

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.display.show_info("Downloading...")
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "Unknown")

                self.display.console.print()
                self.display.show_success(f"Downloaded: {title}")
                self.display.show_info(f"Saved to: {output_dir}")

            return True

        except Exception as e:
            self.display.show_error(f"yt-dlp download failed: {str(e)}")
            return False

    def _download_with_pytube(self, url: str, download_type: str) -> bool:
        """Download using pytube"""
        from pytube import YouTube
        import requests
        from tqdm import tqdm

        try:
            yt = YouTube(url)

            self.display.show_info(f"Title: {yt.title}")
            self.display.show_info(f"Duration: {yt.length // 60}m {yt.length % 60}s")
            self.display.console.print()

            # Get download directory
            if download_type == "video":
                output_dir = self.config.get("downloads.video_path", "VideosDownloads")
                stream = yt.streams.filter(
                    progressive=True, file_extension="mp4"
                ).first()
                ext = "mp4"
            else:
                output_dir = self.config.get("downloads.audio_path", "AudiosDownloads")
                stream = yt.streams.filter(only_audio=True).first()
                ext = "mp3"

            ensure_directory(output_dir)

            if not stream:
                self.display.show_error("No suitable stream found")
                return False

            # Clean filename
            filename = re.sub(r'[<>:"/\\|?*]', "_", yt.title)
            filepath = os.path.join(output_dir, f"{filename}.{ext}")

            self.display.show_info("Downloading...")

            # Download with progress bar
            response = requests.get(stream.url, stream=True)
            total_size = int(response.headers.get("content-length", 0))

            with open(filepath, "wb") as f:
                with tqdm(
                    total=total_size, unit="B", unit_scale=True, unit_divisor=1024
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))

            self.display.console.print()
            self.display.show_success(f"Downloaded: {yt.title}")
            self.display.show_info(f"Saved to: {filepath}")

            return True

        except Exception as e:
            self.display.show_error(f"pytube download failed: {str(e)}")
            return False

    def _progress_hook(self, d):
        """Progress hook for yt-dlp"""
        if d["status"] == "downloading":
            pass  # Could add progress bar here


class FileDownloaderModule(BaseModule):
    """Download files from URL"""

    def __init__(self, display: Display):
        super().__init__(
            name="File Downloader",
            description="Download files from direct URLs",
            category="downloads",
        )
        self.display = display
        self.config = get_config()
        self.icon = "⬇️"

    def execute(self) -> bool:
        try:
            import requests
            from tqdm import tqdm

            url = self.display.prompt("Enter file URL")
            if not url:
                self.display.show_warning("No URL provided")
                return False

            # Get filename from URL or user
            filename = os.path.basename(url.split("?")[0])
            custom_filename = self.display.prompt(
                f"Save as (default: {filename})", default=filename
            )

            if custom_filename:
                filename = custom_filename

            # Get output directory
            output_dir = self.config.get("downloads.general_path", "Downloads")
            ensure_directory(output_dir)
            filepath = os.path.join(output_dir, filename)

            self.display.console.print()
            self.display.show_info(f"Downloading to: {filepath}")

            # Download with progress bar
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))

            with open(filepath, "wb") as f:
                if total_size > 0:
                    with tqdm(
                        total=total_size, unit="B", unit_scale=True, unit_divisor=1024
                    ) as pbar:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
                else:
                    # No content-length header
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            self.display.console.print()
            file_size = os.path.getsize(filepath)
            self.display.show_success(
                f"Downloaded: {filename} ({format_bytes(file_size)})"
            )
            self.display.show_info(f"Saved to: {filepath}")

            return True

        except requests.exceptions.RequestException as e:
            self.display.show_error(f"Download failed: {str(e)}")
            return False
        except Exception as e:
            self.log_error("File download failed", e)
            self.display.show_error(f"Download failed: {str(e)}")
            return False


class BatchDownloaderModule(BaseModule):
    """Batch download multiple files"""

    def __init__(self, display: Display):
        super().__init__(
            name="Batch Downloader",
            description="Download multiple files from a list of URLs",
            category="downloads",
        )
        self.display = display
        self.config = get_config()
        self.icon = "📦"

    def execute(self) -> bool:
        try:
            import requests
            from tqdm import tqdm

            self.display.show_info("Enter URLs (one per line, empty line to finish):")
            self.display.console.print()

            urls = []
            while True:
                url = input("URL: ").strip()
                if not url:
                    break
                urls.append(url)

            if not urls:
                self.display.show_warning("No URLs provided")
                return False

            self.display.console.print()
            self.display.show_info(f"Downloading {len(urls)} file(s)...")

            # Get output directory
            output_dir = self.config.get("downloads.general_path", "Downloads")
            ensure_directory(output_dir)

            successful = 0
            failed = 0

            for i, url in enumerate(urls, 1):
                try:
                    filename = os.path.basename(url.split("?")[0]) or f"file_{i}"
                    filepath = os.path.join(output_dir, filename)

                    self.display.console.print()
                    self.display.show_info(f"[{i}/{len(urls)}] Downloading: {filename}")

                    response = requests.get(url, stream=True, timeout=30)
                    response.raise_for_status()

                    total_size = int(response.headers.get("content-length", 0))

                    with open(filepath, "wb") as f:
                        if total_size > 0:
                            with tqdm(
                                total=total_size, unit="B", unit_scale=True
                            ) as pbar:
                                for chunk in response.iter_content(chunk_size=8192):
                                    if chunk:
                                        f.write(chunk)
                                        pbar.update(len(chunk))
                        else:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)

                    successful += 1
                    self.display.show_success(f"✓ {filename}")

                except Exception as e:
                    failed += 1
                    self.display.show_error(f"✗ Failed: {str(e)}")

            self.display.console.print()
            self.display.show_info(
                f"Completed: {successful} successful, {failed} failed"
            )

            return successful > 0

        except Exception as e:
            self.log_error("Batch download failed", e)
            self.display.show_error(f"Batch download failed: {str(e)}")
            return False


def get_download_modules(display: Display) -> List[BaseModule]:
    """Get all download modules"""
    return [
        YouTubeDownloadModule(display),
        FileDownloaderModule(display),
        BatchDownloaderModule(display),
    ]

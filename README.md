# 🚀 Media & Music Automation Suite 🎶📸

A professional automation toolkit designed to organize your digital life. This suite includes advanced Python scripts for sorting **iPhone Media** and managing **YouTube Music Playlists**.

---

## 🎵 Module 1: YT Music Organizer
Tired of messy playlists? This module helps you sort your library with surgical precision.

### ✨ Features
* **Smart Artist Sorting**: Automatically re-orders any playlist alphabetically by **Artist Name**.
* **Year-Based Filtering**: Split main playlists into categories like "Old" and "New" based on a specific year (e.g., *Trap Vechi* vs *Trap Nou*).
* **Anti-Conflict Engine**: Built-in logic to prevent **HTTP 409 Conflict** errors by filtering duplicate video IDs.
* **Batch Processing**: Adds songs in batches of 50 with timed delays to stay within API safety limits.

### 🚀 Usage
1. Generate your `headers.json` using the `ytmusicapi` setup.
2. Run the script to fetch, sort, and re-create your playlists in seconds.

---

## 📸 Module 2: iOS MediaSorter Pro
Perfect for iPhone users who want to move files to Windows without losing chronological order.

### ✨ Features
* **📱 HEIC/HEIF Support**: Native support for Apple's high-efficiency formats via `pillow-heif`.
* **🎬 Video Metadata**: Extracts the "Creation Date" from `.MOV` and `.MP4` containers using `hachoir`.
* **📅 Full Date Naming**: Renames files using the `YYYY-MM-DD_0001` format.
* **🛡️ WinError 32 Fix**: Forced stream closure to prevent Windows from locking files during the rename process.
* **🕒 1904 Epoch Fix**: Automatically detects and skips the "1904" metadata bug common in QuickTime files.

---

## 🛠 Prerequisites

Install the necessary libraries before running the scripts:

```bash
# For YT Music
pip install ytmusicapi

# For Photos & HEIC
pip install Pillow pillow-heif

# For Videos
pip install hachoir

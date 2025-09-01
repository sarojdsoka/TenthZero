# TenthZero
File Integrity Checker UJAR TECH Solution intership Project
# File Integrity Checker

Welcome to the **TenthZero**! This is a simple Python tool that acts like a security guard for your files. It checks if your files have been tampered with (changed, edited, or corrupted) by creating and comparing unique "fingerprints" (hashes) for them. If someone messes with your files, it shouts an alert!

This tool is perfect for anyone who wants to protect important files (like documents, photos, or configs) and make sure they stay unchanged. It’s beginner-friendly and works on Linux, Mac, or Windows.

---

## What Does This Tool Do?

Think of it as a guard who:
1. **Takes a photo (hash)** of your files and saves it in a locked notebook (`Hash.txt`).
2. **Checks later** if the files still match their photos. If not, it yells, “Changed!”
3. **Keeps a diary** (`Logs.txt`) of everything it does, with timestamps.
4. **Locks the notebook** so nobody can edit it without permission.
5. **Asks before overwriting** the notebook if you run it again, so you don’t lose old data.

It uses **SHA256** (a secure way to make fingerprints) to ensure even tiny changes are caught.

---

## Features

- **Create Hashes**: Generate unique fingerprints for your files and save them securely.
- **Check Integrity**: Compare current files to saved hashes to detect changes.
- **Secure Notebook**: The hash file (`Hashes.txt`) is set to read-only to prevent tampering.
- **Overwrite Protection**: Asks if you want to overwrite old hashes when you run the tool again.
- **Logging**: Keeps a detailed log of all actions in `Logs.txt`.
- **Easy to Use**: Run from the command line with simple commands.

---

## Requirements

- **Python 3.x**: You need Python installed (download from [python.org](https://www.python.org/downloads/)).
- No extra libraries needed—uses built-in Python modules (`hashlib`, `os`, `datetime`).
- Works on **Linux**, **Mac**, or **Windows**.
- A terminal (Linux/Mac) or Command Prompt/PowerShell (Windows) to run the script.

---

## How to Set It Up

1. **Clone or Download the Repo**:
   - Clone: `git clone https://github.com/sarojdsoka/TenthZero.git`
2. **Navigate to the Folder**:
   ```bash
   cd TenthZero
   ```

3. **Check Python**:
   - Run: `python --version` or `python3 --version`
   - Ensure it shows Python 3.x (e.g., 3.8 or higher).

4. **Save the Script**:
   - The main script is `TenthZero.py` (already in the repo).
   - No installation needed—just run it!

---

## How to Use the Tool

The tool has two modes: **store** (save file hashes) and **check** (verify files).

### Step 1: Store Hashes
- **What it does**: Creates fingerprints (hashes) for your files and saves them in `Hashes.txt`. Locks the file to read-only.
- **Command**:
  ```bash
  python TenthZero.py store file1.txt file2.jpg
  ```
- **What happens**:
  - Generates hashes for `file1.txt` and `file2.jpg`.
  - Saves them in `Hash.txt` (e.g., `file1.txt:abc123...`).
  - Sets `Hash.txt` to read-only (nobody can edit without unlocking).
  - Logs actions in `Logs.txt` (e.g., “Stored hash for file1.txt”).
  - If `Hash.txt` exists, asks: “Overwrite? (yes/no)”. Type `yes` to replace, `no` to stop.

### Step 2: Check Files
- **What it does**: Checks if files match their saved hashes.
- **Command**:
  ```bash
  python TenthZero.py check file1.txt file2.jpg
  ```
- **What happens**:
  - Makes new hashes for the files.
  - Compares with `Hash.txt`.
  - Prints:
    - `OK: file1.txt` if unchanged.
    - `ALERT: file1.txt Changed!` if changed.
  - Logs results in `Logs.txt`.

### Example
1. Create test files:
   ```bash
   echo "Hello" > test.txt
   echo "World" > photo.jpg
   ```
2. Store hashes:
   ```bash
   python TenthZero.py store test.txt photo.jpg
   ```
   - Creates `Hash.txt` (locked) and logs in `Logs.txt`.
3. Change a file:
   ```bash
   echo "Hacked" > test.txt
   ```
4. Check:
   ```bash
   python TenthZero.py check test.txt photo.jpg
   ```
   - Output: `ALERT: test.txt Changed!` and `OK: photo.jpg`.
5. Check logs (`Logs.txt`):
   ```
   [2025-09-02 02:43:00] Stored hash for test.txt: abc123...
   [2025-09-02 02:43:00] Stored hash for photo.jpg: xyz789...
   [2025-09-02 02:43:00] Set hashes.txt to read-only
   [2025-09-02 02:45:00] ALERT: File test.txt has been tampered! (hash mismatch).
   [2025-09-02 02:45:00] File photo.jpg is intact (hash matches).
   ```

### Running Multiple Times
- **Store Mode**:
  - If you run `store` again (e.g., `python Hash.py store newfile.txt`), it checks if `Hash.txt` exists.
  - Asks: “Warning: hashes.txt already exists. Overwrite? (yes/no)”.
    - Type `yes`: Overwrites `Hash.txt` with new file’s hash, locks it again.
    - Type `no` (or anything else): Stops, keeps old `Hash.txt`.
  - Logs the choice in `Logs.txt`.
- **Check Mode**: No issue—checks against current `Hash.txt`.
- **Logs**: Always adds new entries to `Logs.txt`, never overwrites.

---

## Understanding the Logic

Think of the tool as a **security guard** for your files:
- **Store Mode**: The guard takes a photo (hash) of each file, writes it in a notebook (`Hash.txt`), locks the notebook (read-only), and notes in his diary (`Logs.txt`).
- **Check Mode**: The guard takes new photos, compares with the notebook, and shouts if they don’t match (prints “ALERT”).
- **Diary**: Every action (saving, checking, errors) is written in `Logs.txt` with the time.
- **Safety**: The notebook is locked, and you’re asked before overwriting it.

### Why Hashes?
A hash is like a unique fingerprint for a file. If even one letter changes, the hash changes completely. We use **SHA256** (a strong, secure method) to make these fingerprints.

---

## Scheduling Automatic Checks (Optional)

You can make the tool check files automatically (e.g., every hour) using **cron** (Linux/Mac) or **Task Scheduler** (Windows).

### Linux/Mac (Cron)
1. Edit crontab:
   ```bash
   crontab -e
   ```
2. Add (checks every hour):
   ```bash
   0 * * * * python [path of python file] check file1.txt file2.jpg
   ```
3. Save and exit. It’ll run hourly.

### Windows (Task Scheduler)
1. Open Task Scheduler (search in Start menu).
2. Create a task:
   - Set trigger to daily/hourly.
   - Set action to run: `python [path of python file] check file1.txt file2.jpg`
3. Save and test.

---
## Troubleshooting

- **Error: “No hash database found”**:
  - Run `store` first to create `Hash.txt`.
- **Permission denied for Hash.txt**:
  - It’s read-only (good!). Unlock it (see above) if you need to edit.
- **File not found**:
  - Check file names/paths (e.g., use `test.txt`, not `Test.txt`).
- **Python not found**:
  - Use `python3` instead of `python`, or ensure Python is installed.

---

## Contributing

Feel free to fork this repo, make changes, and submit a pull request! If you’re new, try the tweaks above or ask for help in the Issues section.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for keeping your files safe!**

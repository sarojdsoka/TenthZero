import hashlib
import os
import datetime
import stat

HASH_DB_FILE = 'Hash.txt'
LOG_FILE = 'Logs.txt'

def calculate_hash(file_path, algorithm='sha256'):
    if not os.path.exists(file_path):
        return None
    hash_func = hashlib.sha256() if algorithm == 'sha256' else hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        log_activity(f"Error calculating hash for {file_path}: {e}")
        return None

def set_read_only(file_path):
    try:
        os.chmod(file_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        log_activity(f"Set {file_path} to read-only")
    except Exception as e:
        log_activity(f"Error setting {file_path} to read-only: {e}")

def store_hashes(files):
    if os.path.exists(HASH_DB_FILE):
        print(f"Warning: {HASH_DB_FILE} already exists. Overwrite? (yes/no)")
        choice = input().lower()
        if choice != 'yes':
            log_activity("Stopped: User chose not to overwrite Hash.txt")
            print("Stopped. No changes made.")
            return
    with open(HASH_DB_FILE, 'w') as db:
        for file in files:
            hash_value = calculate_hash(file)
            if hash_value:
                db.write(f"{file}:{hash_value}\n")
                log_activity(f"Stored hash for {file}: {hash_value}")
            else:
                log_activity(f"Couldn’t store hash for {file}")
    set_read_only(HASH_DB_FILE)

def check_integrity(files):
    if not os.path.exists(HASH_DB_FILE):
        log_activity("No hash database found. Run 'store' first.")
        print("Error: Run 'store' first to save hashes.")
        return
    stored_hashes = {}
    with open(HASH_DB_FILE, 'r') as db:
        for line in db:
            file, hash_value = line.strip().split(':')
            stored_hashes[file] = hash_value
    for file in files:
        current_hash = calculate_hash(file)
        if current_hash is None:
            continue
        if file in stored_hashes and stored_hashes[file] == current_hash:
            log_activity(f"File {file} is intact (hash matches).")
            print(f"OK: {file}")
        else:
            log_activity(f"ALERT: File {file} has been Changed! (hash mismatch).")
            print(f"ALERT: {file} Changed!")

def log_activity(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as log:
        log.write(f"[{timestamp}] {message}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python TenthZero.py [store/check] file1 file2 ...")
        sys.exit(1)
    mode = sys.argv[1]
    files = sys.argv[2:]
    if mode == 'store':
        store_hashes(files)
    elif mode == 'check':
        check_integrity(files)
    else:
        print("Invalid mode. Use 'store' or 'check'.")

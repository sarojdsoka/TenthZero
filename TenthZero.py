import hashlib  
import os       
import datetime 

HASH_DB_FILE = 'Hash.txt'
LOG_FILE = 'Logs.txt' 

def calculate_hash(file_path, algorithm='sha256'):
    """Calculate the hash of a file."""
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

def store_hashes(files):
    """Store hashes of multiple files in the hash database."""
    with open(HASH_DB_FILE, 'w') as db:
        for file in files:
            hash_value = calculate_hash(file)
            if hash_value:
                db.write(f"{file}:{hash_value}\n") 
                log_activity(f"Stored hash for {file}: {hash_value}")
            else:
                log_activity(f"Failed to store hash for {file}")

def check_integrity(files):
    """Check if files match their stored hashes."""
    if not os.path.exists(HASH_DB_FILE):  
        log_activity("No hash database found. Run 'store' first.")
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
            log_activity(f"ALERT: File {file} has been changed! (hash mismatch).")
            print(f"ALERT: {file} Changed!") 

def log_activity(message):
    """Log messages with timestamp."""
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

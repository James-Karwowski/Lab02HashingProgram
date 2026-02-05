import hashlib
import json
import os

"""Calculates the SHA_256 of the file path"""
def calc_sha256(file_path):
  sha256_hash = hashlib.sha256()
  try:
    with open(file_path, "rb") as f:
      for byte_block in iter(lambda: f.read(4096), b""):
        sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
  except Exception:
    return None

def generate_hashes():
  dir_path = input("Enter the directory path to hash: ")
  if not os.path.isdir(dir_path):
    print("Invalid directory, please try again.")
    return

  os.mkdir("dir_hash_tables")
  # Using path as hash key
  hash_table = {}
  for root, _, files in os.walk(dir_path):
    for file in files:
      full_path = os.path.abspath(os.path.join(root, file))
      f_hash = calc_sha256(full_path)
      if f_hash:
        hash_table[full_path] = f_hash
  data = {"directory": os.path.abspath(dir_path), "hashes": hash_table}
  
  with open(os.path.join("dir_hash_tables", f"hash_{os.path.basename(dir_path)}.json"), "w") as f:
    json.dump(data, f, indent=4)
  print(f"Table generated with {len(hash_table)} files.")

def verify_hashes():
  if not os.path.exists("dir_hash_tables"):
    print("No hash table found. Please generate one first.")
    return
  with open(os.path.join("dir_hash_tables", f"hash_{os.path.basename(os.path.abspath(input('Enter the specific directory name (i.e. "folder_for_uncc_notes") to verify: ')))}.json"), "r") as f:
    stored_data = json.load(f)

  stored_hashes = stored_data["hashes"] # {path: hash}
  target_dir = stored_data["directory"]
  # Scan current directory and build a "Live" map
  current_files = {} # {path: hash}
  for root, _, files in os.walk(target_dir):
    for file in files:
      p = os.path.abspath(os.path.join(root, file))
      h = calc_sha256(p)
      if h:
        current_files[p] = h
  # Create helper maps for cross-referencing
  stored_hash_to_path = {h: p for p, h in stored_hashes.items()}
  updates_hashes = stored_hashes.copy()
  print(f"\n--- Verification Results for {target_dir} ---")

  #Tracking seen files to identify brand new ones later
  processed_current_paths = set()
  #Iterate through what we expected to find
  for old_path, old_hash in stored_hashes.items():
    if old_path in current_files:
      # File exists at the same path
      processed_current_paths.add(old_path)
      old_hash = current_files[old_path]
      if old_hash == stored_hashes[old_path]:
        print(f"[UNCHANGED] {old_path}")
      else:
        print(f"[MODIFIED] {old_path}")
        updates_hashes[old_path] = old_hash
    else:
      # File is missing from original path
      # Check if any currently existing file has the exact same hash
      found_at_new_path = None
      for c_path, c_hash in current_files.items():
        if c_hash == old_hash:
          found_at_new_path = c_path
          break
      if found_at_new_path:
        print(f"[RENAMED] {old_path} - FILE NAME CHANGED: {os.path.basename(old_path)} RENAMED TO {os.path.basename(found_at_new_path)}")
        del updates_hashes[old_path]
        updates_hashes[found_at_new_path] = old_hash
        processed_current_paths.add(found_at_new_path)
      else:
        print(f"[DELETED] {old_path}")
        del updates_hashes[old_path]
  
  # Check for entirely new files  
  for c_path, c_hash in current_files.items():
    if c_path not in processed_current_paths:
      print(f"[NEW FILE] {c_path}")
      updates_hashes[c_path] = c_hash
  
  stored_data["hashes"] = updates_hashes
  with open(os.path.join("dir_hash_tables", f"{os.path.basename(target_dir)}.json"), "w") as f:
    json.dump(stored_data, f, indent=4)
    print("\nHash table updated.")

def main():
  print("1. Generate Hash Table\n2. Verify Hashes\n3. Exit")
  choice = input("Select: ")
  if choice == '1': generate_hashes()
  elif choice == '2': verify_hashes()
  elif choice == '3': return
  else:
    print("Invalid choice, please try again.")

if __name__ == "__main__":
  main()

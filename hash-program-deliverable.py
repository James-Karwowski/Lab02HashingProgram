import hashlib
import json
import os

"""Calculates the SHA_256 of the file path"""
def calc_sha256(file_path):
  sha256_hash = hashlib.sha256()
  try:
    with open(file_path, "rb" as f:
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

  # Using path as hash key
  hash_table = {}
  for root, _, files in os.walk(dir_path):
    for file in files:
      full_path = os.path.abspath(os.path.join(root, file))
      f_hash = calculate_sha256(full_path)
      if f_hash:
        hash_table[full_path] = f_hash
  data = {"directory": os.path.abspath(dir_path), "hashes": hash_table}
  with open("hashes.json", "w") as f:
    json.dump(data, f, index=4)
  print(f"Table generated with {len(hash_table)} files.")

def verify_hashes():
  # Unknown

def main():
  print("1. Generate Hash Table\n2. Verify Hashes")
  choice = input("Select: ")
  if choice == '1': generate_hashes()
  elif choice == '2': verify_hashes()

if __name__ == "__main__":
  main()

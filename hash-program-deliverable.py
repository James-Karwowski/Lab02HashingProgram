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

import os
import hashlib

def hash_sensitive_data(data: str) -> tuple[bytes, bytes]:
    salt = os.urandom(16)
    hashed = hashlib.scrypt(
        data.encode('utf-8'), 
        salt=salt, 
        n=16384, r=8, p=1
    )
    return hashed, salt

def verify_sensitive_data(data: str, hashed: bytes, salt: bytes) -> bool:
    new_hash = hashlib.scrypt(
        data.encode('utf-8'), 
        salt=salt, 
        n=16384, r=8, p=1
    )
    return new_hash == hashed

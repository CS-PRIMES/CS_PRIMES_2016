import hashlib

def secure_hash(a):
    x = hashlib.sha512()
    x.update(a)
    return x.digest()

def hash_length():
    return 64

def prehash_associated_with_source(v):
    return str(v)


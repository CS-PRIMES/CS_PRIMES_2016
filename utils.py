import hashlib

def secure_hash(a):
    x = hashlib.sha224()
    x.update(a)
    return x.digest()

import hashlib

def secure_hash(a):
    x = hashlib.sha512()
    x.update(a)
    return x.digest()

def hash_length():
	return 64
from hashlib import sha256

def hash_password(password):
	# Hash a password using SHA256
	return sha256(str.encode(password)).hexdigest()

def verify_password_hash(password, hash):
	return hash_password(password) == hash

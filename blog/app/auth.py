from pwdlib import PasswordHash

# Create an instance of PasswordHash
pwd_hasher = PasswordHash.recommended()


def generate_hash(plain_password: str):
    return pwd_hasher.hash(plain_password)

def verify_password(plain_password: str, hashed_password):
    return pwd_hasher.verify(plain_password, hashed_password)
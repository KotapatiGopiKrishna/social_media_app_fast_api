
#used to hash the password
from passlib.context import CryptContext


#configuring the algorithm needed to be used for hashing the password
pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")

#funtion to be used in other files
def hash(password: str):
    return pwd_context.hash(password)

def verify(raw_password, hashed_password):
    return pwd_context.verify(raw_password, hashed_password)
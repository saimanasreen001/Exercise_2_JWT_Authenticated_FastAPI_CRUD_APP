import os
from dotenv import load_dotenv # load_dotenv class from dotenv library is used to load env variables
from passlib.context import CryptContext # CryptContext class from passlib library is used to hash password and verify password
from datetime import datetime,timedelta # used in expiry time
from jose import JWTError, jwt
from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer # OAuth2PasswordBearer class asks to send the bearer token.


load_dotenv() # loading the environment variables.

# Fetching all the env variables created in .env file
SECRET_KEY = os.getenv("SECRET_KEY","your_secret_key_here")
ALGORITHM =os.getenv("ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",30))

# CryptContext is a class from passlib library which is used to hash password and verify password
pwd_context= CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

# data is a dictionary which contains user info like data={"sub":"Admin"} 
def create_access_token(data:dict, expires_delta:timedelta=None):
    to_encode=data.copy() # A copy of data dictionary is created as dictionaries are mutable. If not created copy, values in both will change.
    if expires_delta: # if expiry time is present, simply add expiry time to the current time.
        expire = datetime.utcnow() + expires_delta
    else:             # else add 15 minutes to the current time as the expiry time.
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp":expire}) # update to_encode with expiry time as to_encode={"sub":"Admin","exp":"the expiry time"}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM) # jwt token created with to_encode and others
    return encoded_jwt

def decode_access_token(token:str):
        try:
            payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
            return payload
        except JWTError:
             return None
        
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token") # Brings the bearer token from the /token endpoint
def get_current_user(token:str=Depends(oauth2_scheme)):# Depends tell before running get_current_user function, 
                                                       # run oauth2_scheme and pass the token inside get_current_user function.
     credentials_exception=HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Could not validate credentials",
          headers={"WWW-Authenticate":"Bearer"}
     )
     payload=decode_access_token(token)
     if payload is None:
          raise credentials_exception
     username: str=payload.get("sub")
     if username is None:
          raise credentials_exception
     
     return username
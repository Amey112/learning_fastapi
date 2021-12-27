from jose import JWTError, jwt
from datetime import datetime, timedelta

from sqlalchemy.orm.session import Session

from app import models, schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import database
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

print(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if not id:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
        return token_data

    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"},)

    user_token = verify_access_token(
        token=token, credentials_exception=credentials_exception)
    user = db.query(models.User).filter(
        models.User.id == user_token.id).first()
    return(user)

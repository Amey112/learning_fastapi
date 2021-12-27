from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND
from ..database import get_db
from .. import schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login(auth_user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == auth_user.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    is_verified = utils.verify(auth_user.password, user.password)

    if not is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

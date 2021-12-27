from logging import error
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, utils, models
from ..database import get_db
from sqlalchemy.exc import SQLAlchemyError
router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user.password = utils.hash(user.password)
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='User already exists')


@router.get('/{id}', response_model=schemas.UserResponse)
def get_username(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} not found")

    return user

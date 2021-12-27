from fastapi import APIRouter, status, HTTPException
from fastapi.param_functions import Depends
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id ==
                                              vote.post_id, current_user.id == models.Vote.user_id)
    found_vote = vote_query.first()

    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user has already voted on post")
        else:
            post = db.query(models.Post).filter(
                models.Post.id == vote.post_id).first()
            if post:
                new_vote = models.Vote(post_id=vote.post_id,
                                       user_id=current_user.id)
                db.add(new_vote)
                db.commit()
                return {"Message: Successfully liked the post"}
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Post with id: {vote.post_id} does not exist")

    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully removed like"}

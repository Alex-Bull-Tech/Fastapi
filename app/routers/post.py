from fastapi import FastAPI, Response, status,  HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from .. import models, oauth2, schemas
from ..database import get_db 

router = APIRouter(
        prefix="/post",
        tags= ["posts"]
)

@router.get('/', response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user),
limit : int = 10, skip : int = 0, search : Optional[str] = ""):
    # cursor.execute("""SELECT * FROM post """)
    # post = cursor.fetchall()

 

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post : schemas.PostCreate, db: Session = Depends(get_db), current_user : int =
Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO post(title, content, published) VALUES (%s,%s,%s)RETURNING *""", (post.title, post.content,post.published))
    # conn.commit()
    # new_post = cursor.fetchone()
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(post)
    return new_post



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user : int =
Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from post WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post =  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(
        models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")

    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user : int =
Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE from post WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with the id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authotized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


 
@router.put("/post/{id}", response_model= schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,  db: Session = Depends(get_db), current_user : int =
Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    # (post.title, post.content,post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with the id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authotized to perform requested action")
    

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
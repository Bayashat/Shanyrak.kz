from fastapi import HTTPException

from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from app.db.models import User, Post

from app.api.serializers.users import CreateUser, ModifyUser, ShanyrakItem, FavoriteShanyrak


class UsersRepository:
    @staticmethod
    def create_user(db: Session, user_data: CreateUser) -> int:
        try: 
            # Try to query if the user already exists
            existing_user_email = db.query(User).filter(User.username == user_data.username).first()
            existing_user_phone = db.query(User).filter(User.phone == user_data.phone).first()
            
            if existing_user_email or existing_user_phone:
                raise HTTPException(status_code=400, detail="User already exists")
            
            # If the user does not exist, create a new user object and add it to the database
            user = User(**user_data.model_dump())
            db.add(user)
            db.commit()
            db.refresh(user)
        except Exception as e:
            # Handle exceptions (e.g., database errors, custom exceptions)
            db.rollback()
            raise e
        
        return user.id
    
    @staticmethod
    def get_by_email(db: Session, username: str) -> User:
        user = db.query(User).filter(User.username == username).first()
        
        if user:
            return user
        
        raise HTTPException(status_code=404, detail="User not found")
            
            
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: ModifyUser):
        db_user = db.query(User).filter(User.id == user_id).first()
        
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            for key, value in user_data.model_dump(exclude_unset=True).items():
                setattr(db_user, key, value)
                
        try:
            db.commit()
            db.refresh(db_user)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Invalid user data")
        
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User:
        db_user = db.query(User).filter(User.id == user_id).first()
        
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            return db_user
        
                
    @staticmethod
    def add_favorite(db: Session, user_id: int, post_id: int):
        db_user = db.query(User).filter(User.id == user_id).first()
        db_post = db.query(Post).filter(Post.id == post_id).first()

        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        elif db_post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        else:
            if str(post_id) in db_user.favorites:
                raise HTTPException(status_code=400, detail="Post already favorited")
            else:
                db_user.favorites += f"{post_id},"
                db.commit()
                db.refresh(db_user)
                        
                
    @staticmethod
    def get_favorite(db: Session, user_id: int):
        db_user = db.query(User).filter(User.id == user_id).first()
        
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        favorites_list = db_user.favorites.split(",")[:-1]
        favorite_posts = []
        for id in favorites_list:
            db_post = db.query(Post).filter(Post.id == id).first()
            favorite_posts.append(ShanyrakItem(id=id, address=db_post.address))
        return favorite_posts

    
    @staticmethod
    def delete_favorite(db: Session, user_id: int, post_id: int):
        db_user = db.query(User).filter(User.id == user_id).first()

        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            if str(post_id) in db_user.favorites:
                db_user.favorites = db_user.favorites.replace(f"{post_id},", "")
                db.commit()
                db.refresh(db_user)
            else:
                raise HTTPException(status_code=404, detail="Post not found in favorites")
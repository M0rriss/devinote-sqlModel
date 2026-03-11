from sqlmodel import Session, select

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)
    
    def get_by_email(self, email: str) -> User | None:
        return self.db.exec(select(User).where(User.email == email)).first()
    
    def create(self, user: User) -> User:
        self.db.add(user)
        # self.db.flush()
        self.db.commit()
        self.db.refresh(user)
        
        return user
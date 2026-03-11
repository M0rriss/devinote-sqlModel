
from fastapi import HTTPException
from sqlmodel import Session

from app.models.label import Label, LabelCreate
from app.repositories.label_repository import LabelRepository


class LabelService:
    
    def __init__(self, db: Session):
        self.repo = LabelRepository(db)
        
    def list(self, owner_id: int) -> list[Label]:
        return self.repo.list_by_user(owner_id)
    
    def create(self, owner_id: int, payload: LabelCreate) -> Label:
        
        if self.repo.get_by_name(owner_id, payload.name):
            raise HTTPException(status_code = 400, detail = "Etiqueta ya existe")
        
        return self.repo.create(owner_id, payload.name)
    
    def delete(self, owner_id: int, label_id: int) -> None:
        
        label = self.repo.get(label_id)
        
        if not label or label.owner_id != owner_id:
            raise  HTTPException(status_code = 404 , detail = "La etiqueta no exite o no autorizado")
        
        self.repo.delete(label)
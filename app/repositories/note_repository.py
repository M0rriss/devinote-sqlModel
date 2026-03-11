from sqlmodel import Session, select, delete

from app.models.label import NoteLabelLink
from app.models.note import Note


class NoteRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def list_owned(self, owner_id: int) -> list[Note]:
        query = select(Note).where(Note.owner_id == owner_id).order_by(Note.id.desc())
        
        return self.db.exec(query).all()
    
    def get(self, note_id: int) -> Note | None:
        return self.db.get(Note, note_id)
    
    def create(self, note: Note) -> Note:
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note
    
    def update(self, note: Note) -> Note:
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note
    
    def delete(self, note: Note) -> None:
        self.db.exec(delete(NoteLabelLink).where(NoteLabelLink.note_id == note.id ))
        self.db.delete(note)
        self.db.commit()
        
    def replace_labels(self, owner_id: int, note_id: int, label_ids: list[int]) -> None:
        self.db.exec(delete(NoteLabelLink).where(NoteLabelLink.note_id == note_id ))
        for label in set(label_ids or []):
            self.db.add(NoteLabelLink(note_id=note_id, label_id=label))
        
        self.db.commit()
        
    def list_by_ids(self, ids: list[int]) -> list[Note]:
        
        if not ids:
            return []
        
        return self.db.exec(select(Note).where(Note.id.in_(ids))).all()
            
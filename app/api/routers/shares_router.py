from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DBSession
from app.models.share import ShareRequest
from app.services.share_service import ShareService


router = APIRouter(prefix = "/shares", tags = ["Shares"])

@router.post("/note/{note_id}", status_code = status.HTTP_201_CREATED)
def share_note(note_id: int, payload: ShareRequest, db: DBSession, user: CurrentUser):
    share = ShareService(db).share_note(user.id, note_id, payload.target_user_id, payload.role)
    
    return {
        "id": share.id,
        "note_id": note_id,
        "user_target_id": payload.target_user_id,
        "role": share.role
        
    }
    
@router.delete("/notes/{note_id}", status_code = status.HTTP_204_NO_CONTENT)
def unshare_note(note_id: int, target_user_id: int, db: DBSession, user: CurrentUser):
    ShareService(db).unshare_note(user.id, note_id, target_user_id)
    
@router.post("/labels/{label_id}", status_code = status.HTTP_201_CREATED)
def share_label(label_id: int, payload: ShareRequest, db: DBSession, user: CurrentUser):
    share = ShareService(db).share_label(user.id, label_id, payload.target_user_id, payload.role)
    
    return {
    "id": share.id,
    "label_id": label_id,
    "user_target_id": payload.target_user_id,
    "role": share.role
    
    }
    
@router.delete("/labels/{label_id}", status_code = status.HTTP_204_NO_CONTENT)
def unshare_label(label_id: int, target_user_id: int, db: DBSession, user: CurrentUser):
    ShareService(db).unshare_label(user.id, label_id, target_user_id)
    return None
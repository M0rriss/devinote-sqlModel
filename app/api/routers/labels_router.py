from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DBSession
from app.models.label import LabelCreate, LabelRead
from app.services.label_service import LabelService


router = APIRouter(prefix="/labels", tags=["Labels"])

@router.get("/", response_model = list[LabelRead])
def list_labels(db: DBSession, user: CurrentUser):
    return LabelService(db).list(user.id)

@router.post("/", response_model = LabelRead, status_code = status.HTTP_201_CREATED)
def create_label(payload: LabelCreate, db: DBSession, user: CurrentUser):
    return LabelService(db).create(user.id, payload)

@router.delete("/{label_id}", status_code = status.HTTP_204_NO_CONTENT )
def delete_label(label_id: int, db: DBSession, user: CurrentUser):
    LabelService(db).delete(user.id, label_id)
    return None 
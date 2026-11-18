from fastapi import APIRouter

from schemas import UserOut
from security import AdminUser
from storage import SENT_EMAILS, USERS

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut])
def list_users(admin: AdminUser):
    return list(USERS.values())


@router.get("/emails")
def list_sent_emails(admin: AdminUser):
    return SENT_EMAILS

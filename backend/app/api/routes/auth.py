import secrets
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.models import PasswordResetToken, User
from app.schemas.auth import (
    ForgotPasswordIn,
    ForgotPasswordOut,
    LoginIn,
    MessageOut,
    RegisterIn,
    ResetPasswordIn,
    TokenOut,
    UserMeOut,
)
from app.core.config import settings
from app.services.jwt_service import create_access_token
from app.services.password_service import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenOut)
def register(body: RegisterIn, db: Session = Depends(get_db)):
    user = User(email=body.email.lower(), hashed_password=hash_password(body.password))
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    return TokenOut(access_token=create_access_token(user.id))

@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email.lower()).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return TokenOut(access_token=create_access_token(user.id))

@router.get("/me", response_model=UserMeOut)
def me(current_user: User = Depends(get_current_user)):
    return UserMeOut(id=current_user.id, email=current_user.email)

@router.post("/forgot-password", response_model=ForgotPasswordOut)
def forgot_password(body: ForgotPasswordIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email.lower()).first()
    raw = None
    if user:
        db.query(PasswordResetToken).filter(PasswordResetToken.user_id == user.id).delete()
        raw = secrets.token_urlsafe(32)
        exp = datetime.now(timezone.utc) + timedelta(hours=1)
        row = PasswordResetToken(user_id=user.id, token=raw, expires_at=exp)
        db.add(row)
        db.commit()
    msg = "If that email is registered, check your inbox for reset instructions."
    if settings.return_reset_token_in_response:
        msg = "Development mode: copy reset_token and POST /auth/reset-password with your new password."
    return ForgotPasswordOut(
        message=msg,
        reset_token=raw if user and settings.return_reset_token_in_response else None,
    )

@router.post("/reset-password", response_model=MessageOut)
def reset_password(body: ResetPasswordIn, db: Session = Depends(get_db)):
    row = db.query(PasswordResetToken).filter(PasswordResetToken.token == body.token).first()
    now = datetime.now(timezone.utc)
    if not row:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    exp = row.expires_at
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    if exp < now:
        db.delete(row)
        db.commit()
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == row.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    user.hashed_password = hash_password(body.password)
    db.delete(row)
    db.commit()
    return MessageOut(message="Password updated. You can sign in now.")

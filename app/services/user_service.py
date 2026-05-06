from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.utils import hash_password, verify_password


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, name: str, email: str, password: str, role: str, doctor_id: int = None):
    if get_user_by_email(db, email):
        return None

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role=role,
        doctor_id=doctor_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

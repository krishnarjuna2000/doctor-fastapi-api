from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.auth import UserRegister, Token
from app.services.user_service import create_user, authenticate_user
from app.database import get_db
from app.auth.utils import create_access_token

router = APIRouter()


@router.post("/register", response_model=Token)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    created_user = create_user(
        db,
        name=user_data.name,
        email=user_data.email,
        password=user_data.password,
        role=user_data.role,
        doctor_id=user_data.doctor_id,
    )

    if created_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )

    access_token = create_access_token(
        data={"sub": str(created_user.id), "role": created_user.role}
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )

    return {"access_token": access_token, "token_type": "bearer"}
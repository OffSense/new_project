from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import auth, models, schemas
from .database import Base, engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/users/", response_model=schemas.user.User)
def create_user(user_in: schemas.user.UserCreate, db: Session = Depends(get_db)):
    existing = auth.get_user_by_username(db, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user_in.password)
    user = models.user.User(username=user_in.username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/token", response_model=schemas.user.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.user.User)
async def read_users_me(
    current_user: models.user.User = Depends(auth.get_current_user),
):
    return current_user


@app.post("/profile", response_model=schemas.user.Profile)
async def create_or_update_profile(
    profile_in: schemas.user.ProfileCreate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(auth.get_current_user),
):
    profile = (
        db.query(models.profile.Profile)
        .filter(models.profile.Profile.user_id == current_user.id)
        .first()
    )
    if not profile:
        profile = models.profile.Profile(user_id=current_user.id, **profile_in.dict())
        db.add(profile)
    else:
        for key, value in profile_in.dict().items():
            setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile

# app/crud.py
# كل عمليات المستخدمين في مكان واحد

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app import models, schemas
from app.mongo import logs_collection


def write_log(action: str, user_id: int, details: dict | None = None):
    # بنسجل كل عملية في MongoDB عشان نعرف مين عمل ايه ومتى
    logs_collection.insert_one(
        {
            "action": action,
            "user_id": user_id,
            "details": details or {},
            "timestamp": datetime.now(timezone.utc),
        }
    )


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    write_log("create", db_user.id, {"name": db_user.name, "email": db_user.email})
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user is None:
        return None

    # بنعدل بس الحقول اللي اتبعتت فعلا
    changes = user.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)

    write_log("update", db_user.id, changes)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user is None:
        return False

    db.delete(db_user)
    db.commit()

    write_log("delete", user_id)
    return True
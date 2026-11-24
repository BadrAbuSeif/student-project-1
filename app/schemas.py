from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int | None = None


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    age: int | None = None


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int | None = None

    model_config = {"from_attributes": True}
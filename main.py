from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from pydantic.types import UUID4
from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID4("7d20c086-1254-4709-a4af-2cffdbd89898"),
        first_name="Nadia",
        last_name="Alviana",
        gender=Gender.female,
        roles=[Role.student]
        ),
    User(
        id=UUID4("9eea5863-bc9d-4db0-b5a1-0948d06ade32"),
        first_name="Rifqi",
        last_name="Farhan",
        gender=Gender.male,
        roles=[Role.admin, Role.user]
        ),
]

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/api/v1/users")
async def fetch_user():
    return db;


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
        raise HTTPException(
            status_code=404,
            detail=f"user with id: {user_id} does not exists"
        )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user_update.first_name is not None:
            user.first_name = user_update.first_name
        if user_update.last_name is not None:
            user.last_name = user_update.last_name
        if user_update.middle_name is not None:
            user.middle_name = user_update.middle_name
        if user_update.roles is not None:
            user.roles = user_update.roles
        return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )

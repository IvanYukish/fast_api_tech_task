from datetime import datetime, timedelta

from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings
from app.core.db import db
from app.user.dependencies import get_password_hash, authenticate_user, create_access_token, get_current_user
from app.user.schemas import UserSchema, ShowUserSchema, UpdateUserSchema

router = APIRouter()


@router.post("/", response_description="Add new user", response_model=UserSchema)
async def create_user(user: UserSchema):
    user.created_at = datetime.now().strftime("%m/%d/%y %H:%M:%S")
    user.password = get_password_hash(user.password)

    user = jsonable_encoder(user)
    new_user = await db["users"].insert_one(user)
    await db["users"].update_one(
        {
            "_id": new_user.inserted_id
        },
        {
            "$rename": {
                "password": "hashed_pass"
            }
        }
    )

    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorect ID or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["_id"]}, expires_delta=access_token_expires
    )
    await db["users"].update_one({"_id": form_data.username}, {"$set": {
        "last_login": datetime.now().strftime("%m/%d/%y %H:%M:%S"),
        "is_active": "true"
    }})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/list", response_description="List all users", response_model=list[ShowUserSchema]
)
async def list_users():
    users = await db["users"].find().to_list(100)
    for user in users:
        user["is_active"] = "false"
        try:
            if user.get("last_login"):
                last_login = datetime.strptime(user["last_login"], "%m/%d/%y %H:%M:%S")
                my_delta = datetime.now() - last_login
                if my_delta <= timedelta(days=30):
                    user["is_active"] = "true"
        except ValueError:
            pass
    return users


@router.get("/me", response_description="Current User", response_model=ShowUserSchema)
async def current_user(current_user: ShowUserSchema = Depends(get_current_user)):
    return current_user


@router.put("/admin/{user_id}", response_description="Update a user", response_model=UpdateUserSchema)
async def update_user(user_id: str, user: UpdateUserSchema, current_user: UserSchema = Depends(get_current_user)):
    if current_user["role"] == "admin":
        user = {k: v for k, v in user.dict().items() if v is not None}

        if len(user) >= 1:
            update_result = await db["users"].update_one({"_id": user_id}, {"$set": user})

            if update_result.modified_count == 1:
                if (
                        updated_user := await db["users"].find_one({"_id": user_id})
                ) is not None:
                    return updated_user

        if (existing_user := await db["users"].find_one({"_id": user_id})) is not None:
            return existing_user

        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    else:
        raise HTTPException(status_code=403, detail=f"Not having sufficient rights to modify the content")


@router.delete("/{user_id}", response_description="Delete a user")
async def delete_user(user_id: str):
    delete_result = await db["users"].delete_one({"_id": user_id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content='')

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")

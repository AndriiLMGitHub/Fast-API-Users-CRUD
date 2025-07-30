from fastapi import APIRouter, HTTPException, status
from src.users.schemas import UserCreate, UserChange
from src.users.models import User
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/')
async def get_all_users():
    users = await User.all()
    return {
        'message': "success",
        "data": users
    }

@router.post('/')
async def create_user(user: UserCreate):
    user = await User.create(
        username="Andrii",
        email="andrii@gmail.com"
    )
    return {
        "message": "success",
        "data": user
    }

@router.get('/{user_id}')
async def get_user(user_id:str):
    user = await User.get_or_none(id=user_id)
    return {
        "message": "success",
        "data": user
    }


@router.put('/{user_id}')
async def change_user(user_id: str, change_user: UserChange):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if change_user.username is not None:
        user.username = change_user.username

    if change_user.email is not None:
        user.email = change_user.email

    if change_user.first_name is not None:
        user.first_name = change_user.first_name

    if change_user.last_name is not None:
        user.last_name = change_user.last_name

    if user.is_active is not None:
        user.is_active = change_user.is_active

    await user.save()
    return {
        "message": "success",
        "info": "User has been updated successfully",
        "user": {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "modified_at": user.modified_at,
    }}


@router.delete('/{user_id}')
async def delete_user(user_id: str):
    user = User.get_or_none(id=user_id)
    if not user_id:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id} not found!")

    # Delete the user
    await user.delete()
    return JSONResponse({
        "message": "success",
        "info": "User has been deleted successfully!",
    }, status_code=status.HTTP_200_OK)
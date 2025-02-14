from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.user import user_service
from app.schemas.user import UserCreate, UserUpdate, UserResponse, PasswordUpdate
from app.schemas.response import ResponseBase, PageResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.core.exceptions import NotFoundException, ValidationException, PermissionDeniedException
from app.core.logger import logger

router = APIRouter()

@router.post("/", response_model=ResponseBase[UserResponse])
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建新用户
    """
    logger.info(f"Creating new user with username: {user_in.username}")
    try:
        user = await user_service.create_user(db=db, user_in=user_in)
        logger.info(f"User created successfully: {user.username}")
        return ResponseBase(data=user)
    except ValueError as e:
        logger.warning(f"Failed to create user: {str(e)}")
        raise ValidationException(str(e))

@router.get("/", response_model=PageResponse[List[UserResponse]])
async def get_users(
    page: int = 1,
    size: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户列表
    """
    logger.info(f"Fetching users list - page: {page}, size: {size}")
    skip = (page - 1) * size
    users = await user_service.get_users(db=db, skip=skip, limit=size)
    logger.info(f"Found {len(users)} users")
    return PageResponse(
        data=users,
        page_info={"total": len(users), "page": page, "size": size}
    )

@router.get("/{user_id}", response_model=ResponseBase[UserResponse])
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    根据ID获取用户信息
    """
    logger.info(f"Fetching user details for ID: {user_id}")
    user = await user_service.get_user(db=db, user_id=user_id)
    if not user:
        logger.warning(f"User not found with ID: {user_id}")
        raise NotFoundException("User not found")
    logger.info(f"Found user: {user.username}")
    return ResponseBase(data=user)

@router.get("/me", response_model=ResponseBase[UserResponse])
async def read_user_me(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息"""
    logger.info(f"User {current_user.username} fetching their profile")
    return ResponseBase(data=current_user)

@router.put("/me", response_model=ResponseBase[UserResponse])
async def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新当前用户信息"""
    logger.info(f"User {current_user.username} updating their profile")
    try:
        user = await user_service.update_user(
            db=db, 
            user_id=current_user.user_id, 
            user_in=user_in
        )
        logger.info(f"User {user.username} profile updated successfully")
        return ResponseBase(data=user)
    except ValueError as e:
        logger.warning(f"Failed to update user profile: {str(e)}")
        raise ValidationException(str(e))

@router.put("/{user_id}", response_model=ResponseBase[UserResponse])
async def update_user(
    user_id: str,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    更新用户信息
    """
    logger.info(f"Updating user with ID: {user_id}")
    try:
        user = await user_service.update_user(db=db, user_id=user_id, user_in=user_in)
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            raise NotFoundException("User not found")
        logger.info(f"User {user.username} updated successfully")
        return ResponseBase(data=user)
    except ValueError as e:
        logger.warning(f"Failed to update user: {str(e)}")
        raise ValidationException(str(e))

@router.put("/{user_id}/password", response_model=ResponseBase[UserResponse])
async def update_password(
    user_id: str,
    password_in: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """修改用户密码"""
    logger.info(f"Password update attempt for user ID: {user_id}")
    if current_user.user_id != user_id:
        logger.warning(f"Unauthorized password update attempt for user ID: {user_id} by user: {current_user.username}")
        raise PermissionDeniedException("Not allowed to modify other user's password")
    try:
        user = await user_service.update_password(
            db=db,
            user_id=user_id,
            old_password=password_in.old_password,
            new_password=password_in.new_password
        )
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            raise NotFoundException("User not found")
        logger.info(f"Password updated successfully for user: {user.username}")
        return ResponseBase(data=user)
    except ValueError as e:
        logger.warning(f"Password update failed: {str(e)}")
        raise ValidationException(str(e))

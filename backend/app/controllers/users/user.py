from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List
import logging
from app.models.users.user import create_user, get_user, update_user, delete_user, get_all_users, create_basetype_admin
from app.schemas.user import UserCreate, UserUpdate, UserOut, BasetypeAdminCreate
from app.config.settings import SECRET_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        logger.info(f"Decoded JWT payload: {payload}")
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None:
            logger.error(f"Invalid token: missing 'sub'")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.info(f"Authenticated user: id={user_id}, role={role}")
        return {"id": user_id, "role": role}
    except JWTError as e:
        logger.error(f"JWT decode failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/", response_model=UserOut)
async def create_user_endpoint(user: UserCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["system_admin", "basetype_admin"]:
        logger.warning(f"Unauthorized attempt to create user by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="System or basetype admin access required")
    if current_user["role"] == "basetype_admin" and user.role not in ["hr_admin", "organization_admin"]:
        logger.warning(f"Basetype admin attempted to create unauthorized role: {user.role}")
        raise HTTPException(status_code=403, detail="Basetype admin can only create hr_admin or organization_admin")
    result = await create_user(user)
    if not result:
        logger.warning(f"Failed to create user: {user.email}")
        raise HTTPException(status_code=400, detail="Email already exists")
    logger.info(f"Created user: {user.email}, role={result.role}")
    return result

@router.post("/basetype-admin", response_model=UserOut)
async def create_basetype_admin_endpoint(user: BasetypeAdminCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "system_admin":
        logger.warning(f"Unauthorized attempt to create basetype admin by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="System admin access required")
    result = await create_basetype_admin(user)
    if not result:
        logger.warning(f"Failed to create basetype admin: {user.email}")
        raise HTTPException(status_code=400, detail="Email already exists")
    logger.info(f"Created basetype admin: {user.email}")
    return result

@router.get("/me", response_model=UserOut)
async def get_current_user_endpoint(current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["id"])
    result = await get_user(user_id)
    if not result:
        logger.warning(f"User not found: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Retrieved current user: id={user_id}, role={result.role}")
    return result

@router.get("/{user_id}", response_model=UserOut)
async def get_user_endpoint(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "system_admin":
        logger.warning(f"Unauthorized attempt to get user by id={user_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="System admin access required")
    result = await get_user(user_id)
    if not result:
        logger.warning(f"User not found: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Retrieved user: id={user_id}, role={result.role}")
    return result

@router.get("/", response_model=List[UserOut])
async def get_all_users_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "system_admin":
        logger.warning(f"Unauthorized attempt to list all users by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="System admin access required")
    results = await get_all_users()
    logger.info(f"Retrieved {len(results)} users")
    return results

@router.put("/me", response_model=UserOut)
async def update_user_endpoint(user: UserUpdate, current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["id"])
    result = await update_user(user_id, user)
    if not result:
        logger.warning(f"User not found for update: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Updated user: id={user_id}, role={result.role}")
    return result

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "system_admin":
        logger.warning(f"Unauthorized attempt to delete user by id={user_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="System admin access required")
    result = await delete_user(user_id)
    if not result:
        logger.warning(f"User not found for deletion: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Deleted user: id={user_id}")
    return {"message": "User deleted"}
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.role_type import create_role_type, get_role_type, get_all_role_types, update_role_type, delete_role_type
from app.schemas.role_type import RoleTypeCreate, RoleTypeUpdate, RoleTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Create a new role type
@router.post("/role_types/", response_model=RoleTypeOut, status_code=status.HTTP_201_CREATED)
async def create_role_type_endpoint(role_type: RoleTypeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to create role type by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await create_role_type(role_type)
    if not result:
        logger.warning(f"Failed to create role type: {role_type.description}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create role type")
    return result

# Get role type by ID
@router.get("/role_types/{role_type_id}", response_model=RoleTypeOut)
async def get_role_type_endpoint(role_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to get role type id={role_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await get_role_type(role_type_id)
    if not result:
        logger.warning(f"Role type not found: id={role_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role type not found")
    return result

# Get all role types
@router.get("/role_types/", response_model=List[RoleTypeOut])
async def get_all_role_types_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to list role types by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    return await get_all_role_types()

# Update role type
@router.put("/role_types/{role_type_id}", response_model=RoleTypeOut)
async def update_role_type_endpoint(role_type_id: int, role_type: RoleTypeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to update role type id={role_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await update_role_type(role_type_id, role_type)
    if not result:
        logger.warning(f"Role type not found or no changes made: id={role_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role type not found or no changes made")
    return result

# Delete role type
@router.delete("/role_types/{role_type_id}", status_code=status.HTTP_200_OK)
async def delete_role_type_endpoint(role_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to delete role type id={role_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await delete_role_type(role_type_id)
    if not result:
        logger.warning(f"Role type not found for deletion: id={role_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role type not found")
    return {"message": "Role type deleted"}
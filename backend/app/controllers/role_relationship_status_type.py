from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.role_relationship_status_type import create_role_relationship_status_type, get_role_relationship_status_type, get_all_role_relationship_status_types, update_role_relationship_status_type, delete_role_relationship_status_type
from app.schemas.role_relationship_status_type import RoleRelationshipStatusTypeCreate, RoleRelationshipStatusTypeUpdate, RoleRelationshipStatusTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Create a new role relationship status type
@router.post("/role_relationship_status_types/", response_model=RoleRelationshipStatusTypeOut, status_code=status.HTTP_201_CREATED)
async def create_role_relationship_status_type_endpoint(role_relationship_status_type: RoleRelationshipStatusTypeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to create role relationship status type by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await create_role_relationship_status_type(role_relationship_status_type)
    if not result:
        logger.warning(f"Failed to create role relationship status type: {role_relationship_status_type.description}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create role relationship status type")
    return result

# Get role relationship status type by ID
@router.get("/role_relationship_status_types/{role_relationship_status_type_id}", response_model=RoleRelationshipStatusTypeOut)
async def get_role_relationship_status_type_endpoint(role_relationship_status_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to get role relationship status type id={role_relationship_status_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await get_role_relationship_status_type(role_relationship_status_type_id)
    if not result:
        logger.warning(f"Role relationship status type not found: id={role_relationship_status_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role relationship status type not found")
    return result

# Get all role relationship status types
@router.get("/role_relationship_status_types/", response_model=List[RoleRelationshipStatusTypeOut])
async def get_all_role_relationship_status_types_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to list role relationship status types by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    return await get_all_role_relationship_status_types()

# Update role relationship status type
@router.put("/role_relationship_status_types/{role_relationship_status_type_id}", response_model=RoleRelationshipStatusTypeOut)
async def update_role_relationship_status_type_endpoint(role_relationship_status_type_id: int, role_relationship_status_type: RoleRelationshipStatusTypeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to update role relationship status type id={role_relationship_status_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await update_role_relationship_status_type(role_relationship_status_type_id, role_relationship_status_type)
    if not result:
        logger.warning(f"Role relationship status type not found or no changes made: id={role_relationship_status_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role relationship status type not found or no changes made")
    return result

# Delete role relationship status type
@router.delete("/role_relationship_status_types/{role_relationship_status_type_id}", status_code=status.HTTP_200_OK)
async def delete_role_relationship_status_type_endpoint(role_relationship_status_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to delete role relationship status type id={role_relationship_status_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await delete_role_relationship_status_type(role_relationship_status_type_id)
    if not result:
        logger.warning(f"Role relationship status type not found for deletion: id={role_relationship_status_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role relationship status type not found")
    return {"message": "Role relationship status type deleted"}
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.priority_type import create_priority_type, get_priority_type, get_all_priority_types, update_priority_type, delete_priority_type
from app.schemas.priority_type import PriorityTypeCreate, PriorityTypeUpdate, PriorityTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Create a new priority type
@router.post("/priority_types/", response_model=PriorityTypeOut, status_code=status.HTTP_201_CREATED)
async def create_priority_type_endpoint(priority_type: PriorityTypeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to create priority type by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await create_priority_type(priority_type)
    if not result:
        logger.warning(f"Failed to create priority type: {priority_type.description}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create priority type")
    return result

# Get priority type by ID
@router.get("/priority_types/{priority_type_id}", response_model=PriorityTypeOut)
async def get_priority_type_endpoint(priority_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to get priority type id={priority_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await get_priority_type(priority_type_id)
    if not result:
        logger.warning(f"Priority type not found: id={priority_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Priority type not found")
    return result

# Get all priority types
@router.get("/priority_types/", response_model=List[PriorityTypeOut])
async def get_all_priority_types_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to list priority types by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    return await get_all_priority_types()

# Update priority type
@router.put("/priority_types/{priority_type_id}", response_model=PriorityTypeOut)
async def update_priority_type_endpoint(priority_type_id: int, priority_type: PriorityTypeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to update priority type id={priority_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await update_priority_type(priority_type_id, priority_type)
    if not result:
        logger.warning(f"Priority type not found or no changes made: id={priority_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Priority type not found or no changes made")
    return result

# Delete priority type
@router.delete("/priority_types/{priority_type_id}", status_code=status.HTTP_200_OK)
async def delete_priority_type_endpoint(priority_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to delete priority type id={priority_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await delete_priority_type(priority_type_id)
    if not result:
        logger.warning(f"Priority type not found for deletion: id={priority_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Priority type not found")
    return {"message": "Priority type deleted"}
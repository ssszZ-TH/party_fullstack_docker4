from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.relationship_type import create_relationship_type, get_relationship_type, get_all_relationship_types, update_relationship_type, delete_relationship_type
from app.schemas.relationship_type import RelationshipTypeCreate, RelationshipTypeUpdate, RelationshipTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Create a new relationship type
@router.post("/relationship_types/", response_model=RelationshipTypeOut, status_code=status.HTTP_201_CREATED)
async def create_relationship_type_endpoint(relationship_type: RelationshipTypeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to create relationship type by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await create_relationship_type(relationship_type)
    if not result:
        logger.warning(f"Failed to create relationship type: {relationship_type.description}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create relationship type")
    return result

# Get relationship type by ID
@router.get("/relationship_types/{relationship_type_id}", response_model=RelationshipTypeOut)
async def get_relationship_type_endpoint(relationship_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to get relationship type id={relationship_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await get_relationship_type(relationship_type_id)
    if not result:
        logger.warning(f"Relationship type not found: id={relationship_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relationship type not found")
    return result

# Get all relationship types
@router.get("/relationship_types/", response_model=List[RelationshipTypeOut])
async def get_all_relationship_types_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to list relationship types by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    return await get_all_relationship_types()

# Update relationship type
@router.put("/relationship_types/{relationship_type_id}", response_model=RelationshipTypeOut)
async def update_relationship_type_endpoint(relationship_type_id: int, relationship_type: RelationshipTypeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to update relationship type id={relationship_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await update_relationship_type(relationship_type_id, relationship_type)
    if not result:
        logger.warning(f"Relationship type not found or no changes made: id={relationship_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relationship type not found or no changes made")
    return result

# Delete relationship type
@router.delete("/relationship_types/{relationship_type_id}", status_code=status.HTTP_200_OK)
async def delete_relationship_type_endpoint(relationship_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to delete relationship type id={relationship_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await delete_relationship_type(relationship_type_id)
    if not result:
        logger.warning(f"Relationship type not found for deletion: id={relationship_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relationship type not found")
    return {"message": "Relationship type deleted"}
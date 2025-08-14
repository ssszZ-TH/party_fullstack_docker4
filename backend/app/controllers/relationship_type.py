from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.relationship_type import create_relationship_type, get_relationship_type, get_all_relationship_types, update_relationship_type, delete_relationship_type
from app.schemas.relationship_type import RelationshipTypeCreate, RelationshipTypeUpdate, RelationshipTypeOut
from app.controllers.users.user import get_current_user

router = APIRouter()

# Create relationship type
@router.post("/relationship_types/", response_model=RelationshipTypeOut, status_code=status.HTTP_201_CREATED)
async def create_relationship_type_endpoint(relationship_type: RelationshipTypeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await create_relationship_type(relationship_type)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create relationship type")
    return result

# Get relationship type by ID
@router.get("/relationship_types/{relationship_type_id}", response_model=RelationshipTypeOut)
async def get_relationship_type_endpoint(relationship_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await get_relationship_type(relationship_type_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relationship type not found")
    return result

# Get all relationship types
@router.get("/relationship_types/", response_model=List[RelationshipTypeOut])
async def get_all_relationship_types_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await get_all_relationship_types()

# Update relationship type
@router.put("/relationship_types/{relationship_type_id}", response_model=RelationshipTypeOut)
async def update_relationship_type_endpoint(relationship_type_id: int, relationship_type: RelationshipTypeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await update_relationship_type(relationship_type_id, relationship_type)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relationship type not found or no changes made")
    return result

# Delete relationship type
@router.delete("/relationship_types/{relationship_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_relationship_type_endpoint(relationship_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await delete_relationship_type(relationship_type_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relationship type not found")
    return None
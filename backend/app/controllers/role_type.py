from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.role_type import create_role_type, get_role_type, get_all_role_types, update_role_type, delete_role_type
from app.schemas.role_type import RoleTypeCreate, RoleTypeUpdate, RoleTypeOut
from app.controllers.users.user import get_current_user

router = APIRouter()

# Create role type
@router.post("/role_types/", response_model=RoleTypeOut, status_code=status.HTTP_201_CREATED)
async def create_role_type_endpoint(role_type: RoleTypeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await create_role_type(role_type)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create role type")
    return result

# Get role type by ID
@router.get("/role_types/{role_type_id}", response_model=RoleTypeOut)
async def get_role_type_endpoint(role_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await get_role_type(role_type_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role type not found")
    return result

# Get all role types
@router.get("/role_types/", response_model=List[RoleTypeOut])
async def get_all_role_types_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await get_all_role_types()

# Update role type
@router.put("/role_types/{role_type_id}", response_model=RoleTypeOut)
async def update_role_type_endpoint(role_type_id: int, role_type: RoleTypeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await update_role_type(role_type_id, role_type)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role type not found or no changes made")
    return result

# Delete role type
@router.delete("/role_types/{role_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role_type_endpoint(role_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await delete_role_type(role_type_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role type not found")
    return None
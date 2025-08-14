from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.contact_mechanism_type import create_contact_mechanism_type, get_contact_mechanism_type, get_all_contact_mechanism_types, update_contact_mechanism_type, delete_contact_mechanism_type
from app.schemas.contact_mechanism_type import ContactMechanismTypeCreate, ContactMechanismTypeUpdate, ContactMechanismTypeOut
from app.controllers.users.user import get_current_user
router = APIRouter()

# Create contact mechanism type
@router.post("/contact_mechanism_types/", response_model=ContactMechanismTypeOut, status_code=status.HTTP_201_CREATED)
async def create_contact_mechanism_type_endpoint(contact_mechanism_type: ContactMechanismTypeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await create_contact_mechanism_type(contact_mechanism_type)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create contact mechanism type")
    return result

# Get contact mechanism type by ID
@router.get("/contact_mechanism_types/{contact_mechanism_type_id}", response_model=ContactMechanismTypeOut)
async def get_contact_mechanism_type_endpoint(contact_mechanism_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await get_contact_mechanism_type(contact_mechanism_type_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact mechanism type not found")
    return result

# Get all contact mechanism types
@router.get("/contact_mechanism_types/", response_model=List[ContactMechanismTypeOut])
async def get_all_contact_mechanism_types_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await get_all_contact_mechanism_types()

# Update contact mechanism type
@router.put("/contact_mechanism_types/{contact_mechanism_type_id}", response_model=ContactMechanismTypeOut)
async def update_contact_mechanism_type_endpoint(contact_mechanism_type_id: int, contact_mechanism_type: ContactMechanismTypeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await update_contact_mechanism_type(contact_mechanism_type_id, contact_mechanism_type)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact mechanism type not found or no changes made")
    return result

# Delete contact mechanism type
@router.delete("/contact_mechanism_types/{contact_mechanism_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact_mechanism_type_endpoint(contact_mechanism_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await delete_contact_mechanism_type(contact_mechanism_type_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact mechanism type not found")
    return None
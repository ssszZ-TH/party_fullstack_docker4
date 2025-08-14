from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.contact_mechanism_type import create_contact_mechanism_type, get_contact_mechanism_type, get_all_contact_mechanism_types, update_contact_mechanism_type, delete_contact_mechanism_type
from app.schemas.contact_mechanism_type import ContactMechanismTypeCreate, ContactMechanismTypeUpdate, ContactMechanismTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Create a new contact mechanism type
@router.post("/contact_mechanism_types/", response_model=ContactMechanismTypeOut, status_code=status.HTTP_201_CREATED)
async def create_contact_mechanism_type_endpoint(contact_mechanism_type: ContactMechanismTypeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to create contact mechanism type by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await create_contact_mechanism_type(contact_mechanism_type)
    if not result:
        logger.warning(f"Failed to create contact mechanism type: {contact_mechanism_type.description}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create contact mechanism type")
    return result

# Get contact mechanism type by ID
@router.get("/contact_mechanism_types/{contact_mechanism_type_id}", response_model=ContactMechanismTypeOut)
async def get_contact_mechanism_type_endpoint(contact_mechanism_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to get contact mechanism type id={contact_mechanism_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await get_contact_mechanism_type(contact_mechanism_type_id)
    if not result:
        logger.warning(f"Contact mechanism type not found: id={contact_mechanism_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact mechanism type not found")
    return result

# Get all contact mechanism types
@router.get("/contact_mechanism_types/", response_model=List[ContactMechanismTypeOut])
async def get_all_contact_mechanism_types_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to list contact mechanism types by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    return await get_all_contact_mechanism_types()

# Update contact mechanism type
@router.put("/contact_mechanism_types/{contact_mechanism_type_id}", response_model=ContactMechanismTypeOut)
async def update_contact_mechanism_type_endpoint(contact_mechanism_type_id: int, contact_mechanism_type: ContactMechanismTypeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to update contact mechanism type id={contact_mechanism_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await update_contact_mechanism_type(contact_mechanism_type_id, contact_mechanism_type)
    if not result:
        logger.warning(f"Contact mechanism type not found or no changes made: id={contact_mechanism_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact mechanism type not found or no changes made")
    return result

# Delete contact mechanism type
@router.delete("/contact_mechanism_types/{contact_mechanism_type_id}", status_code=status.HTTP_200_OK)
async def delete_contact_mechanism_type_endpoint(contact_mechanism_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to delete contact mechanism type id={contact_mechanism_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await delete_contact_mechanism_type(contact_mechanism_type_id)
    if not result:
        logger.warning(f"Contact mechanism type not found for deletion: id={contact_mechanism_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact mechanism type not found")
    return {"message": "Contact mechanism type deleted"}
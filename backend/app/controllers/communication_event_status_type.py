from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.communication_event_status_type import create_communication_event_status_type, get_communication_event_status_type, get_all_communication_event_status_types, update_communication_event_status_type, delete_communication_event_status_type
from app.schemas.communication_event_status_type import CommunicationEventStatusTypeCreate, CommunicationEventStatusTypeUpdate, CommunicationEventStatusTypeOut
from app.controllers.users.user import get_current_user
router = APIRouter()

# Create communication event status type
@router.post("/communication_event_status_types/", response_model=CommunicationEventStatusTypeOut, status_code=status.HTTP_201_CREATED)
async def create_communication_event_status_type_endpoint(communication_event_status_type: CommunicationEventStatusTypeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await create_communication_event_status_type(communication_event_status_type)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create communication event status type")
    return result

# Get communication event status type by ID
@router.get("/communication_event_status_types/{communication_event_status_type_id}", response_model=CommunicationEventStatusTypeOut)
async def get_communication_event_status_type_endpoint(communication_event_status_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await get_communication_event_status_type(communication_event_status_type_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Communication event status type not found")
    return result

# Get all communication event status types
@router.get("/communication_event_status_types/", response_model=List[CommunicationEventStatusTypeOut])
async def get_all_communication_event_status_types_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await get_all_communication_event_status_types()

# Update communication event status type
@router.put("/communication_event_status_types/{communication_event_status_type_id}", response_model=CommunicationEventStatusTypeOut)
async def update_communication_event_status_type_endpoint(communication_event_status_type_id: int, communication_event_status_type: CommunicationEventStatusTypeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await update_communication_event_status_type(communication_event_status_type_id, communication_event_status_type)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Communication event status type not found or no changes made")
    return result

# Delete communication event status type
@router.delete("/communication_event_status_types/{communication_event_status_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_communication_event_status_type_endpoint(communication_event_status_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    result = await delete_communication_event_status_type(communication_event_status_type_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Communication event status type not found")
    return None
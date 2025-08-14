from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.communication_event_purpose_type import create_communication_event_purpose_type, get_communication_event_purpose_type, get_all_communication_event_purpose_types, update_communication_event_purpose_type, delete_communication_event_purpose_type
from app.schemas.communication_event_purpose_type import CommunicationEventPurposeTypeCreate, CommunicationEventPurposeTypeUpdate, CommunicationEventPurposeTypeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Create a new communication event purpose type
@router.post("/communication_event_purpose_types/", response_model=CommunicationEventPurposeTypeOut, status_code=status.HTTP_201_CREATED)
async def create_communication_event_purpose_type_endpoint(communication_event_purpose_type: CommunicationEventPurposeTypeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to create communication event purpose type by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await create_communication_event_purpose_type(communication_event_purpose_type)
    if not result:
        logger.warning(f"Failed to create communication event purpose type: {communication_event_purpose_type.description}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create communication event purpose type")
    return result

# Get communication event purpose type by ID
@router.get("/communication_event_purpose_types/{communication_event_purpose_type_id}", response_model=CommunicationEventPurposeTypeOut)
async def get_communication_event_purpose_type_endpoint(communication_event_purpose_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to get communication event purpose type id={communication_event_purpose_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await get_communication_event_purpose_type(communication_event_purpose_type_id)
    if not result:
        logger.warning(f"Communication event purpose type not found: id={communication_event_purpose_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Communication event purpose type not found")
    return result

# Get all communication event purpose types
@router.get("/communication_event_purpose_types/", response_model=List[CommunicationEventPurposeTypeOut])
async def get_all_communication_event_purpose_types_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to list communication event purpose types by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    return await get_all_communication_event_purpose_types()

# Update communication event purpose type
@router.put("/communication_event_purpose_types/{communication_event_purpose_type_id}", response_model=CommunicationEventPurposeTypeOut)
async def update_communication_event_purpose_type_endpoint(communication_event_purpose_type_id: int, communication_event_purpose_type: CommunicationEventPurposeTypeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to update communication event purpose type id={communication_event_purpose_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await update_communication_event_purpose_type(communication_event_purpose_type_id, communication_event_purpose_type)
    if not result:
        logger.warning(f"Communication event purpose type not found or no changes made: id={communication_event_purpose_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Communication event purpose type not found or no changes made")
    return result

# Delete communication event purpose type
@router.delete("/communication_event_purpose_types/{communication_event_purpose_type_id}", status_code=status.HTTP_200_OK)
async def delete_communication_event_purpose_type_endpoint(communication_event_purpose_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to delete communication event purpose type id={communication_event_purpose_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Base type admin access required")
    result = await delete_communication_event_purpose_type(communication_event_purpose_type_id)
    if not result:
        logger.warning(f"Communication event purpose type not found for deletion: id={communication_event_purpose_type_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Communication event purpose type not found")
    return {"message": "Communication event purpose type deleted"}
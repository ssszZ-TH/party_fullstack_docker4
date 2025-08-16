from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.communication_event_purpose import create_communication_event_purpose, get_communication_event_purpose, get_all_communication_event_purposes, update_communication_event_purpose, delete_communication_event_purpose
from app.schemas.communication_event_purpose import CommunicationEventPurposeCreate, CommunicationEventPurposeUpdate, CommunicationEventPurposeOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Create a new communication event purpose (organization_user, person_user)
@router.post("/communication_event_purpose/", response_model=CommunicationEventPurposeOut, status_code=status.HTTP_201_CREATED)
async def create_communication_event_purpose_endpoint(communication_event_purpose: CommunicationEventPurposeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to create communication event purpose by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await create_communication_event_purpose(communication_event_purpose, current_user["id"])
    if not result:
        logger.warning(f"Failed to create communication event purpose for party_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create communication event purpose")
    return result

# Get communication event purpose by ID (organization_user, person_user)
@router.get("/communication_event_purpose/{communication_event_purpose_id}", response_model=CommunicationEventPurposeOut)
async def get_communication_event_purpose_endpoint(communication_event_purpose_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to get communication event purpose id={communication_event_purpose_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await get_communication_event_purpose(communication_event_purpose_id, current_user["id"])
    if not result:
        logger.warning(f"Communication event purpose not found: id={communication_event_purpose_id}, party_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Communication event purpose not found")
    return result

# Get all communication event purposes (organization_user, person_user)
@router.get("/communication_event_purpose/", response_model=List[CommunicationEventPurposeOut])
async def get_all_communication_event_purposes_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to list communication event purposes by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    return await get_all_communication_event_purposes(current_user["id"])

# Update communication event purpose (organization_user, person_user)
@router.put("/communication_event_purpose/{communication_event_purpose_id}", response_model=CommunicationEventPurposeOut)
async def update_communication_event_purpose_endpoint(communication_event_purpose_id: int, communication_event_purpose: CommunicationEventPurposeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to update communication event purpose id={communication_event_purpose_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await update_communication_event_purpose(communication_event_purpose_id, communication_event_purpose, current_user["id"])
    if not result:
        logger.warning(f"Communication event purpose not found or no changes made: id={communication_event_purpose_id}, party_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Communication event purpose not found or no changes made")
    return result

# Delete communication event purpose (organization_user, person_user)
@router.delete("/communication_event_purpose/{communication_event_purpose_id}", status_code=status.HTTP_200_OK)
async def delete_communication_event_purpose_endpoint(communication_event_purpose_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to delete communication event purpose id={communication_event_purpose_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await delete_communication_event_purpose(communication_event_purpose_id, current_user["id"])
    if not result:
        logger.warning(f"Communication event purpose not found for deletion: id={communication_event_purpose_id}, party_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Communication event purpose not found")
    return {"message": "Communication event purpose deleted"}
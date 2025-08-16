from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.communication_event import create_communication_event, get_communication_event, get_all_communication_events, update_communication_event, delete_communication_event
from app.schemas.communication_event import CommunicationEventCreate, CommunicationEventUpdate, CommunicationEventOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Create a new communication event (organization_user, person_user)
@router.post("/communication_event/", response_model=CommunicationEventOut, status_code=status.HTTP_201_CREATED)
async def create_communication_event_endpoint(communication_event: CommunicationEventCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to create communication event by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await create_communication_event(communication_event, current_user["id"])
    if not result:
        logger.warning(f"Failed to create communication event for party_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create communication event")
    return result

# Get communication event by ID (organization_user, person_user)
@router.get("/communication_event/{communication_event_id}", response_model=CommunicationEventOut)
async def get_communication_event_endpoint(communication_event_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to get communication event id={communication_event_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await get_communication_event(communication_event_id, current_user["id"])
    if not result:
        logger.warning(f"Communication event not found: id={communication_event_id}, party_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Communication event not found")
    return result

# Get all communication events (organization_user, person_user)
@router.get("/communication_event/", response_model=List[CommunicationEventOut])
async def get_all_communication_events_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to list communication events by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    return await get_all_communication_events(current_user["id"])

# Update communication event (organization_user, person_user)
@router.put("/communication_event/{communication_event_id}", response_model=CommunicationEventOut)
async def update_communication_event_endpoint(communication_event_id: int, communication_event: CommunicationEventUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to update communication event id={communication_event_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await update_communication_event(communication_event_id, communication_event, current_user["id"])
    if not result:
        logger.warning(f"Communication event not found or no changes made: id={communication_event_id}, party_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Communication event not found or no changes made")
    return result

# Delete communication event (organization_user, person_user)
@router.delete("/communication_event/{communication_event_id}", status_code=status.HTTP_200_OK)
async def delete_communication_event_endpoint(communication_event_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to delete communication event id={communication_event_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await delete_communication_event(communication_event_id, current_user["id"])
    if not result:
        logger.warning(f"Communication event not found for deletion: id={communication_event_id}, party_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Communication event not found")
    return {"message": "Communication event deleted"}
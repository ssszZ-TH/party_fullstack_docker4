from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.communication_event_history import get_communication_event_history, get_all_communication_event_histories
from app.schemas.communication_event_history import CommunicationEventHistoryOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Get communication event history by ID (hr_admin, organization_admin)
@router.get("/communication_event_history/{history_id}", response_model=CommunicationEventHistoryOut)
async def get_communication_event_history_endpoint(history_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["hr_admin", "organization_admin"]:
        logger.warning(f"Unauthorized attempt to get communication event history id={history_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HR admin or Organization admin access required")
    result = await get_communication_event_history(history_id)
    if not result:
        logger.warning(f"Communication event history not found: id={history_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Communication event history not found")
    return result

# Get all communication event histories (hr_admin, organization_admin)
@router.get("/communication_event_history/", response_model=List[CommunicationEventHistoryOut])
async def get_all_communication_event_histories_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["hr_admin", "organization_admin"]:
        logger.warning(f"Unauthorized attempt to list communication event histories by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HR admin or Organization admin access required")
    return await get_all_communication_event_histories()
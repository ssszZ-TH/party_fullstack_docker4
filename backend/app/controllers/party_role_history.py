from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.party_role_history import get_party_role_history, get_all_party_role_histories
from app.schemas.party_role_history import PartyRoleHistoryOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Get party role history by ID (hr_admin, organization_admin)
@router.get("/party_role_history/{history_id}", response_model=PartyRoleHistoryOut)
async def get_party_role_history_endpoint(history_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["hr_admin", "organization_admin"]:
        logger.warning(f"Unauthorized attempt to get party role history id={history_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HR admin or Organization admin access required")
    result = await get_party_role_history(history_id)
    if not result:
        logger.warning(f"Party role history not found: id={history_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Party role history not found")
    return result

# Get all party role histories (hr_admin, organization_admin)
@router.get("/party_role_history/", response_model=List[PartyRoleHistoryOut])
async def get_all_party_role_histories_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["hr_admin", "organization_admin"]:
        logger.warning(f"Unauthorized attempt to list party role histories by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HR admin or Organization admin access required")
    return await get_all_party_role_histories()
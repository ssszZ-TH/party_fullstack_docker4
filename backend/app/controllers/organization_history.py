from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.organization_history import get_organization_history, get_all_organization_histories
from app.schemas.organization_history import OrganizationHistoryOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Get organization history by ID (organization_admin)
@router.get("/organization_history/{history_id}", response_model=OrganizationHistoryOut)
async def get_organization_history_endpoint(history_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "organization_admin":
        logger.warning(f"Unauthorized attempt to get organization history id={history_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization admin access required")
    result = await get_organization_history(history_id)
    if not result:
        logger.warning(f"Organization history not found: id={history_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization history not found")
    return result

# Get all organization histories (organization_admin)
@router.get("/organization_history/", response_model=List[OrganizationHistoryOut])
async def get_all_organization_histories_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "organization_admin":
        logger.warning(f"Unauthorized attempt to list organization histories by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization admin access required")
    return await get_all_organization_histories()
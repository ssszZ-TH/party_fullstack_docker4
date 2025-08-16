from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.passport_history import get_passport_history, get_all_passport_histories
from app.schemas.passport_history import PassportHistoryOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Get passport history by ID (hr_admin)
@router.get("/passport_history/{history_id}", response_model=PassportHistoryOut)
async def get_passport_history_endpoint(history_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to get passport history id={history_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HR admin access required")
    result = await get_passport_history(history_id)
    if not result:
        logger.warning(f"Passport history not found: id={history_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Passport history not found")
    return result

# Get all passport histories (hr_admin)
@router.get("/passport_history/", response_model=List[PassportHistoryOut])
async def get_all_passport_histories_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to list passport histories by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HR admin access required")
    return await get_all_passport_histories()
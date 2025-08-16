from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.person_history import get_person_history, get_all_person_histories
from app.schemas.person_history import PersonHistoryOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Get person history by ID (hr_admin)
@router.get("/person_history/{history_id}", response_model=PersonHistoryOut)
async def get_person_history_endpoint(history_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to get person history id={history_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HR admin access required")
    result = await get_person_history(history_id)
    if not result:
        logger.warning(f"Person history not found: id={history_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person history not found")
    return result

# Get all person histories (hr_admin)
@router.get("/person_history/", response_model=List[PersonHistoryOut])
async def get_all_person_histories_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to list person histories by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HR admin access required")
    return await get_all_person_histories()
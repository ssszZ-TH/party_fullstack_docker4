from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.role_relationship_history import get_role_relationship_history, get_all_role_relationship_histories
from app.schemas.role_relationship_history import RoleRelationshipHistoryOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Get role relationship history by ID (hr_admin, organization_admin)
@router.get("/role_relationship_history/{history_id}", response_model=RoleRelationshipHistoryOut)
async def get_role_relationship_history_endpoint(history_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["hr_admin", "organization_admin"]:
        logger.warning(f"Unauthorized attempt to get role relationship history id={history_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HR admin or Organization admin access required")
    result = await get_role_relationship_history(history_id)
    if not result:
        logger.warning(f"Role relationship history not found: id={history_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role relationship history not found")
    return result

# Get all role relationship histories (hr_admin, organization_admin)
@router.get("/role_relationship_history/", response_model=List[RoleRelationshipHistoryOut])
async def get_all_role_relationship_histories_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["hr_admin", "organization_admin"]:
        logger.warning(f"Unauthorized attempt to list role relationship histories by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HR admin or Organization admin access required")
    return await get_all_role_relationship_histories()
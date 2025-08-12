from fastapi import APIRouter, HTTPException, Depends
import logging
from typing import List
from app.models.income_range import create_income_range, get_income_range, get_all_income_ranges, update_income_range, delete_income_range
from app.schemas.income_range import IncomeRangeCreate, IncomeRangeUpdate, IncomeRangeOut
from app.controllers.users.user import get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/income_ranges", tags=["income_ranges"])

# Create income range
# Role: basetype_admin
@router.post("/", response_model=IncomeRangeOut)
async def create_income_range_endpoint(income_range: IncomeRangeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to create income range by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await create_income_range(income_range)
    if not result:
        logger.warning(f"Failed to create income range: {income_range.description}")
        raise HTTPException(status_code=400, detail="Income range already exists")
    return result

# Get income range by ID
# Role: basetype_admin
@router.get("/{income_range_id}", response_model=IncomeRangeOut)
async def get_income_range_endpoint(income_range_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to get income range by id={income_range_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await get_income_range(income_range_id)
    if not result:
        logger.warning(f"Income range not found: id={income_range_id}")
        raise HTTPException(status_code=404, detail="Income range not found")
    return result

# List all income ranges
# Role: basetype_admin
@router.get("/", response_model=List[IncomeRangeOut])
async def get_all_income_ranges_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to list income ranges by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    results = await get_all_income_ranges()
    return results

# Update income range
# Role: basetype_admin
@router.put("/{income_range_id}", response_model=IncomeRangeOut)
async def update_income_range_endpoint(income_range_id: int, income_range: IncomeRangeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to update income range by id={income_range_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await update_income_range(income_range_id, income_range)
    if not result:
        logger.warning(f"Income range not found for update: id={income_range_id}")
        raise HTTPException(status_code=404, detail="Income range not found")
    return result

# Delete income range
# Role: basetype_admin
@router.delete("/{income_range_id}")
async def delete_income_range_endpoint(income_range_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to delete income range by id={income_range_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await delete_income_range(income_range_id)
    if not result:
        logger.warning(f"Income range not found for deletion: id={income_range_id}")
        raise HTTPException(status_code=404, detail="Income range not found")
    return {"message": "Income range deleted"}
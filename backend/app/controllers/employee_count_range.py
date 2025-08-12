from fastapi import APIRouter, HTTPException, Depends
import logging
from typing import List
from app.models.employee_count_range import create_employee_count_range, get_employee_count_range, get_all_employee_count_ranges, update_employee_count_range, delete_employee_count_range
from app.schemas.employee_count_range import EmployeeCountRangeCreate, EmployeeCountRangeUpdate, EmployeeCountRangeOut
from app.controllers.users.user import get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/employee_count_ranges", tags=["employee_count_ranges"])

# Create employee count range
# Role: basetype_admin
@router.post("/", response_model=EmployeeCountRangeOut)
async def create_employee_count_range_endpoint(employee_count_range: EmployeeCountRangeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to create employee count range by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await create_employee_count_range(employee_count_range)
    if not result:
        logger.warning(f"Failed to create employee count range: {employee_count_range.description}")
        raise HTTPException(status_code=400, detail="Employee count range already exists")
    return result

# Get employee count range by ID
# Role: basetype_admin
@router.get("/{employee_count_range_id}", response_model=EmployeeCountRangeOut)
async def get_employee_count_range_endpoint(employee_count_range_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to get employee count range by id={employee_count_range_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await get_employee_count_range(employee_count_range_id)
    if not result:
        logger.warning(f"Employee count range not found: id={employee_count_range_id}")
        raise HTTPException(status_code=404, detail="Employee count range not found")
    return result

# List all employee count ranges
# Role: basetype_admin
@router.get("/", response_model=List[EmployeeCountRangeOut])
async def get_all_employee_count_ranges_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to list employee count ranges by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    results = await get_all_employee_count_ranges()
    return results

# Update employee count range
# Role: basetype_admin
@router.put("/{employee_count_range_id}", response_model=EmployeeCountRangeOut)
async def update_employee_count_range_endpoint(employee_count_range_id: int, employee_count_range: EmployeeCountRangeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to update employee count range by id={employee_count_range_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await update_employee_count_range(employee_count_range_id, employee_count_range)
    if not result:
        logger.warning(f"Employee count range not found for update: id={employee_count_range_id}")
        raise HTTPException(status_code=404, detail="Employee count range not found")
    return result

# Delete employee count range
# Role: basetype_admin
@router.delete("/{employee_count_range_id}")
async def delete_employee_count_range_endpoint(employee_count_range_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to delete employee count range by id={employee_count_range_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await delete_employee_count_range(employee_count_range_id)
    if not result:
        logger.warning(f"Employee count range not found for deletion: id={employee_count_range_id}")
        raise HTTPException(status_code=404, detail="Employee count range not found")
    return {"message": "Employee count range deleted"}
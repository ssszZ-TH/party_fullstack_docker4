from fastapi import APIRouter, HTTPException, Depends
import logging
from typing import List
from app.models.industry_type import create_industry_type, get_industry_type, get_all_industry_types, update_industry_type, delete_industry_type
from app.schemas.industry_type import IndustryTypeCreate, IndustryTypeUpdate, IndustryTypeOut
from app.controllers.users.user import get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/industry_types", tags=["industry_types"])

# Create industry type
# Role: basetype_admin
@router.post("/", response_model=IndustryTypeOut)
async def create_industry_type_endpoint(industry_type: IndustryTypeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to create industry type by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await create_industry_type(industry_type)
    if not result:
        logger.warning(f"Failed to create industry type: {industry_type.description}")
        raise HTTPException(status_code=400, detail="Industry type already exists")
    return result

# Get industry type by ID
# Role: basetype_admin
@router.get("/{industry_type_id}", response_model=IndustryTypeOut)
async def get_industry_type_endpoint(industry_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to get industry type by id={industry_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await get_industry_type(industry_type_id)
    if not result:
        logger.warning(f"Industry type not found: id={industry_type_id}")
        raise HTTPException(status_code=404, detail="Industry type not found")
    return result

# List all industry types
# Role: basetype_admin
@router.get("/", response_model=List[IndustryTypeOut])
async def get_all_industry_types_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to list industry types by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    results = await get_all_industry_types()
    return results

# Update industry type
# Role: basetype_admin
@router.put("/{industry_type_id}", response_model=IndustryTypeOut)
async def update_industry_type_endpoint(industry_type_id: int, industry_type: IndustryTypeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to update industry type by id={industry_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await update_industry_type(industry_type_id, industry_type)
    if not result:
        logger.warning(f"Industry type not found for update: id={industry_type_id}")
        raise HTTPException(status_code=404, detail="Industry type not found")
    return result

# Delete industry type
# Role: basetype_admin
@router.delete("/{industry_type_id}")
async def delete_industry_type_endpoint(industry_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to delete industry type by id={industry_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await delete_industry_type(industry_type_id)
    if not result:
        logger.warning(f"Industry type not found for deletion: id={industry_type_id}")
        raise HTTPException(status_code=404, detail="Industry type not found")
    return {"message": "Industry type deleted"}
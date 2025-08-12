from fastapi import APIRouter, HTTPException, Depends
import logging
from typing import List
from app.models.ethnicity_type import create_ethnicity_type, get_ethnicity_type, get_all_ethnicity_types, update_ethnicity_type, delete_ethnicity_type
from app.schemas.ethnicity_type import EthnicityTypeCreate, EthnicityTypeUpdate, EthnicityTypeOut
from app.controllers.users.user import get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ethnicity_types", tags=["ethnicity_types"])

# Create ethnicity type
# Role: basetype_admin
@router.post("/", response_model=EthnicityTypeOut)
async def create_ethnicity_type_endpoint(ethnicity_type: EthnicityTypeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to create ethnicity type by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await create_ethnicity_type(ethnicity_type)
    if not result:
        logger.warning(f"Failed to create ethnicity type: {ethnicity_type.description}")
        raise HTTPException(status_code=400, detail="Ethnicity type already exists")
    return result

# Get ethnicity type by ID
# Role: basetype_admin
@router.get("/{ethnicity_type_id}", response_model=EthnicityTypeOut)
async def get_ethnicity_type_endpoint(ethnicity_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to get ethnicity type by id={ethnicity_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await get_ethnicity_type(ethnicity_type_id)
    if not result:
        logger.warning(f"Ethnicity type not found: id={ethnicity_type_id}")
        raise HTTPException(status_code=404, detail="Ethnicity type not found")
    return result

# List all ethnicity types
# Role: basetype_admin
@router.get("/", response_model=List[EthnicityTypeOut])
async def get_all_ethnicity_types_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to list ethnicity types by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    results = await get_all_ethnicity_types()
    return results

# Update ethnicity type
# Role: basetype_admin
@router.put("/{ethnicity_type_id}", response_model=EthnicityTypeOut)
async def update_ethnicity_type_endpoint(ethnicity_type_id: int, ethnicity_type: EthnicityTypeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to update ethnicity type by id={ethnicity_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await update_ethnicity_type(ethnicity_type_id, ethnicity_type)
    if not result:
        logger.warning(f"Ethnicity type not found for update: id={ethnicity_type_id}")
        raise HTTPException(status_code=404, detail="Ethnicity type not found")
    return result

# Delete ethnicity type
# Role: basetype_admin
@router.delete("/{ethnicity_type_id}")
async def delete_ethnicity_type_endpoint(ethnicity_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to delete ethnicity type by id={ethnicity_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await delete_ethnicity_type(ethnicity_type_id)
    if not result:
        logger.warning(f"Ethnicity type not found for deletion: id={ethnicity_type_id}")
        raise HTTPException(status_code=404, detail="Ethnicity type not found")
    return {"message": "Ethnicity type deleted"}
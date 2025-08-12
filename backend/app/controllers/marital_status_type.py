from fastapi import APIRouter, HTTPException, Depends
import logging
from typing import List
from app.models.marital_status_type import create_marital_status_type, get_marital_status_type, get_all_marital_status_types, update_marital_status_type, delete_marital_status_type
from app.schemas.marital_status_type import MaritalStatusTypeCreate, MaritalStatusTypeUpdate, MaritalStatusTypeOut
from app.controllers.users.user import get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/marital_status_types", tags=["marital_status_types"])

# Create marital status type
# Role: basetype_admin
@router.post("/", response_model=MaritalStatusTypeOut)
async def create_marital_status_type_endpoint(marital_status_type: MaritalStatusTypeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to create marital status type by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await create_marital_status_type(marital_status_type)
    if not result:
        logger.warning(f"Failed to create marital status type: {marital_status_type.description}")
        raise HTTPException(status_code=400, detail="Marital status type already exists")
    return result

# Get marital status type by ID
# Role: basetype_admin
@router.get("/{marital_status_type_id}", response_model=MaritalStatusTypeOut)
async def get_marital_status_type_endpoint(marital_status_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to get marital status type by id={marital_status_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await get_marital_status_type(marital_status_type_id)
    if not result:
        logger.warning(f"Marital status type not found: id={marital_status_type_id}")
        raise HTTPException(status_code=404, detail="Marital status type not found")
    return result

# List all marital status types
# Role: basetype_admin
@router.get("/", response_model=List[MaritalStatusTypeOut])
async def get_all_marital_status_types_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to list marital status types by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    results = await get_all_marital_status_types()
    return results

# Update marital status type
# Role: basetype_admin
@router.put("/{marital_status_type_id}", response_model=MaritalStatusTypeOut)
async def update_marital_status_type_endpoint(marital_status_type_id: int, marital_status_type: MaritalStatusTypeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to update marital status type by id={marital_status_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await update_marital_status_type(marital_status_type_id, marital_status_type)
    if not result:
        logger.warning(f"Marital status type not found for update: id={marital_status_type_id}")
        raise HTTPException(status_code=404, detail="Marital status type not found")
    return result

# Delete marital status type
# Role: basetype_admin
@router.delete("/{marital_status_type_id}")
async def delete_marital_status_type_endpoint(marital_status_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to delete marital status type by id={marital_status_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await delete_marital_status_type(marital_status_type_id)
    if not result:
        logger.warning(f"Marital status type not found for deletion: id={marital_status_type_id}")
        raise HTTPException(status_code=404, detail="Marital status type not found")
    return {"message": "Marital status type deleted"}
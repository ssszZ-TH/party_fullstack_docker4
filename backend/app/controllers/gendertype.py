from fastapi import APIRouter, HTTPException, Depends
import logging
from typing import List
from app.models.gendertype import create_gender_type, get_gender_type, get_all_gender_types, update_gender_type, delete_gender_type
from app.schemas.gendertype import GenderTypeCreate, GenderTypeUpdate, GenderTypeOut
from app.controllers.users.user import get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/gender_types", tags=["gender_types"])

# Create gender type
# Role: basetype_admin
@router.post("/", response_model=GenderTypeOut)
async def create_gender_type_endpoint(gender_type: GenderTypeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to create gender type by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await create_gender_type(gender_type)
    if not result:
        logger.warning(f"Failed to create gender type: {gender_type.description}")
        raise HTTPException(status_code=400, detail="Gender type already exists")
    return result

# Get gender type by ID
# Role: basetype_admin
@router.get("/{gender_type_id}", response_model=GenderTypeOut)
async def get_gender_type_endpoint(gender_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to get gender type by id={gender_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await get_gender_type(gender_type_id)
    if not result:
        logger.warning(f"Gender type not found: id={gender_type_id}")
        raise HTTPException(status_code=404, detail="Gender type not found")
    return result

# List all gender types
# Role: basetype_admin
@router.get("/", response_model=List[GenderTypeOut])
async def get_all_gender_types_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to list gender types by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    results = await get_all_gender_types()
    return results

# Update gender type
# Role: basetype_admin
@router.put("/{gender_type_id}", response_model=GenderTypeOut)
async def update_gender_type_endpoint(gender_type_id: int, gender_type: GenderTypeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to update gender type by id={gender_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await update_gender_type(gender_type_id, gender_type)
    if not result:
        logger.warning(f"Gender type not found for update: id={gender_type_id}")
        raise HTTPException(status_code=404, detail="Gender type not found")
    return result

# Delete gender type
# Role: basetype_admin
@router.delete("/{gender_type_id}")
async def delete_gender_type_endpoint(gender_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to delete gender type by id={gender_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await delete_gender_type(gender_type_id)
    if not result:
        logger.warning(f"Gender type not found for deletion: id={gender_type_id}")
        raise HTTPException(status_code=404, detail="Gender type not found")
    return {"message": "Gender type deleted"}
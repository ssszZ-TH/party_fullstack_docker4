from fastapi import APIRouter, HTTPException, Depends
import logging
from typing import List
from app.models.organization_type import create_organization_type, get_organization_type, get_all_organization_types, update_organization_type, delete_organization_type
from app.schemas.organization_type import OrganizationTypeCreate, OrganizationTypeUpdate, OrganizationTypeOut
from app.controllers.users.user import get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/organization_types", tags=["organization_types"])

# Create organization type
# Role: basetype_admin
@router.post("/", response_model=OrganizationTypeOut)
async def create_organization_type_endpoint(organization_type: OrganizationTypeCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to create organization type by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await create_organization_type(organization_type)
    if not result:
        logger.warning(f"Failed to create organization type: {organization_type.description}")
        raise HTTPException(status_code=400, detail="Organization type already exists")
    return result

# Get organization type by ID
# Role: basetype_admin
@router.get("/{organization_type_id}", response_model=OrganizationTypeOut)
async def get_organization_type_endpoint(organization_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to get organization type by id={organization_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await get_organization_type(organization_type_id)
    if not result:
        logger.warning(f"Organization type not found: id={organization_type_id}")
        raise HTTPException(status_code=404, detail="Organization type not found")
    return result

# List all organization types
# Role: basetype_admin
@router.get("/", response_model=List[OrganizationTypeOut])
async def get_all_organization_types_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to list organization types by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    results = await get_all_organization_types()
    return results

# Update organization type
# Role: basetype_admin
@router.put("/{organization_type_id}", response_model=OrganizationTypeOut)
async def update_organization_type_endpoint(organization_type_id: int, organization_type: OrganizationTypeUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to update organization type by id={organization_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await update_organization_type(organization_type_id, organization_type)
    if not result:
        logger.warning(f"Organization type not found for update: id={organization_type_id}")
        raise HTTPException(status_code=404, detail="Organization type not found")
    return result

# Delete organization type
# Role: basetype_admin
@router.delete("/{organization_type_id}")
async def delete_organization_type_endpoint(organization_type_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to delete organization type by id={organization_type_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await delete_organization_type(organization_type_id)
    if not result:
        logger.warning(f"Organization type not found for deletion: id={organization_type_id}")
        raise HTTPException(status_code=404, detail="Organization type not found")
    return {"message": "Organization type deleted"}
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.party_role import create_party_role, get_party_role, get_all_party_roles, update_party_role, delete_party_role
from app.schemas.party_role import PartyRoleCreate, PartyRoleUpdate, PartyRoleOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Create a new party role (organization_user, person_user)
@router.post("/party_role/", response_model=PartyRoleOut, status_code=status.HTTP_201_CREATED)
async def create_party_role_endpoint(party_role: PartyRoleCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to create party role by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await create_party_role(party_role, current_user["id"])
    if not result:
        logger.warning(f"Failed to create party role for party_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create party role")
    return result

# Get party role by ID (organization_user, person_user)
@router.get("/party_role/{party_role_id}", response_model=PartyRoleOut)
async def get_party_role_endpoint(party_role_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to get party role id={party_role_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await get_party_role(party_role_id, current_user["id"])
    if not result:
        logger.warning(f"Party role not found: id={party_role_id}, party_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Party role not found")
    return result

# Get all party roles (organization_user, person_user)
@router.get("/party_role/", response_model=List[PartyRoleOut])
async def get_all_party_roles_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to list party roles by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    return await get_all_party_roles(current_user["id"])

# Update party role (organization_user, person_user)
@router.put("/party_role/{party_role_id}", response_model=PartyRoleOut)
async def update_party_role_endpoint(party_role_id: int, party_role: PartyRoleUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to update party role id={party_role_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await update_party_role(party_role_id, party_role, current_user["id"])
    if not result:
        logger.warning(f"Party role not found or no changes made: id={party_role_id}, party_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Party role not found or no changes made")
    return result

# Delete party role (organization_user, person_user)
@router.delete("/party_role/{party_role_id}", status_code=status.HTTP_200_OK)
async def delete_party_role_endpoint(party_role_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to delete party role id={party_role_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await delete_party_role(party_role_id, current_user["id"])
    if not result:
        logger.warning(f"Party role not found for deletion: id={party_role_id}, party_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Party role not found")
    return {"message": "Party role deleted"}
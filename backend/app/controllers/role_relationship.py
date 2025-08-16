from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.role_relationship import create_role_relationship, get_role_relationship, get_all_role_relationships, update_role_relationship, delete_role_relationship
from app.schemas.role_relationship import RoleRelationshipCreate, RoleRelationshipUpdate, RoleRelationshipOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Create a new role relationship (organization_user, person_user)
@router.post("/role_relationship/", response_model=RoleRelationshipOut, status_code=status.HTTP_201_CREATED)
async def create_role_relationship_endpoint(role_relationship: RoleRelationshipCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to create role relationship by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await create_role_relationship(role_relationship, current_user["id"])
    if not result:
        logger.warning(f"Failed to create role relationship for from_party_role_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create role relationship")
    return result

# Get role relationship by ID (organization_user, person_user)
@router.get("/role_relationship/{role_relationship_id}", response_model=RoleRelationshipOut)
async def get_role_relationship_endpoint(role_relationship_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to get role relationship id={role_relationship_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await get_role_relationship(role_relationship_id, current_user["id"])
    if not result:
        logger.warning(f"Role relationship not found: id={role_relationship_id}, party_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role relationship not found")
    return result

# Get all role relationships (organization_user, person_user)
@router.get("/role_relationship/", response_model=List[RoleRelationshipOut])
async def get_all_role_relationships_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to list role relationships by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    return await get_all_role_relationships(current_user["id"])

# Update role relationship (organization_user, person_user)
@router.put("/role_relationship/{role_relationship_id}", response_model=RoleRelationshipOut)
async def update_role_relationship_endpoint(role_relationship_id: int, role_relationship: RoleRelationshipUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to update role relationship id={role_relationship_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await update_role_relationship(role_relationship_id, role_relationship, current_user["id"])
    if not result:
        logger.warning(f"Role relationship not found or no changes made: id={role_relationship_id}, from_party_role_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role relationship not found or no changes made")
    return result

# Delete role relationship (organization_user, person_user)
@router.delete("/role_relationship/{role_relationship_id}", status_code=status.HTTP_200_OK)
async def delete_role_relationship_endpoint(role_relationship_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["organization_user", "person_user"]:
        logger.warning(f"Unauthorized attempt to delete role relationship id={role_relationship_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization or person user access required")
    result = await delete_role_relationship(role_relationship_id, current_user["id"])
    if not result:
        logger.warning(f"Role relationship not found for deletion: id={role_relationship_id}, party_id={current_user['id']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role relationship not found")
    return {"message": "Role relationship deleted"}
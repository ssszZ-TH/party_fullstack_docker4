from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List
import logging
from app.models.organizations.organization import create_organization, get_organization, update_organization, delete_organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationOut
from app.config.settings import SECRET_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/organizations", tags=["organizations"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        logger.info(f"Decoded JWT payload: {payload}")
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None:
            logger.error(f"Invalid token: missing 'sub'")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.info(f"Authenticated user: id={user_id}, role={role}")
        return {"id": user_id, "role": role}
    except JWTError as e:
        logger.error(f"JWT decode failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/", response_model=OrganizationOut)
async def create_organization_endpoint(organization: OrganizationCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "organization_admin":
        logger.warning(f"Unauthorized attempt to create organization by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Organization admin access required")
    result = await create_organization(organization)
    if not result:
        logger.warning(f"Failed to create organization: {organization.name_en}")
        raise HTTPException(status_code=400, detail="Organization already exists")
    logger.info(f"Created organization: {organization.name_en}")
    return result

@router.get("/{organization_id}", response_model=OrganizationOut)
async def get_organization_endpoint(organization_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "organization_admin":
        logger.warning(f"Unauthorized attempt to get organization by id={organization_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Organization admin access required")
    result = await get_organization(organization_id)
    if not result:
        logger.warning(f"Organization not found: id={organization_id}")
        raise HTTPException(status_code=404, detail="Organization not found")
    logger.info(f"Retrieved organization: id={organization_id}")
    return result

@router.put("/{organization_id}", response_model=OrganizationOut)
async def update_organization_endpoint(organization_id: int, organization: OrganizationUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "organization_admin":
        logger.warning(f"Unauthorized attempt to update organization by id={organization_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Organization admin access required")
    result = await update_organization(organization_id, organization)
    if not result:
        logger.warning(f"Organization not found for update: id={organization_id}")
        raise HTTPException(status_code=404, detail="Organization not found")
    logger.info(f"Updated organization: id={organization_id}")
    return result

@router.delete("/{organization_id}")
async def delete_organization_endpoint(organization_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "organization_admin":
        logger.warning(f"Unauthorized attempt to delete organization by id={organization_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Organization admin access required")
    result = await delete_organization(organization_id)
    if not result:
        logger.warning(f"Organization not found for deletion: id={organization_id}")
        raise HTTPException(status_code=404, detail="Organization not found")
    logger.info(f"Deleted organization: id={organization_id}")
    return {"message": "Organization deleted"}
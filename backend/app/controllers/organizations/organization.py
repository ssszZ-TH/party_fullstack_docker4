from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List, Optional
from datetime import datetime, timedelta
import logging
from app.models.organizations.organization import create_organization, get_organization, get_all_organizations, update_organization, delete_organization, verify_organization_credentials
from app.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationOut, OrganizationLogin
from app.config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.controllers.users.user import get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/organizations", tags=["organizations"])  # Define organization router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/organizations/login")  # OAuth2 for token auth

# Authenticate organization from JWT token
# Role: organization_user
async def get_current_organization(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Decoded JWT payload: {payload}")
        org_id: str = payload.get("sub")
        if org_id is None:
            logger.error("Invalid token: missing 'sub'")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.info(f"Authenticated organization: id={org_id}")
        return {"id": org_id}
    except JWTError as e:
        logger.error(f"JWT decode failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

# Create organization
# Role: organization_admin
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

# Organization login
# Role: organization_user
@router.post("/login")
async def login_organization_endpoint(organization: OrganizationLogin):
    credentials = await verify_organization_credentials(organization.username, organization.password)
    if not credentials:
        logger.warning(f"Failed login attempt for organization: {organization.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(credentials["id"]), "role": "organization_user"},
        expires_delta=access_token_expires
    )
    logger.info(f"Organization logged in: {organization.username}")
    return {"access_token": access_token, "token_type": "bearer"}

# Get current organization data
# Role: organization_user
@router.get("/me", response_model=OrganizationOut)
async def get_current_organization_endpoint(current: dict = Depends(get_current_organization)):
    org_id = int(current["id"])
    result = await get_organization(org_id)
    if not result:
        logger.warning(f"Organization not found: id={org_id}")
        raise HTTPException(status_code=404, detail="Organization not found")
    logger.info(f"Retrieved current organization: id={org_id}")
    return result

# Get organization by ID
# Role: organization_user (own data only)
@router.get("/{organization_id}", response_model=OrganizationOut)
async def get_organization_endpoint(organization_id: int, current: dict = Depends(get_current_organization)):
    if int(current["id"]) != organization_id:
        logger.warning(f"Unauthorized attempt to get organization by id={organization_id} by organization: id={current['id']}")
        raise HTTPException(status_code=403, detail="Access to this organization not allowed")
    result = await get_organization(organization_id)
    if not result:
        logger.warning(f"Organization not found: id={organization_id}")
        raise HTTPException(status_code=404, detail="Organization not found")
    logger.info(f"Retrieved organization: id={organization_id}")
    return result

# List all organizations
# Role: organization_admin
@router.get("/", response_model=List[OrganizationOut])
async def get_all_organizations_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "organization_admin":
        logger.warning(f"Unauthorized attempt to list all organizations by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Organization admin access required")
    results = await get_all_organizations()
    logger.info(f"Retrieved {len(results)} organizations")
    return results

# Update organization
# Role: organization_admin
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

# Delete organization
# Role: organization_admin
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

# Create JWT access token with configurable expiration
# Role: any (used internally)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
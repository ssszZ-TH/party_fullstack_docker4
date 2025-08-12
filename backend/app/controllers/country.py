from fastapi import APIRouter, HTTPException, Depends
import logging
from typing import List
from app.models.country import create_country, get_country, get_all_countries, update_country, delete_country
from app.schemas.country import CountryCreate, CountryUpdate, CountryOut
from app.controllers.users.user import get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/countries", tags=["countries"])

# Create country
# Role: basetype_admin
@router.post("/", response_model=CountryOut)
async def create_country_endpoint(country: CountryCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to create country by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await create_country(country)
    if not result:
        logger.warning(f"Failed to create country: {country.name_en}")
        raise HTTPException(status_code=400, detail="Country already exists")
    return result

# Get country by ID
# Role: basetype_admin
@router.get("/{country_id}", response_model=CountryOut)
async def get_country_endpoint(country_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to get country by id={country_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await get_country(country_id)
    if not result:
        logger.warning(f"Country not found: id={country_id}")
        raise HTTPException(status_code=404, detail="Country not found")
    return result

# List all countries
# Role: basetype_admin
@router.get("/", response_model=List[CountryOut])
async def get_all_countries_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to list countries by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    results = await get_all_countries()
    return results

# Update country
# Role: basetype_admin
@router.put("/{country_id}", response_model=CountryOut)
async def update_country_endpoint(country_id: int, country: CountryUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to update country by id={country_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await update_country(country_id, country)
    if not result:
        logger.warning(f"Country not found for update: id={country_id}")
        raise HTTPException(status_code=404, detail="Country not found")
    return result

# Delete country
# Role: basetype_admin
@router.delete("/{country_id}")
async def delete_country_endpoint(country_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "basetype_admin":
        logger.warning(f"Unauthorized attempt to delete country by id={country_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Base type admin access required")
    result = await delete_country(country_id)
    if not result:
        logger.warning(f"Country not found for deletion: id={country_id}")
        raise HTTPException(status_code=404, detail="Country not found")
    return {"message": "Country deleted"}
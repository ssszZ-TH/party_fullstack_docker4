from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.passport import create_passport, get_passport, get_all_passports, update_passport, delete_passport
from app.schemas.passport import PassportCreate, PassportUpdate, PassportOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Create a new passport
@router.post("/passports/", response_model=PassportOut, status_code=status.HTTP_201_CREATED)
async def create_passport_endpoint(passport: PassportCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to create passport by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HR admin access required")
    result = await create_passport(passport)
    if not result:
        logger.warning(f"Failed to create passport: {passport.passport_id_number}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create passport")
    return result

# Get passport by ID
@router.get("/passports/{passport_id}", response_model=PassportOut)
async def get_passport_endpoint(passport_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to get passport id={passport_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HR admin access required")
    result = await get_passport(passport_id)
    if not result:
        logger.warning(f"Passport not found: id={passport_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Passport not found")
    return result

# Get all passports
@router.get("/passports/", response_model=List[PassportOut])
async def get_all_passports_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to list passports by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HR admin access required")
    return await get_all_passports()

# Update passport
@router.put("/passports/{passport_id}", response_model=PassportOut)
async def update_passport_endpoint(passport_id: int, passport: PassportUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to update passport id={passport_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HR admin access required")
    result = await update_passport(passport_id, passport)
    if not result:
        logger.warning(f"Passport not found or no changes made: id={passport_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Passport not found or no changes made")
    return result

# Delete passport
@router.delete("/passports/{passport_id}", status_code=status.HTTP_200_OK)
async def delete_passport_endpoint(passport_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to delete passport id={passport_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="HR admin access required")
    result = await delete_passport(passport_id)
    if not result:
        logger.warning(f"Passport not found for deletion: id={passport_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Passport not found")
    return {"message": "Passport deleted"}
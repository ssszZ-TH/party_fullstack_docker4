from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List
import logging
from app.models.persons.person import create_person, get_person, update_person, delete_person
from app.schemas.person import PersonCreate, PersonUpdate, PersonOut
from app.config.settings import SECRET_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/persons", tags=["persons"])

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

@router.post("/", response_model=PersonOut)
async def create_person_endpoint(person: PersonCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to create person by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="HR admin access required")
    result = await create_person(person)
    if not result:
        logger.warning(f"Failed to create person: {person.username}")
        raise HTTPException(status_code=400, detail="Person already exists")
    logger.info(f"Created person: {person.username}")
    return result

@router.get("/{person_id}", response_model=PersonOut)
async def get_person_endpoint(person_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to get person by id={person_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="HR admin access required")
    result = await get_person(person_id)
    if not result:
        logger.warning(f"Person not found: id={person_id}")
        raise HTTPException(status_code=404, detail="Person not found")
    logger.info(f"Retrieved person: id={person_id}")
    return result

@router.put("/{person_id}", response_model=PersonOut)
async def update_person_endpoint(person_id: int, person: PersonUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to update person by id={person_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="HR admin access required")
    result = await update_person(person_id, person)
    if not result:
        logger.warning(f"Person not found for update: id={person_id}")
        raise HTTPException(status_code=404, detail="Person not found")
    logger.info(f"Updated person: id={person_id}")
    return result

@router.delete("/{person_id}")
async def delete_person_endpoint(person_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to delete person by id={person_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="HR admin access required")
    result = await delete_person(person_id)
    if not result:
        logger.warning(f"Person not found for deletion: id={person_id}")
        raise HTTPException(status_code=404, detail="Person not found")
    logger.info(f"Deleted person: id={person_id}")
    return {"message": "Person deleted"}
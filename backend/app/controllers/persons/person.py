from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List, Optional
from datetime import datetime, timedelta
import logging
from app.models.persons.person import create_person, get_person, get_all_persons, update_person, delete_person, verify_person_credentials
from app.schemas.person import PersonCreate, PersonUpdate, PersonOut, PersonLogin
from app.config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.controllers.users.user import get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/persons", tags=["persons"])  # Define person router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/persons/login")  # OAuth2 for token auth

# Authenticate person from JWT token
# Role: person_user
async def get_current_person(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Decoded JWT payload: {payload}")
        person_id: str = payload.get("sub")
        if person_id is None:
            logger.error("Invalid token: missing 'sub'")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.info(f"Authenticated person: id={person_id}")
        return {"id": person_id}
    except JWTError as e:
        logger.error(f"JWT decode failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

# Create person
# Role: hr_admin
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

# Person login
# Role: person_user
@router.post("/login")
async def login_person_endpoint(person: PersonLogin):
    credentials = await verify_person_credentials(person.username, person.password)
    if not credentials:
        logger.warning(f"Failed login attempt for person: {person.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(credentials["id"]), "role": "person_user"},
        expires_delta=access_token_expires
    )
    logger.info(f"Person logged in: {person.username}")
    return {"access_token": access_token, "token_type": "bearer"}

# Get current person data
# Role: person_user
@router.get("/me", response_model=PersonOut)
async def get_current_person_endpoint(current: dict = Depends(get_current_person)):
    person_id = int(current["id"])
    result = await get_person(person_id)
    if not result:
        logger.warning(f"Person not found: id={person_id}")
        raise HTTPException(status_code=404, detail="Person not found")
    logger.info(f"Retrieved current person: id={person_id}")
    return result

# Get person by ID
# Role: hr_admin
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

# List all persons
# Role: hr_admin
@router.get("/", response_model=List[PersonOut])
async def get_all_persons_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to list all persons by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="HR admin access required")
    results = await get_all_persons()
    logger.info(f"Retrieved {len(results)} persons")
    return results

# Update person
# Role: hr_admin
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

# Delete person
# Role: hr_admin
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
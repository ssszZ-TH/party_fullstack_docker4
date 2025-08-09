from fastapi import APIRouter, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config.settings import SECRET_KEY, BCRYPT_SALT
from app.config.database import database
import bcrypt
import logging
from app.schemas.user import UserCreate, UserLogin
from app.models.users.user import create_user, get_user_by_email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

ALGORITHM = "HS256"

def create_access_token(data: dict):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info(f"Created JWT for user: id={data.get('sub')}, role={data.get('role')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating JWT: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create token")

@router.post("/register")
async def register(user: UserCreate):
    try:
        result = await create_user(user)
        if not result:
            logger.warning(f"Registration failed: Email {user.email} already exists")
            raise HTTPException(status_code=400, detail="Email already exists")
        logger.info(f"User registered: {user.email}, role={result.role}")
        return {"message": "User created"}
    except ValueError as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Invalid BCRYPT_SALT")

@router.post("/login")
async def login(user: UserLogin):
    db_user = await get_user_by_email(user.email)
    if not db_user:
        logger.warning(f"Login attempt with invalid email: {user.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    logger.info(f"Found user: id={db_user['id']}, email={db_user['email']}, role={db_user['role']}")
    try:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        if hashed_password != db_user["password"]:
            logger.warning(f"Invalid password for email: {user.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except ValueError as e:
        logger.error(f"Error verifying password for {user.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Invalid BCRYPT_SALT")
    token = create_access_token({"sub": str(db_user["id"]), "role": db_user["role"]})
    logger.info(f"User logged in: {user.email}, token sub={db_user['id']}, role={db_user['role']}")
    return {"access_token": token, "token_type": "bearer"}
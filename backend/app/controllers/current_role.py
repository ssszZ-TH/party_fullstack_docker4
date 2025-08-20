from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import logging
from typing import Dict
from app.config.settings import SECRET_KEY, ALGORITHM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# OAuth2 scheme to extract the token from the Authorization header
# The tokenUrl points to the endpoint where users can authenticate to get a token (e.g., /auth/login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") # ใส่ /auth/login ไปงั้นเเหละ ตามมาตรฐาน oAuth2 ไม่ได้มีผลอะไรกับระบบ

# Get current user's role from JWT token
@router.get("/currentrole", response_model=Dict[str, str])
async def get_user_role(token: str = Depends(oauth2_scheme)):
    """
    Retrieve the role of the authenticated user from a JWT token provided in the Authorization header.

    How it works:
    - The endpoint expects a Bearer token in the Authorization header (e.g., "Bearer <token>").
    - The OAuth2PasswordBearer dependency extracts the token from the header.
    - The token is decoded using the SECRET_KEY and ALGORITHM defined in settings.
    - The payload is expected to contain 'sub' (user ID) and 'role' fields.
    - If the token is missing, invalid, or lacks required fields, an HTTP 401 error is raised.
    - On success, the endpoint returns a dictionary with the user's role.

    Example request:
    - GET /currentrole
    - Header: Authorization: Bearer <jwt_token>

    Example response:
    - Success: {"role": "system_admin"}
    - Failure: 401 Unauthorized with detail "No token provided" or "Invalid token"
    """
    if not token:
        logger.error("No token provided in Authorization header")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")
    
    try:
        # Decode the JWT token to extract the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Decoded JWT payload: {payload}")
        
        # Extract user_id and role from the payload
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        
        # Validate that both user_id and role are present in the payload
        if user_id is None or role is None:
            logger.error("Invalid token: missing 'sub' or 'role'")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        logger.info(f"Retrieved role for user: id={user_id}, role={role}")
        return {"role": role}
    except JWTError as e:
        logger.error(f"JWT decode failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
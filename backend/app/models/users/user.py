from app.config.database import database
from app.config.settings import BCRYPT_SALT
from app.schemas.user import UserCreate, UserUpdate, UserOut, BasetypeAdminCreate
import bcrypt
import logging
from typing import Optional, List
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Role permissions:
# system_admin: CRUD all users
# basetype_admin: CRUD users with roles hr_admin, organization_admin
# hr_admin: CRUD person-related data
# organization_admin: CRUD organization-related data

async def get_user_by_email(email: str) -> Optional[dict]:
    query = "SELECT id, name, email, password, role, created_at, updated_at FROM users WHERE email = :email"
    result = await database.fetch_one(query=query, values={"email": email})
    logger.info(f"Queried user with email {email}: {result}")
    return result

async def create_user(user: UserCreate) -> Optional[UserOut]:
    try:
        existing_user = await get_user_by_email(user.email)
        if existing_user:
            logger.warning(f"Attempt to create user with existing email: {user.email}")
            return None
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        now = datetime.utcnow()
        query = """
            INSERT INTO users (name, email, password, role, created_at)
            VALUES (:name, :email, :password, :role, :created_at)
            RETURNING id, name, email, role, created_at, updated_at
        """
        values = {
            "name": user.name,
            "email": user.email,
            "password": hashed_password,
            "role": user.role or "hr_admin",
            "created_at": now
        }
        result = await database.fetch_one(query=query, values=values)
        logger.info(f"Created user: {user.email}, role: {user.role}")
        return UserOut(**result._mapping) if result else None
    except ValueError as e:
        logger.error(f"Error hashing password for {user.email}: {str(e)}")
        raise

async def create_basetype_admin(user: BasetypeAdminCreate) -> Optional[UserOut]:
    try:
        existing_user = await get_user_by_email(user.email)
        if existing_user:
            logger.warning(f"Attempt to create basetype admin with existing email: {user.email}")
            return None
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        now = datetime.utcnow()
        query = """
            INSERT INTO users (name, email, password, role, created_at)
            VALUES (:name, :email, :password, :role, :created_at)
            RETURNING id, name, email, role, created_at, updated_at
        """
        values = {
            "name": user.name,
            "email": user.email,
            "password": hashed_password,
            "role": "basetype_admin",
            "created_at": now
        }
        result = await database.fetch_one(query=query, values=values)
        logger.info(f"Created basetype admin: {user.email}")
        return UserOut(**result._mapping) if result else None
    except ValueError as e:
        logger.error(f"Error hashing password for {user.email}: {str(e)}")
        raise

async def get_user(user_id: int) -> Optional[UserOut]:
    query = "SELECT id, name, email, role, created_at, updated_at FROM users WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": user_id})
    logger.info(f"Retrieved user: id={user_id}")
    return UserOut(**result._mapping) if result else None

async def get_all_users() -> List[UserOut]:
    query = "SELECT id, name, email, role, created_at, updated_at FROM users ORDER BY id ASC"
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} users")
    return [UserOut(**result._mapping) for result in results]

async def update_user(user_id: int, user: UserUpdate) -> Optional[UserOut]:
    values = {"id": user_id, "updated_at": datetime.utcnow()}
    query_parts = []
    
    if user.name is not None:
        query_parts.append("name = :name")
        values["name"] = user.name
    if user.email is not None:
        query_parts.append("email = :email")
        values["email"] = user.email
    if user.password is not None:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        query_parts.append("password = :password")
        values["password"] = hashed_password

    if not query_parts:
        logger.info(f"No fields to update for user id={user_id}")
        return None

    query = f"""
        UPDATE users
        SET {', '.join(query_parts)}, updated_at = :updated_at
        WHERE id = :id
        RETURNING id, name, email, role, created_at, updated_at
    """
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Updated user: id={user_id}")
    return UserOut(**result._mapping) if result else None

async def delete_user(user_id: int) -> Optional[int]:
    query = "DELETE FROM users WHERE id = :id RETURNING id"
    result = await database.fetch_one(query=query, values={"id": user_id})
    logger.info(f"Deleted user: id={user_id}")
    return result["id"] if result else None

async def verify_user_password(user_id: int, password: str) -> bool:
    query = "SELECT password FROM users WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": user_id})
    if not result:
        logger.warning(f"User not found for password verification: id={user_id}")
        return False
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
    logger.info(f"Verified password for user id={user_id}")
    return hashed_password == result["password"]
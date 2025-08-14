from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.role_type import RoleTypeCreate, RoleTypeUpdate, RoleTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a new role type
async def create_role_type(role_type: RoleTypeCreate) -> Optional[RoleTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO role_types (description)
                VALUES (:description)
                RETURNING id, description
            """
            values = {"description": role_type.description}
            result = await database.fetch_one(query=query, values=values)
            logger.info(f"Created role type: {role_type.description}")
            return RoleTypeOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error creating role type: {str(e)}")
            raise

# Get role type by ID
async def get_role_type(role_type_id: int) -> Optional[RoleTypeOut]:
    query = """
        SELECT id, description 
        FROM role_types WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": role_type_id})
    logger.info(f"Retrieved role type: id={role_type_id}")
    return RoleTypeOut(**result._mapping) if result else None

# Get all role types
async def get_all_role_types() -> List[RoleTypeOut]:
    query = """
        SELECT id, description 
        FROM role_types ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} role types")
    return [RoleTypeOut(**result._mapping) for result in results]

# Update role type
async def update_role_type(role_type_id: int, role_type: RoleTypeUpdate) -> Optional[RoleTypeOut]:
    async with database.transaction():
        try:
            values = {"id": role_type_id}
            query_parts = []

            if role_type.description is not None:
                query_parts.append("description = :description")
                values["description"] = role_type.description

            if not query_parts:
                logger.info(f"No fields to update for role type id={role_type_id}")
                return None

            query = f"""
                UPDATE role_types
                SET {', '.join(query_parts)}
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values=values)
            logger.info(f"Updated role type: id={role_type_id}")
            return RoleTypeOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error updating role type: {str(e)}")
            raise

# Delete role type
async def delete_role_type(role_type_id: int) -> Optional[int]:
    async with database.transaction():
        try:
            query = "DELETE FROM role_types WHERE id = :id RETURNING id"
            result = await database.fetch_one(query=query, values={"id": role_type_id})
            logger.info(f"Deleted role type: id={role_type_id}")
            return result["id"] if result else None
        except Exception as e:
            logger.error(f"Error deleting role type: {str(e)}")
            raise
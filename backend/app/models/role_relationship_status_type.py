from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.role_relationship_status_type import RoleRelationshipStatusTypeCreate, RoleRelationshipStatusTypeUpdate, RoleRelationshipStatusTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a new role relationship status type
async def create_role_relationship_status_type(role_relationship_status_type: RoleRelationshipStatusTypeCreate) -> Optional[RoleRelationshipStatusTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO role_relationship_status_types (description)
                VALUES (:description)
                RETURNING id, description
            """
            values = {"description": role_relationship_status_type.description}
            result = await database.fetch_one(query=query, values=values)
            logger.info(f"Created role relationship status type: {role_relationship_status_type.description}")
            return RoleRelationshipStatusTypeOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error creating role relationship status type: {str(e)}")
            raise

# Get role relationship status type by ID
async def get_role_relationship_status_type(role_relationship_status_type_id: int) -> Optional[RoleRelationshipStatusTypeOut]:
    query = """
        SELECT id, description 
        FROM role_relationship_status_types WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": role_relationship_status_type_id})
    logger.info(f"Retrieved role relationship status type: id={role_relationship_status_type_id}")
    return RoleRelationshipStatusTypeOut(**result._mapping) if result else None

# Get all role relationship status types
async def get_all_role_relationship_status_types() -> List[RoleRelationshipStatusTypeOut]:
    query = """
        SELECT id, description 
        FROM role_relationship_status_types ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} role relationship status types")
    return [RoleRelationshipStatusTypeOut(**result._mapping) for result in results]

# Update role relationship status type
async def update_role_relationship_status_type(role_relationship_status_type_id: int, role_relationship_status_type: RoleRelationshipStatusTypeUpdate) -> Optional[RoleRelationshipStatusTypeOut]:
    async with database.transaction():
        try:
            values = {"id": role_relationship_status_type_id}
            query_parts = []

            if role_relationship_status_type.description is not None:
                query_parts.append("description = :description")
                values["description"] = role_relationship_status_type.description

            if not query_parts:
                logger.info(f"No fields to update for role relationship status type id={role_relationship_status_type_id}")
                return None

            query = f"""
                UPDATE role_relationship_status_types
                SET {', '.join(query_parts)}
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values=values)
            logger.info(f"Updated role relationship status type: id={role_relationship_status_type_id}")
            return RoleRelationshipStatusTypeOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error updating role relationship status type: {str(e)}")
            raise

# Delete role relationship status type
async def delete_role_relationship_status_type(role_relationship_status_type_id: int) -> Optional[int]:
    async with database.transaction():
        try:
            query = "DELETE FROM role_relationship_status_types WHERE id = :id RETURNING id"
            result = await database.fetch_one(query=query, values={"id": role_relationship_status_type_id})
            logger.info(f"Deleted role relationship status type: id={role_relationship_status_type_id}")
            return result["id"] if result else None
        except Exception as e:
            logger.error(f"Error deleting role relationship status type: {str(e)}")
            raise
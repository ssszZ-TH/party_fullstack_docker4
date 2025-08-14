from app.config.database import database
import logging
from typing import Optional, List
from datetime import datetime
from app.schemas.priority_type import PriorityTypeCreate, PriorityTypeUpdate, PriorityTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create priority type
async def create_priority_type(priority_type: PriorityTypeCreate) -> Optional[PriorityTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO priority_types (description, created_at)
                VALUES (:description, :created_at)
                RETURNING id, description, created_at, updated_at
            """
            values = {"description": priority_type.description, "created_at": datetime.utcnow()}
            result = await database.fetch_one(query=query, values=values)
            logger.info(f"Created priority type: {priority_type.description}")
            return PriorityTypeOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error creating priority type: {str(e)}")
            raise

# Get priority type by ID
async def get_priority_type(priority_type_id: int) -> Optional[PriorityTypeOut]:
    query = """
        SELECT id, description, created_at, updated_at 
        FROM priority_types WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": priority_type_id})
    logger.info(f"Retrieved priority type: id={priority_type_id}")
    return PriorityTypeOut(**result._mapping) if result else None

# Get all priority types
async def get_all_priority_types() -> List[PriorityTypeOut]:
    query = """
        SELECT id, description, created_at, updated_at 
        FROM priority_types ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} priority types")
    return [PriorityTypeOut(**result._mapping) for result in results]

# Update priority type
async def update_priority_type(priority_type_id: int, priority_type: PriorityTypeUpdate) -> Optional[PriorityTypeOut]:
    async with database.transaction():
        try:
            values = {"id": priority_type_id, "updated_at": datetime.utcnow()}
            query_parts = []

            if priority_type.description is not None:
                query_parts.append("description = :description")
                values["description"] = priority_type.description

            if not query_parts:
                logger.info(f"No fields to update for priority type id={priority_type_id}")
                return None

            query = f"""
                UPDATE priority_types
                SET {', '.join(query_parts)}, updated_at = :updated_at
                WHERE id = :id
                RETURNING id, description, created_at, updated_at
            """
            result = await database.fetch_one(query=query, values=values)
            logger.info(f"Updated priority type: id={priority_type_id}")
            return PriorityTypeOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error updating priority type: {str(e)}")
            raise

# Delete priority type
async def delete_priority_type(priority_type_id: int) -> Optional[int]:
    async with database.transaction():
        try:
            query = "DELETE FROM priority_types WHERE id = :id RETURNING id"
            result = await database.fetch_one(query=query, values={"id": priority_type_id})
            logger.info(f"Deleted priority type: id={priority_type_id}")
            return result["id"] if result else None
        except Exception as e:
            logger.error(f"Error deleting priority type: {str(e)}")
            raise
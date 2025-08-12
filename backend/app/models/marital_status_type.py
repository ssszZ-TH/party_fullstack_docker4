from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.marital_status_type import MaritalStatusTypeCreate, MaritalStatusTypeUpdate, MaritalStatusTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create marital status type
# Role: basetype_admin
async def create_marital_status_type(marital_status_type: MaritalStatusTypeCreate) -> Optional[MaritalStatusTypeOut]:
    query = """
        INSERT INTO marital_status_types (description)
        VALUES (:description)
        RETURNING id, description
    """
    values = {"description": marital_status_type.description}
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Created marital status type: {marital_status_type.description}")
    return MaritalStatusTypeOut(**result._mapping) if result else None

# Get marital status type by ID
# Role: basetype_admin
async def get_marital_status_type(marital_status_type_id: int) -> Optional[MaritalStatusTypeOut]:
    query = "SELECT id, description FROM marital_status_types WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": marital_status_type_id})
    logger.info(f"Retrieved marital status type: id={marital_status_type_id}")
    return MaritalStatusTypeOut(**result._mapping) if result else None

# Get all marital status types
# Role: basetype_admin
async def get_all_marital_status_types() -> List[MaritalStatusTypeOut]:
    query = "SELECT id, description FROM marital_status_types ORDER BY id ASC"
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} marital status types")
    return [MaritalStatusTypeOut(**result._mapping) for result in results]

# Update marital status type
# Role: basetype_admin
async def update_marital_status_type(marital_status_type_id: int, marital_status_type: MaritalStatusTypeUpdate) -> Optional[MaritalStatusTypeOut]:
    query_parts = []
    values = {"id": marital_status_type_id}
    if marital_status_type.description is not None:
        query_parts.append("description = :description")
        values["description"] = marital_status_type.description
    if not query_parts:
        logger.info(f"No fields to update for marital status type id={marital_status_type_id}")
        return None
    query = f"""
        UPDATE marital_status_types
        SET {', '.join(query_parts)}
        WHERE id = :id
        RETURNING id, description
    """
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Updated marital status type: id={marital_status_type_id}")
    return MaritalStatusTypeOut(**result._mapping) if result else None

# Delete marital status type
# Role: basetype_admin
async def delete_marital_status_type(marital_status_type_id: int) -> Optional[int]:
    query = "DELETE FROM marital_status_types WHERE id = :id RETURNING id"
    result = await database.fetch_one(query=query, values={"id": marital_status_type_id})
    logger.info(f"Deleted marital status type: id={marital_status_type_id}")
    return result["id"] if result else None
from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.ethnicity_type import EthnicityTypeCreate, EthnicityTypeUpdate, EthnicityTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create ethnicity type
# Role: basetype_admin
async def create_ethnicity_type(ethnicity_type: EthnicityTypeCreate) -> Optional[EthnicityTypeOut]:
    query = """
        INSERT INTO ethnicity_types (description)
        VALUES (:description)
        RETURNING id, description
    """
    values = {"description": ethnicity_type.description}
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Created ethnicity type: {ethnicity_type.description}")
    return EthnicityTypeOut(**result._mapping) if result else None

# Get ethnicity type by ID
# Role: basetype_admin
async def get_ethnicity_type(ethnicity_type_id: int) -> Optional[EthnicityTypeOut]:
    query = "SELECT id, description FROM ethnicity_types WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": ethnicity_type_id})
    logger.info(f"Retrieved ethnicity type: id={ethnicity_type_id}")
    return EthnicityTypeOut(**result._mapping) if result else None

# Get all ethnicity types
# Role: basetype_admin
async def get_all_ethnicity_types() -> List[EthnicityTypeOut]:
    query = "SELECT id, description FROM ethnicity_types ORDER BY id ASC"
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} ethnicity types")
    return [EthnicityTypeOut(**result._mapping) for result in results]

# Update ethnicity type
# Role: basetype_admin
async def update_ethnicity_type(ethnicity_type_id: int, ethnicity_type: EthnicityTypeUpdate) -> Optional[EthnicityTypeOut]:
    query_parts = []
    values = {"id": ethnicity_type_id}
    if ethnicity_type.description is not None:
        query_parts.append("description = :description")
        values["description"] = ethnicity_type.description
    if not query_parts:
        logger.info(f"No fields to update for ethnicity type id={ethnicity_type_id}")
        return None
    query = f"""
        UPDATE ethnicity_types
        SET {', '.join(query_parts)}
        WHERE id = :id
        RETURNING id, description
    """
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Updated ethnicity type: id={ethnicity_type_id}")
    return EthnicityTypeOut(**result._mapping) if result else None

# Delete ethnicity type
# Role: basetype_admin
async def delete_ethnicity_type(ethnicity_type_id: int) -> Optional[int]:
    query = "DELETE FROM ethnicity_types WHERE id = :id RETURNING id"
    result = await database.fetch_one(query=query, values={"id": ethnicity_type_id})
    logger.info(f"Deleted ethnicity type: id={ethnicity_type_id}")
    return result["id"] if result else None
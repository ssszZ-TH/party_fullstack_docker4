from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.gendertype import GenderTypeCreate, GenderTypeUpdate, GenderTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create gender type
# Role: basetype_admin
async def create_gender_type(gender_type: GenderTypeCreate) -> Optional[GenderTypeOut]:
    query = """
        INSERT INTO gender_types (description)
        VALUES (:description)
        RETURNING id, description
    """
    values = {"description": gender_type.description}
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Created gender type: {gender_type.description}")
    return GenderTypeOut(**result._mapping) if result else None

# Get gender type by ID
# Role: basetype_admin
async def get_gender_type(gender_type_id: int) -> Optional[GenderTypeOut]:
    query = "SELECT id, description FROM gender_types WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": gender_type_id})
    logger.info(f"Retrieved gender type: id={gender_type_id}")
    return GenderTypeOut(**result._mapping) if result else None

# Get all gender types
# Role: basetype_admin
async def get_all_gender_types() -> List[GenderTypeOut]:
    query = "SELECT id, description FROM gender_types ORDER BY id ASC"
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} gender types")
    return [GenderTypeOut(**result._mapping) for result in results]

# Update gender type
# Role: basetype_admin
async def update_gender_type(gender_type_id: int, gender_type: GenderTypeUpdate) -> Optional[GenderTypeOut]:
    query_parts = []
    values = {"id": gender_type_id}
    if gender_type.description is not None:
        query_parts.append("description = :description")
        values["description"] = gender_type.description
    if not query_parts:
        logger.info(f"No fields to update for gender type id={gender_type_id}")
        return None
    query = f"""
        UPDATE gender_types
        SET {', '.join(query_parts)}
        WHERE id = :id
        RETURNING id, description
    """
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Updated gender type: id={gender_type_id}")
    return GenderTypeOut(**result._mapping) if result else None

# Delete gender type
# Role: basetype_admin
async def delete_gender_type(gender_type_id: int) -> Optional[int]:
    query = "DELETE FROM gender_types WHERE id = :id RETURNING id"
    result = await database.fetch_one(query=query, values={"id": gender_type_id})
    logger.info(f"Deleted gender type: id={gender_type_id}")
    return result["id"] if result else None
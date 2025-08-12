from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.industry_type import IndustryTypeCreate, IndustryTypeUpdate, IndustryTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create industry type
# Role: basetype_admin
async def create_industry_type(industry_type: IndustryTypeCreate) -> Optional[IndustryTypeOut]:
    query = """
        INSERT INTO industry_types (naisc, description)
        VALUES (:naisc, :description)
        RETURNING id, naisc, description
    """
    values = {"naisc": industry_type.naisc, "description": industry_type.description}
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Created industry type: {industry_type.description}")
    return IndustryTypeOut(**result._mapping) if result else None

# Get industry type by ID
# Role: basetype_admin
async def get_industry_type(industry_type_id: int) -> Optional[IndustryTypeOut]:
    query = "SELECT id, naisc, description FROM industry_types WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": industry_type_id})
    logger.info(f"Retrieved industry type: id={industry_type_id}")
    return IndustryTypeOut(**result._mapping) if result else None

# Get all industry types
# Role: basetype_admin
async def get_all_industry_types() -> List[IndustryTypeOut]:
    query = "SELECT id, naisc, description FROM industry_types ORDER BY id ASC"
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} industry types")
    return [IndustryTypeOut(**result._mapping) for result in results]

# Update industry type
# Role: basetype_admin
async def update_industry_type(industry_type_id: int, industry_type: IndustryTypeUpdate) -> Optional[IndustryTypeOut]:
    query_parts = []
    values = {"id": industry_type_id}
    if industry_type.naisc is not None:
        query_parts.append("naisc = :naisc")
        values["naisc"] = industry_type.naisc
    if industry_type.description is not None:
        query_parts.append("description = :description")
        values["description"] = industry_type.description
    if not query_parts:
        logger.info(f"No fields to update for industry type id={industry_type_id}")
        return None
    query = f"""
        UPDATE industry_types
        SET {', '.join(query_parts)}
        WHERE id = :id
        RETURNING id, naisc, description
    """
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Updated industry type: id={industry_type_id}")
    return IndustryTypeOut(**result._mapping) if result else None

# Delete industry type
# Role: basetype_admin
async def delete_industry_type(industry_type_id: int) -> Optional[int]:
    query = "DELETE FROM industry_types WHERE id = :id RETURNING id"
    result = await database.fetch_one(query=query, values={"id": industry_type_id})
    logger.info(f"Deleted industry type: id={industry_type_id}")
    return result["id"] if result else None
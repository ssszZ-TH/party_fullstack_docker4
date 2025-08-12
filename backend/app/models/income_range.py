from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.income_range import IncomeRangeCreate, IncomeRangeUpdate, IncomeRangeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create income range
# Role: basetype_admin
async def create_income_range(income_range: IncomeRangeCreate) -> Optional[IncomeRangeOut]:
    query = """
        INSERT INTO income_ranges (description)
        VALUES (:description)
        RETURNING id, description
    """
    values = {"description": income_range.description}
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Created income range: {income_range.description}")
    return IncomeRangeOut(**result._mapping) if result else None

# Get income range by ID
# Role: basetype_admin
async def get_income_range(income_range_id: int) -> Optional[IncomeRangeOut]:
    query = "SELECT id, description FROM income_ranges WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": income_range_id})
    logger.info(f"Retrieved income range: id={income_range_id}")
    return IncomeRangeOut(**result._mapping) if result else None

# Get all income ranges
# Role: basetype_admin
async def get_all_income_ranges() -> List[IncomeRangeOut]:
    query = "SELECT id, description FROM income_ranges ORDER BY id ASC"
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} income ranges")
    return [IncomeRangeOut(**result._mapping) for result in results]

# Update income range
# Role: basetype_admin
async def update_income_range(income_range_id: int, income_range: IncomeRangeUpdate) -> Optional[IncomeRangeOut]:
    query_parts = []
    values = {"id": income_range_id}
    if income_range.description is not None:
        query_parts.append("description = :description")
        values["description"] = income_range.description
    if not query_parts:
        logger.info(f"No fields to update for income range id={income_range_id}")
        return None
    query = f"""
        UPDATE income_ranges
        SET {', '.join(query_parts)}
        WHERE id = :id
        RETURNING id, description
    """
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Updated income range: id={income_range_id}")
    return IncomeRangeOut(**result._mapping) if result else None

# Delete income range
# Role: basetype_admin
async def delete_income_range(income_range_id: int) -> Optional[int]:
    query = "DELETE FROM income_ranges WHERE id = :id RETURNING id"
    result = await database.fetch_one(query=query, values={"id": income_range_id})
    logger.info(f"Deleted income range: id={income_range_id}")
    return result["id"] if result else None
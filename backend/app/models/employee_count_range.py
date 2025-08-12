from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.employee_count_range import EmployeeCountRangeCreate, EmployeeCountRangeUpdate, EmployeeCountRangeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create employee count range
# Role: basetype_admin
async def create_employee_count_range(employee_count_range: EmployeeCountRangeCreate) -> Optional[EmployeeCountRangeOut]:
    query = """
        INSERT INTO employee_count_ranges (description)
        VALUES (:description)
        RETURNING id, description
    """
    values = {"description": employee_count_range.description}
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Created employee count range: {employee_count_range.description}")
    return EmployeeCountRangeOut(**result._mapping) if result else None

# Get employee count range by ID
# Role: basetype_admin
async def get_employee_count_range(employee_count_range_id: int) -> Optional[EmployeeCountRangeOut]:
    query = "SELECT id, description FROM employee_count_ranges WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": employee_count_range_id})
    logger.info(f"Retrieved employee count range: id={employee_count_range_id}")
    return EmployeeCountRangeOut(**result._mapping) if result else None

# Get all employee count ranges
# Role: basetype_admin
async def get_all_employee_count_ranges() -> List[EmployeeCountRangeOut]:
    query = "SELECT id, description FROM employee_count_ranges ORDER BY id ASC"
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} employee count ranges")
    return [EmployeeCountRangeOut(**result._mapping) for result in results]

# Update employee count range
# Role: basetype_admin
async def update_employee_count_range(employee_count_range_id: int, employee_count_range: EmployeeCountRangeUpdate) -> Optional[EmployeeCountRangeOut]:
    query_parts = []
    values = {"id": employee_count_range_id}
    if employee_count_range.description is not None:
        query_parts.append("description = :description")
        values["description"] = employee_count_range.description
    if not query_parts:
        logger.info(f"No fields to update for employee count range id={employee_count_range_id}")
        return None
    query = f"""
        UPDATE employee_count_ranges
        SET {', '.join(query_parts)}
        WHERE id = :id
        RETURNING id, description
    """
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Updated employee count range: id={employee_count_range_id}")
    return EmployeeCountRangeOut(**result._mapping) if result else None

# Delete employee count range
# Role: basetype_admin
async def delete_employee_count_range(employee_count_range_id: int) -> Optional[int]:
    query = "DELETE FROM employee_count_ranges WHERE id = :id RETURNING id"
    result = await database.fetch_one(query=query, values={"id": employee_count_range_id})
    logger.info(f"Deleted employee count range: id={employee_count_range_id}")
    return result["id"] if result else None
from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.organization_history import OrganizationHistoryOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get organization history by ID (organization_admin)
async def get_organization_history(history_id: int) -> Optional[OrganizationHistoryOut]:
    query = """
        SELECT id, organization_id, federal_tax_id, name_en, name_th, organization_type_id, industry_type_id, 
               employee_count_range_id, username, password, comment, action, action_at
        FROM organization_history WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": history_id})
    logger.info(f"Retrieved organization history: id={history_id}")
    return OrganizationHistoryOut(**result._mapping) if result else None

# Get all organization histories (organization_admin)
async def get_all_organization_histories() -> List[OrganizationHistoryOut]:
    query = """
        SELECT id, organization_id, federal_tax_id, name_en, name_th, organization_type_id, industry_type_id, 
               employee_count_range_id, username, password, comment, action, action_at
        FROM organization_history ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} organization histories")
    return [OrganizationHistoryOut(**result._mapping) for result in results]
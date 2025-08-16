from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.role_relationship_history import RoleRelationshipHistoryOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get role relationship history by ID (hr_admin, organization_admin)
async def get_role_relationship_history(history_id: int) -> Optional[RoleRelationshipHistoryOut]:
    query = """
        SELECT id, role_relationship_id, from_party_role_id, to_party_role_id, comment, relationship_type_id, 
               priority_type_id, role_relationship_status_type_id, action, action_at
        FROM role_relationship_history WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": history_id})
    logger.info(f"Retrieved role relationship history: id={history_id}")
    return RoleRelationshipHistoryOut(**result._mapping) if result else None

# Get all role relationship histories (hr_admin, organization_admin)
async def get_all_role_relationship_histories() -> List[RoleRelationshipHistoryOut]:
    query = """
        SELECT id, role_relationship_id, from_party_role_id, to_party_role_id, comment, relationship_type_id, 
               priority_type_id, role_relationship_status_type_id, action, action_at
        FROM role_relationship_history ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} role relationship histories")
    return [RoleRelationshipHistoryOut(**result._mapping) for result in results]
from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.party_role_history import PartyRoleHistoryOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get party role history by ID (hr_admin, organization_admin)
async def get_party_role_history(history_id: int) -> Optional[PartyRoleHistoryOut]:
    query = """
        SELECT id, party_role_id, note, party_id, role_type_id, action, action_at
        FROM party_role_history WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": history_id})
    logger.info(f"Retrieved party role history: id={history_id}")
    return PartyRoleHistoryOut(**result._mapping) if result else None

# Get all party role histories (hr_admin, organization_admin)
async def get_all_party_role_histories() -> List[PartyRoleHistoryOut]:
    query = """
        SELECT id, party_role_id, note, party_id, role_type_id, action, action_at
        FROM party_role_history ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} party role histories")
    return [PartyRoleHistoryOut(**result._mapping) for result in results]
from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.communication_event_history import CommunicationEventHistoryOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get communication event history by ID (hr_admin, organization_admin)
async def get_communication_event_history(history_id: int) -> Optional[CommunicationEventHistoryOut]:
    query = """
        SELECT id, communication_event_id, note, role_relationship_id, contact_mechanism_type_id, 
               communication_event_status_type_id, action, action_at
        FROM communication_event_history WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": history_id})
    logger.info(f"Retrieved communication event history: id={history_id}")
    return CommunicationEventHistoryOut(**result._mapping) if result else None

# Get all communication event histories (hr_admin, organization_admin)
async def get_all_communication_event_histories() -> List[CommunicationEventHistoryOut]:
    query = """
        SELECT id, communication_event_id, note, role_relationship_id, contact_mechanism_type_id, 
               communication_event_status_type_id, action, action_at
        FROM communication_event_history ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} communication event histories")
    return [CommunicationEventHistoryOut(**result._mapping) for result in results]
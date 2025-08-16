from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.communication_event_purpose_history import CommunicationEventPurposeHistoryOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get communication event purpose history by ID (hr_admin, organization_admin)
async def get_communication_event_purpose_history(history_id: int) -> Optional[CommunicationEventPurposeHistoryOut]:
    query = """
        SELECT id, communication_event_purpose_id, note, communication_event_id, 
               communication_event_purpose_type_id, action, action_at
        FROM communication_event_purpose_history WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": history_id})
    logger.info(f"Retrieved communication event purpose history: id={history_id}")
    return CommunicationEventPurposeHistoryOut(**result._mapping) if result else None

# Get all communication event purpose histories (hr_admin, organization_admin)
async def get_all_communication_event_purpose_histories() -> List[CommunicationEventPurposeHistoryOut]:
    query = """
        SELECT id, communication_event_purpose_id, note, communication_event_id, 
               communication_event_purpose_type_id, action, action_at
        FROM communication_event_purpose_history ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} communication event purpose histories")
    return [CommunicationEventPurposeHistoryOut(**result._mapping) for result in results]
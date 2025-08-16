from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.passport_history import PassportHistoryOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get passport history by ID (hr_admin)
async def get_passport_history(history_id: int) -> Optional[PassportHistoryOut]:
    query = """
        SELECT id, passport_id, passport_id_number, issue_date, expire_date, person_id, action, action_at
        FROM passport_history WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": history_id})
    logger.info(f"Retrieved passport history: id={history_id}")
    return PassportHistoryOut(**result._mapping) if result else None

# Get all passport histories (hr_admin)
async def get_all_passport_histories() -> List[PassportHistoryOut]:
    query = """
        SELECT id, passport_id, passport_id_number, issue_date, expire_date, person_id, action, action_at
        FROM passport_history ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} passport histories")
    return [PassportHistoryOut(**result._mapping) for result in results]
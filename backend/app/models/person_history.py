from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.person_history import PersonHistoryOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get person history by ID (hr_admin)
async def get_person_history(history_id: int) -> Optional[PersonHistoryOut]:
    query = """
        SELECT id, person_id, username, password, personal_id_number, first_name, middle_name, last_name, 
               nick_name, birth_date, gender_type_id, marital_status_type_id, country_id, height, weight, 
               ethnicity_type_id, income_range_id, comment, action, action_at
        FROM person_history WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": history_id})
    logger.info(f"Retrieved person history: id={history_id}")
    return PersonHistoryOut(**result._mapping) if result else None

# Get all person histories (hr_admin)
async def get_all_person_histories() -> List[PersonHistoryOut]:
    query = """
        SELECT id, person_id, username, password, personal_id_number, first_name, middle_name, last_name, 
               nick_name, birth_date, gender_type_id, marital_status_type_id, country_id, height, weight, 
               ethnicity_type_id, income_range_id, comment, action, action_at
        FROM person_history ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} person histories")
    return [PersonHistoryOut(**result._mapping) for result in results]
from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.communication_event_status_type import CommunicationEventStatusTypeCreate, CommunicationEventStatusTypeUpdate, CommunicationEventStatusTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a new communication event status type
async def create_communication_event_status_type(communication_event_status_type: CommunicationEventStatusTypeCreate) -> Optional[CommunicationEventStatusTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO communication_event_status_types (description)
                VALUES (:description)
                RETURNING id, description
            """
            values = {"description": communication_event_status_type.description}
            result = await database.fetch_one(query=query, values=values)
            logger.info(f"Created communication event status type: {communication_event_status_type.description}")
            return CommunicationEventStatusTypeOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error creating communication event status type: {str(e)}")
            raise

# Get communication event status type by ID
async def get_communication_event_status_type(communication_event_status_type_id: int) -> Optional[CommunicationEventStatusTypeOut]:
    query = """
        SELECT id, description 
        FROM communication_event_status_types WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": communication_event_status_type_id})
    logger.info(f"Retrieved communication event status type: id={communication_event_status_type_id}")
    return CommunicationEventStatusTypeOut(**result._mapping) if result else None

# Get all communication event status types
async def get_all_communication_event_status_types() -> List[CommunicationEventStatusTypeOut]:
    query = """
        SELECT id, description 
        FROM communication_event_status_types ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} communication event status types")
    return [CommunicationEventStatusTypeOut(**result._mapping) for result in results]

# Update communication event status type
async def update_communication_event_status_type(communication_event_status_type_id: int, communication_event_status_type: CommunicationEventStatusTypeUpdate) -> Optional[CommunicationEventStatusTypeOut]:
    async with database.transaction():
        try:
            values = {"id": communication_event_status_type_id}
            query_parts = []

            if communication_event_status_type.description is not None:
                query_parts.append("description = :description")
                values["description"] = communication_event_status_type.description

            if not query_parts:
                logger.info(f"No fields to update for communication event status type id={communication_event_status_type_id}")
                return None

            query = f"""
                UPDATE communication_event_status_types
                SET {', '.join(query_parts)}
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values=values)
            logger.info(f"Updated communication event status type: id={communication_event_status_type_id}")
            return CommunicationEventStatusTypeOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error updating communication event status type: {str(e)}")
            raise

# Delete communication event status type
async def delete_communication_event_status_type(communication_event_status_type_id: int) -> Optional[int]:
    async with database.transaction():
        try:
            query = "DELETE FROM communication_event_status_types WHERE id = :id RETURNING id"
            result = await database.fetch_one(query=query, values={"id": communication_event_status_type_id})
            logger.info(f"Deleted communication event status type: id={communication_event_status_type_id}")
            return result["id"] if result else None
        except Exception as e:
            logger.error(f"Error deleting communication event status type: {str(e)}")
            raise
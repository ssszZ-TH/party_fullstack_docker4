from app.config.database import database
import logging
from typing import Optional, List
from datetime import datetime
from app.schemas.communication_event_purpose_type import CommunicationEventPurposeTypeCreate, CommunicationEventPurposeTypeUpdate, CommunicationEventPurposeTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create communication event purpose type
async def create_communication_event_purpose_type(communication_event_purpose_type: CommunicationEventPurposeTypeCreate) -> Optional[CommunicationEventPurposeTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO communication_event_purpose_types (description, created_at)
                VALUES (:description, :created_at)
                RETURNING id, description, created_at, updated_at
            """
            values = {"description": communication_event_purpose_type.description, "created_at": datetime.utcnow()}
            result = await database.fetch_one(query=query, values=values)
            logger.info(f"Created communication event purpose type: {communication_event_purpose_type.description}")
            return CommunicationEventPurposeTypeOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error creating communication event purpose type: {str(e)}")
            raise

# Get communication event purpose type by ID
async def get_communication_event_purpose_type(communication_event_purpose_type_id: int) -> Optional[CommunicationEventPurposeTypeOut]:
    query = """
        SELECT id, description, created_at, updated_at 
        FROM communication_event_purpose_types WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": communication_event_purpose_type_id})
    logger.info(f"Retrieved communication event purpose type: id={communication_event_purpose_type_id}")
    return CommunicationEventPurposeTypeOut(**result._mapping) if result else None

# Get all communication event purpose types
async def get_all_communication_event_purpose_types() -> List[CommunicationEventPurposeTypeOut]:
    query = """
        SELECT id, description, created_at, updated_at 
        FROM communication_event_purpose_types ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} communication event purpose types")
    return [CommunicationEventPurposeTypeOut(**result._mapping) for result in results]

# Update communication event purpose type
async def update_communication_event_purpose_type(communication_event_purpose_type_id: int, communication_event_purpose_type: CommunicationEventPurposeTypeUpdate) -> Optional[CommunicationEventPurposeTypeOut]:
    async with database.transaction():
        try:
            values = {"id": communication_event_purpose_type_id, "updated_at": datetime.utcnow()}
            query_parts = []

            if communication_event_purpose_type.description is not None:
                query_parts.append("description = :description")
                values["description"] = communication_event_purpose_type.description

            if not query_parts:
                logger.info(f"No fields to update for communication event purpose type id={communication_event_purpose_type_id}")
                return None

            query = f"""
                UPDATE communication_event_purpose_types
                SET {', '.join(query_parts)}, updated_at = :updated_at
                WHERE id = :id
                RETURNING id, description, created_at, updated_at
            """
            result = await database.fetch_one(query=query, values=values)
            logger.info(f"Updated communication event purpose type: id={communication_event_purpose_type_id}")
            return CommunicationEventPurposeTypeOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error updating communication event purpose type: {str(e)}")
            raise

# Delete communication event purpose type
async def delete_communication_event_purpose_type(communication_event_purpose_type_id: int) -> Optional[int]:
    async with database.transaction():
        try:
            query = "DELETE FROM communication_event_purpose_types WHERE id = :id RETURNING id"
            result = await database.fetch_one(query=query, values={"id": communication_event_purpose_type_id})
            logger.info(f"Deleted communication event purpose type: id={communication_event_purpose_type_id}")
            return result["id"] if result else None
        except Exception as e:
            logger.error(f"Error deleting communication event purpose type: {str(e)}")
            raise
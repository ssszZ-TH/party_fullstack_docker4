from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.communication_event import CommunicationEventCreate, CommunicationEventUpdate, CommunicationEventOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a new communication event (organization_user, person_user)
async def create_communication_event(communication_event: CommunicationEventCreate, party_id: int) -> Optional[CommunicationEventOut]:
    async with database.transaction():
        try:
            # Verify role_relationship_id is accessible by party_id
            query_check = """
                SELECT rr.id FROM role_relationship rr
                JOIN party_role pr ON pr.id IN (rr.from_party_role_id, rr.to_party_role_id)
                WHERE rr.id = :role_relationship_id AND pr.party_id = :party_id
            """
            result_check = await database.fetch_one(query=query_check, values={
                "role_relationship_id": communication_event.role_relationship_id,
                "party_id": party_id
            })
            if not result_check:
                logger.warning(f"Invalid role_relationship_id for party_id={party_id}")
                return None

            query = """
                INSERT INTO communication_event (note, role_relationship_id, contact_mechanism_type_id, communication_event_status_type_id)
                VALUES (:note, :role_relationship_id, :contact_mechanism_type_id, :communication_event_status_type_id)
                RETURNING id, note, role_relationship_id, contact_mechanism_type_id, communication_event_status_type_id, created_at, updated_at
            """
            values = communication_event.dict()
            result = await database.fetch_one(query=query, values=values)
            if not result:
                logger.warning(f"Failed to create communication event")
                return None

            # Insert into communication_event_history
            history_query = """
                INSERT INTO communication_event_history (communication_event_id, note, role_relationship_id, contact_mechanism_type_id, communication_event_status_type_id, action)
                VALUES (:communication_event_id, :note, :role_relationship_id, :contact_mechanism_type_id, :communication_event_status_type_id, 'CREATE')
            """
            history_values = {
                "communication_event_id": result["id"],
                **values
            }
            await database.execute(query=history_query, values=history_values)

            logger.info(f"Created communication event: id={result['id']}")
            return CommunicationEventOut(**result._mapping)
        except Exception as e:
            logger.error(f"Error creating communication event: {str(e)}")
            raise

# Get communication event by ID (organization_user, person_user)
async def get_communication_event(communication_event_id: int, party_id: int) -> Optional[CommunicationEventOut]:
    query = """
        SELECT ce.id, ce.note, ce.role_relationship_id, ce.contact_mechanism_type_id, ce.communication_event_status_type_id, ce.created_at, ce.updated_at
        FROM communication_event ce
        JOIN role_relationship rr ON rr.id = ce.role_relationship_id
        JOIN party_role pr ON pr.id IN (rr.from_party_role_id, rr.to_party_role_id)
        WHERE ce.id = :id AND pr.party_id = :party_id
    """
    result = await database.fetch_one(query=query, values={"id": communication_event_id, "party_id": party_id})
    logger.info(f"Retrieved communication event: id={communication_event_id} for party_id={party_id}")
    return CommunicationEventOut(**result._mapping) if result else None

# Get all communication events for a party (organization_user, person_user)
async def get_all_communication_events(party_id: int) -> List[CommunicationEventOut]:
    query = """
        SELECT ce.id, ce.note, ce.role_relationship_id, ce.contact_mechanism_type_id, ce.communication_event_status_type_id, ce.created_at, ce.updated_at
        FROM communication_event ce
        JOIN role_relationship rr ON rr.id = ce.role_relationship_id
        JOIN party_role pr ON pr.id IN (rr.from_party_role_id, rr.to_party_role_id)
        WHERE pr.party_id = :party_id
        ORDER BY ce.id ASC
    """
    results = await database.fetch_all(query=query, values={"party_id": party_id})
    logger.info(f"Retrieved {len(results)} communication events for party_id={party_id}")
    return [CommunicationEventOut(**result._mapping) for result in results]

# Update communication event (organization_user, person_user)
async def update_communication_event(communication_event_id: int, communication_event: CommunicationEventUpdate, party_id: int) -> Optional[CommunicationEventOut]:
    async with database.transaction():
        try:
            # Get current communication event for history
            current_communication_event = await get_communication_event(communication_event_id, party_id)
            if not current_communication_event:
                logger.warning(f"Communication event not found for update: id={communication_event_id}, party_id={party_id}")
                return None

            values = {"id": communication_event_id}
            query_parts = []

            if communication_event.note is not None:
                query_parts.append("note = :note")
                values["note"] = communication_event.note
            if communication_event.role_relationship_id is not None:
                query_parts.append("role_relationship_id = :role_relationship_id")
                values["role_relationship_id"] = communication_event.role_relationship_id
            if communication_event.contact_mechanism_type_id is not None:
                query_parts.append("contact_mechanism_type_id = :contact_mechanism_type_id")
                values["contact_mechanism_type_id"] = communication_event.contact_mechanism_type_id
            if communication_event.communication_event_status_type_id is not None:
                query_parts.append("communication_event_status_type_id = :communication_event_status_type_id")
                values["communication_event_status_type_id"] = communication_event.communication_event_status_type_id
            if query_parts:
                query_parts.append("updated_at = CURRENT_TIMESTAMP")

            if not query_parts:
                logger.info(f"No fields to update for communication event id={communication_event_id}")
                return None

            query = f"""
                UPDATE communication_event
                SET {', '.join(query_parts)}
                WHERE id = :id
                RETURNING id, note, role_relationship_id, contact_mechanism_type_id, communication_event_status_type_id, created_at, updated_at
            """
            result = await database.fetch_one(query=query, values=values)
            if not result:
                logger.warning(f"Communication event not found or no changes made: id={communication_event_id}")
                return None

            # Verify updated record is accessible by party_id
            updated_communication_event = await get_communication_event(communication_event_id, party_id)
            if not updated_communication_event:
                logger.warning(f"Updated communication event not accessible: id={communication_event_id}, party_id={party_id}")
                return None

            # Insert into communication_event_history
            history_query = """
                INSERT INTO communication_event_history (communication_event_id, note, role_relationship_id, contact_mechanism_type_id, communication_event_status_type_id, action)
                VALUES (:communication_event_id, :note, :role_relationship_id, :contact_mechanism_type_id, :communication_event_status_type_id, 'UPDATE')
            """
            history_values = {
                "communication_event_id": communication_event_id,
                "note": values.get("note", current_communication_event.note),
                "role_relationship_id": values.get("role_relationship_id", current_communication_event.role_relationship_id),
                "contact_mechanism_type_id": values.get("contact_mechanism_type_id", current_communication_event.contact_mechanism_type_id),
                "communication_event_status_type_id": values.get("communication_event_status_type_id", current_communication_event.communication_event_status_type_id)
            }
            await database.execute(query=history_query, values=history_values)

            logger.info(f"Updated communication event: id={communication_event_id}")
            return CommunicationEventOut(**result._mapping)
        except Exception as e:
            logger.error(f"Error updating communication event: {str(e)}")
            raise

# Delete communication event (organization_user, person_user)
async def delete_communication_event(communication_event_id: int, party_id: int) -> Optional[int]:
    async with database.transaction():
        try:
            # Get current communication event for history
            current_communication_event = await get_communication_event(communication_event_id, party_id)
            if not current_communication_event:
                logger.warning(f"Communication event not found for deletion: id={communication_event_id}, party_id={party_id}")
                return None

            # Insert into communication_event_history
            history_query = """
                INSERT INTO communication_event_history (communication_event_id, note, role_relationship_id, contact_mechanism_type_id, communication_event_status_type_id, action)
                VALUES (:communication_event_id, :note, :role_relationship_id, :contact_mechanism_type_id, :communication_event_status_type_id, 'DELETE')
            """
            history_values = {
                "communication_event_id": communication_event_id,
                "note": current_communication_event.note,
                "role_relationship_id": current_communication_event.role_relationship_id,
                "contact_mechanism_type_id": current_communication_event.contact_mechanism_type_id,
                "communication_event_status_type_id": current_communication_event.communication_event_status_type_id
            }
            await database.execute(query=history_query, values=history_values)

            # Delete communication event
            query = "DELETE FROM communication_event WHERE id = :id RETURNING id"
            result = await database.fetch_one(query=query, values={"id": communication_event_id})
            logger.info(f"Deleted communication event: id={communication_event_id}")
            return result["id"] if result else None
        except Exception as e:
            logger.error(f"Error deleting communication event: {str(e)}")
            raise
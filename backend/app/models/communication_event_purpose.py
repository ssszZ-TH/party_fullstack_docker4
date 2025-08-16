from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.communication_event_purpose import CommunicationEventPurposeCreate, CommunicationEventPurposeUpdate, CommunicationEventPurposeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a new communication event purpose (organization_user, person_user)
async def create_communication_event_purpose(communication_event_purpose: CommunicationEventPurposeCreate, party_id: int) -> Optional[CommunicationEventPurposeOut]:
    async with database.transaction():
        try:
            # Verify communication_event_id is accessible by party_id
            query_check = """
                SELECT ce.id FROM communication_event ce
                JOIN role_relationship rr ON rr.id = ce.role_relationship_id
                JOIN party_role pr ON pr.id IN (rr.from_party_role_id, rr.to_party_role_id)
                WHERE ce.id = :communication_event_id AND pr.party_id = :party_id
            """
            result_check = await database.fetch_one(query=query_check, values={
                "communication_event_id": communication_event_purpose.communication_event_id,
                "party_id": party_id
            })
            if not result_check:
                logger.warning(f"Invalid communication_event_id for party_id={party_id}")
                return None

            query = """
                INSERT INTO communication_event_purpose (note, communication_event_id, communication_event_purpose_type_id)
                VALUES (:note, :communication_event_id, :communication_event_purpose_type_id)
                RETURNING id, note, communication_event_id, communication_event_purpose_type_id, created_at, updated_at
            """
            values = communication_event_purpose.dict()
            result = await database.fetch_one(query=query, values=values)
            if not result:
                logger.warning(f"Failed to create communication event purpose")
                return None

            # Insert into communication_event_purpose_history
            history_query = """
                INSERT INTO communication_event_purpose_history (communication_event_purpose_id, note, communication_event_id, communication_event_purpose_type_id, action)
                VALUES (:communication_event_purpose_id, :note, :communication_event_id, :communication_event_purpose_type_id, 'CREATE')
            """
            history_values = {
                "communication_event_purpose_id": result["id"],
                **values
            }
            await database.execute(query=history_query, values=history_values)

            logger.info(f"Created communication event purpose: id={result['id']}")
            return CommunicationEventPurposeOut(**result._mapping)
        except Exception as e:
            logger.error(f"Error creating communication event purpose: {str(e)}")
            raise

# Get communication event purpose by ID (organization_user, person_user)
async def get_communication_event_purpose(communication_event_purpose_id: int, party_id: int) -> Optional[CommunicationEventPurposeOut]:
    query = """
        SELECT cep.id, cep.note, cep.communication_event_id, cep.communication_event_purpose_type_id, cep.created_at, cep.updated_at
        FROM communication_event_purpose cep
        JOIN communication_event ce ON ce.id = cep.communication_event_id
        JOIN role_relationship rr ON rr.id = ce.role_relationship_id
        JOIN party_role pr ON pr.id IN (rr.from_party_role_id, rr.to_party_role_id)
        WHERE cep.id = :id AND pr.party_id = :party_id
    """
    result = await database.fetch_one(query=query, values={"id": communication_event_purpose_id, "party_id": party_id})
    logger.info(f"Retrieved communication event purpose: id={communication_event_purpose_id} for party_id={party_id}")
    return CommunicationEventPurposeOut(**result._mapping) if result else None

# Get all communication event purposes for a party (organization_user, person_user)
async def get_all_communication_event_purposes(party_id: int) -> List[CommunicationEventPurposeOut]:
    query = """
        SELECT cep.id, cep.note, cep.communication_event_id, cep.communication_event_purpose_type_id, cep.created_at, cep.updated_at
        FROM communication_event_purpose cep
        JOIN communication_event ce ON ce.id = cep.communication_event_id
        JOIN role_relationship rr ON rr.id = ce.role_relationship_id
        JOIN party_role pr ON pr.id IN (rr.from_party_role_id, rr.to_party_role_id)
        WHERE pr.party_id = :party_id
        ORDER BY cep.id ASC
    """
    results = await database.fetch_all(query=query, values={"party_id": party_id})
    logger.info(f"Retrieved {len(results)} communication event purposes for party_id={party_id}")
    return [CommunicationEventPurposeOut(**result._mapping) for result in results]

# Update communication event purpose (organization_user, person_user)
async def update_communication_event_purpose(communication_event_purpose_id: int, communication_event_purpose: CommunicationEventPurposeUpdate, party_id: int) -> Optional[CommunicationEventPurposeOut]:
    async with database.transaction():
        try:
            # Get current communication event purpose for history
            current_communication_event_purpose = await get_communication_event_purpose(communication_event_purpose_id, party_id)
            if not current_communication_event_purpose:
                logger.warning(f"Communication event purpose not found for update: id={communication_event_purpose_id}, party_id={party_id}")
                return None

            values = {"id": communication_event_purpose_id}
            query_parts = []

            if communication_event_purpose.note is not None:
                query_parts.append("note = :note")
                values["note"] = communication_event_purpose.note
            if communication_event_purpose.communication_event_id is not None:
                query_parts.append("communication_event_id = :communication_event_id")
                values["communication_event_id"] = communication_event_purpose.communication_event_id
            if communication_event_purpose.communication_event_purpose_type_id is not None:
                query_parts.append("communication_event_purpose_type_id = :communication_event_purpose_type_id")
                values["communication_event_purpose_type_id"] = communication_event_purpose.communication_event_purpose_type_id
            if query_parts:
                query_parts.append("updated_at = CURRENT_TIMESTAMP")

            if not query_parts:
                logger.info(f"No fields to update for communication event purpose id={communication_event_purpose_id}")
                return None

            query = f"""
                UPDATE communication_event_purpose
                SET {', '.join(query_parts)}
                WHERE id = :id
                RETURNING id, note, communication_event_id, communication_event_purpose_type_id, created_at, updated_at
            """
            result = await database.fetch_one(query=query, values=values)
            if not result:
                logger.warning(f"Communication event purpose not found or no changes made: id={communication_event_purpose_id}")
                return None

            # Verify updated record is accessible by party_id
            updated_communication_event_purpose = await get_communication_event_purpose(communication_event_purpose_id, party_id)
            if not updated_communication_event_purpose:
                logger.warning(f"Updated communication event purpose not accessible: id={communication_event_purpose_id}, party_id={party_id}")
                return None

            # Insert into communication_event_purpose_history
            history_query = """
                INSERT INTO communication_event_purpose_history (communication_event_purpose_id, note, communication_event_id, communication_event_purpose_type_id, action)
                VALUES (:communication_event_purpose_id, :note, :communication_event_id, :communication_event_purpose_type_id, 'UPDATE')
            """
            history_values = {
                "communication_event_purpose_id": communication_event_purpose_id,
                "note": values.get("note", current_communication_event_purpose.note),
                "communication_event_id": values.get("communication_event_id", current_communication_event_purpose.communication_event_id),
                "communication_event_purpose_type_id": values.get("communication_event_purpose_type_id", current_communication_event_purpose.communication_event_purpose_type_id)
            }
            await database.execute(query=history_query, values=history_values)

            logger.info(f"Updated communication event purpose: id={communication_event_purpose_id}")
            return CommunicationEventPurposeOut(**result._mapping)
        except Exception as e:
            logger.error(f"Error updating communication event purpose: {str(e)}")
            raise

# Delete communication event purpose (organization_user, person_user)
async def delete_communication_event_purpose(communication_event_purpose_id: int, party_id: int) -> Optional[int]:
    async with database.transaction():
        try:
            # Get current communication event purpose for history
            current_communication_event_purpose = await get_communication_event_purpose(communication_event_purpose_id, party_id)
            if not current_communication_event_purpose:
                logger.warning(f"Communication event purpose not found for deletion: id={communication_event_purpose_id}, party_id={party_id}")
                return None

            # Insert into communication_event_purpose_history
            history_query = """
                INSERT INTO communication_event_purpose_history (communication_event_purpose_id, note, communication_event_id, communication_event_purpose_type_id, action)
                VALUES (:communication_event_purpose_id, :note, :communication_event_id, :communication_event_purpose_type_id, 'DELETE')
            """
            history_values = {
                "communication_event_purpose_id": communication_event_purpose_id,
                "note": current_communication_event_purpose.note,
                "communication_event_id": current_communication_event_purpose.communication_event_id,
                "communication_event_purpose_type_id": current_communication_event_purpose.communication_event_purpose_type_id
            }
            await database.execute(query=history_query, values=history_values)

            # Delete communication event purpose
            query = "DELETE FROM communication_event_purpose WHERE id = :id RETURNING id"
            result = await database.fetch_one(query=query, values={"id": communication_event_purpose_id})
            logger.info(f"Deleted communication event purpose: id={communication_event_purpose_id}")
            return result["id"] if result else None
        except Exception as e:
            logger.error(f"Error deleting communication event purpose: {str(e)}")
            raise
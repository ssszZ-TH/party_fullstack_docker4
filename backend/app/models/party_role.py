from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.party_role import PartyRoleCreate, PartyRoleUpdate, PartyRoleOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a new party role (organization_user, person_user)
async def create_party_role(party_role: PartyRoleCreate, party_id: int) -> Optional[PartyRoleOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO party_role (note, party_id, role_type_id)
                VALUES (:note, :party_id, :role_type_id)
                RETURNING id, note, party_id, role_type_id, created_at, updated_at
            """
            values = party_role.dict()
            values["party_id"] = party_id
            result = await database.fetch_one(query=query, values=values)
            if not result:
                logger.warning(f"Failed to create party role for party_id={party_id}")
                return None

            # Insert into party_role_history
            history_query = """
                INSERT INTO party_role_history (party_role_id, note, party_id, role_type_id, action)
                VALUES (:party_role_id, :note, :party_id, :role_type_id, 'CREATE')
            """
            history_values = {
                "party_role_id": result["id"],
                "note": party_role.note,
                "party_id": party_id,
                "role_type_id": party_role.role_type_id
            }
            await database.execute(query=history_query, values=history_values)

            logger.info(f"Created party role: id={result['id']} for party_id={party_id}")
            return PartyRoleOut(**result._mapping)
        except Exception as e:
            logger.error(f"Error creating party role: {str(e)}")
            raise

# Get party role by ID (organization_user, person_user)
async def get_party_role(party_role_id: int, party_id: int) -> Optional[PartyRoleOut]:
    query = """
        SELECT id, note, party_id, role_type_id, created_at, updated_at
        FROM party_role WHERE id = :id AND party_id = :party_id
    """
    result = await database.fetch_one(query=query, values={"id": party_role_id, "party_id": party_id})
    logger.info(f"Retrieved party role: id={party_role_id} for party_id={party_id}")
    return PartyRoleOut(**result._mapping) if result else None

# Get all party roles for a party (organization_user, person_user)
async def get_all_party_roles(party_id: int) -> List[PartyRoleOut]:
    query = """
        SELECT id, note, party_id, role_type_id, created_at, updated_at
        FROM party_role WHERE party_id = :party_id ORDER BY id ASC
    """
    results = await database.fetch_all(query=query, values={"party_id": party_id})
    logger.info(f"Retrieved {len(results)} party roles for party_id={party_id}")
    return [PartyRoleOut(**result._mapping) for result in results]

# Update party role (organization_user, person_user)
async def update_party_role(party_role_id: int, party_role: PartyRoleUpdate, party_id: int) -> Optional[PartyRoleOut]:
    async with database.transaction():
        try:
            # Get current party role for history
            current_party_role = await get_party_role(party_role_id, party_id)
            if not current_party_role:
                logger.warning(f"Party role not found for update: id={party_role_id}, party_id={party_id}")
                return None

            values = {"id": party_role_id, "party_id": party_id}
            query_parts = []

            if party_role.note is not None:
                query_parts.append("note = :note")
                values["note"] = party_role.note
            if party_role.role_type_id is not None:
                query_parts.append("role_type_id = :role_type_id")
                values["role_type_id"] = party_role.role_type_id
            if query_parts:
                query_parts.append("updated_at = CURRENT_TIMESTAMP")

            if not query_parts:
                logger.info(f"No fields to update for party role id={party_role_id}")
                return None

            query = f"""
                UPDATE party_role
                SET {', '.join(query_parts)}
                WHERE id = :id AND party_id = :party_id
                RETURNING id, note, party_id, role_type_id, created_at, updated_at
            """
            result = await database.fetch_one(query=query, values=values)
            if not result:
                logger.warning(f"Party role not found or no changes made: id={party_role_id}, party_id={party_id}")
                return None

            # Insert into party_role_history
            history_query = """
                INSERT INTO party_role_history (party_role_id, note, party_id, role_type_id, action)
                VALUES (:party_role_id, :note, :party_id, :role_type_id, 'UPDATE')
            """
            history_values = {
                "party_role_id": party_role_id,
                "note": values.get("note", current_party_role.note),
                "party_id": party_id,
                "role_type_id": values.get("role_type_id", current_party_role.role_type_id)
            }
            await database.execute(query=history_query, values=history_values)

            logger.info(f"Updated party role: id={party_role_id}")
            return PartyRoleOut(**result._mapping)
        except Exception as e:
            logger.error(f"Error updating party role: {str(e)}")
            raise

# Delete party role (organization_user, person_user)
async def delete_party_role(party_role_id: int, party_id: int) -> Optional[int]:
    async with database.transaction():
        try:
            # Get current party role for history
            current_party_role = await get_party_role(party_role_id, party_id)
            if not current_party_role:
                logger.warning(f"Party role not found for deletion: id={party_role_id}, party_id={party_id}")
                return None

            # Insert into party_role_history
            history_query = """
                INSERT INTO party_role_history (party_role_id, note, party_id, role_type_id, action)
                VALUES (:party_role_id, :note, :party_id, :role_type_id, 'DELETE')
            """
            history_values = {
                "party_role_id": party_role_id,
                "note": current_party_role.note,
                "party_id": party_id,
                "role_type_id": current_party_role.role_type_id
            }
            await database.execute(query=history_query, values=history_values)

            # Delete party role
            query = "DELETE FROM party_role WHERE id = :id AND party_id = :party_id RETURNING id"
            result = await database.fetch_one(query=query, values={"id": party_role_id, "party_id": party_id})
            logger.info(f"Deleted party role: id={party_role_id}")
            return result["id"] if result else None
        except Exception as e:
            logger.error(f"Error deleting party role: {str(e)}")
            raise
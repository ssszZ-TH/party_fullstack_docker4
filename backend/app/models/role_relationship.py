from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.role_relationship import RoleRelationshipCreate, RoleRelationshipUpdate, RoleRelationshipOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a new role relationship (organization_user, person_user)
async def create_role_relationship(role_relationship: RoleRelationshipCreate, party_id: str) -> Optional[RoleRelationshipOut]:
    async with database.transaction():
        try:
            # Convert party_id to integer
            party_id_int = int(party_id)
            # Verify party_id has a corresponding party_role
            query_check = """
                SELECT id FROM party_role WHERE party_id = :party_id
            """
            result_check = await database.fetch_one(query=query_check, values={"party_id": party_id_int})
            if not result_check:
                logger.warning(f"No party_role found for party_id={party_id_int}")
                return None
            from_party_role_id = result_check["id"]

            query = """
                INSERT INTO role_relationship (from_party_role_id, to_party_role_id, comment, relationship_type_id, priority_type_id, role_relationship_status_type_id)
                VALUES (:from_party_role_id, :to_party_role_id, :comment, :relationship_type_id, :priority_type_id, :role_relationship_status_type_id)
                RETURNING id, from_party_role_id, to_party_role_id, comment, relationship_type_id, priority_type_id, role_relationship_status_type_id, created_at, updated_at
            """
            values = role_relationship.dict()
            values["from_party_role_id"] = from_party_role_id
            result = await database.fetch_one(query=query, values=values)
            if not result:
                logger.warning(f"Failed to create role relationship")
                return None

            # Insert into role_relationship_history
            history_query = """
                INSERT INTO role_relationship_history (role_relationship_id, from_party_role_id, to_party_role_id, comment, relationship_type_id, priority_type_id, role_relationship_status_type_id, action)
                VALUES (:role_relationship_id, :from_party_role_id, :to_party_role_id, :comment, :relationship_type_id, :priority_type_id, :role_relationship_status_type_id, 'CREATE')
            """
            history_values = {
                "role_relationship_id": result["id"],
                **values
            }
            await database.execute(query=history_query, values=history_values)

            logger.info(f"Created role relationship: id={result['id']}")
            return RoleRelationshipOut(**result._mapping)
        except ValueError as e:
            logger.error(f"Invalid party_id format: {str(e)}")
            raise ValueError("Invalid party_id format")
        except Exception as e:
            logger.error(f"Error creating role relationship: {str(e)}")
            raise

# Get role relationship by ID (organization_user, person_user)
async def get_role_relationship(role_relationship_id: int, party_id: str) -> Optional[RoleRelationshipOut]:
    party_id_int = int(party_id)
    query = """
        SELECT rr.id, rr.from_party_role_id, rr.to_party_role_id, rr.comment, rr.relationship_type_id, rr.priority_type_id, rr.role_relationship_status_type_id, rr.created_at, rr.updated_at
        FROM role_relationship rr
        JOIN party_role pr ON pr.id IN (rr.from_party_role_id, rr.to_party_role_id)
        WHERE rr.id = :id AND pr.party_id = :party_id
    """
    result = await database.fetch_one(query=query, values={"id": role_relationship_id, "party_id": party_id_int})
    logger.info(f"Retrieved role relationship: id={role_relationship_id} for party_id={party_id_int}")
    return RoleRelationshipOut(**result._mapping) if result else None

# Get all role relationships for a party (organization_user, person_user)
async def get_all_role_relationships(party_id: str) -> List[RoleRelationshipOut]:
    party_id_int = int(party_id)
    query = """
        SELECT rr.id, rr.from_party_role_id, rr.to_party_role_id, rr.comment, rr.relationship_type_id, rr.priority_type_id, rr.role_relationship_status_type_id, rr.created_at, rr.updated_at
        FROM role_relationship rr
        JOIN party_role pr ON pr.id IN (rr.from_party_role_id, rr.to_party_role_id)
        WHERE pr.party_id = :party_id
        ORDER BY rr.id ASC
    """
    results = await database.fetch_all(query=query, values={"party_id": party_id_int})
    logger.info(f"Retrieved {len(results)} role relationships for party_id={party_id_int}")
    return [RoleRelationshipOut(**result._mapping) for result in results]

# Update role relationship (organization_user, person_user)
async def update_role_relationship(role_relationship_id: int, role_relationship: RoleRelationshipUpdate, party_id: str) -> Optional[RoleRelationshipOut]:
    async with database.transaction():
        try:
            # Convert party_id to integer
            party_id_int = int(party_id)
            # Get current role relationship for history
            current_role_relationship = await get_role_relationship(role_relationship_id, party_id)
            if not current_role_relationship:
                logger.warning(f"Role relationship not found for update: id={role_relationship_id}, party_id={party_id_int}")
                return None

            # Verify party_id has a corresponding party_role
            query_check = """
                SELECT id FROM party_role WHERE party_id = :party_id
            """
            result_check = await database.fetch_one(query=query_check, values={"party_id": party_id_int})
            if not result_check:
                logger.warning(f"No party_role found for party_id={party_id_int}")
                return None

            values = {"id": role_relationship_id}
            query_parts = []

            if role_relationship.comment is not None:
                query_parts.append("comment = :comment")
                values["comment"] = role_relationship.comment
            if role_relationship.relationship_type_id is not None:
                query_parts.append("relationship_type_id = :relationship_type_id")
                values["relationship_type_id"] = role_relationship.relationship_type_id
            if role_relationship.priority_type_id is not None:
                query_parts.append("priority_type_id = :priority_type_id")
                values["priority_type_id"] = role_relationship.priority_type_id
            if role_relationship.role_relationship_status_type_id is not None:
                query_parts.append("role_relationship_status_type_id = :role_relationship_status_type_id")
                values["role_relationship_status_type_id"] = role_relationship.role_relationship_status_type_id
            if query_parts:
                query_parts.append("updated_at = CURRENT_TIMESTAMP")

            if not query_parts:
                logger.info(f"No fields to update for role relationship id={role_relationship_id}")
                return None

            query = f"""
                UPDATE role_relationship
                SET {', '.join(query_parts)}
                WHERE id = :id
                RETURNING id, from_party_role_id, to_party_role_id, comment, relationship_type_id, priority_type_id, role_relationship_status_type_id, created_at, updated_at
            """
            result = await database.fetch_one(query=query, values=values)
            if not result:
                logger.warning(f"Role relationship not found or no changes made: id={role_relationship_id}")
                return None

            # Verify updated record is accessible by party_id
            updated_role_relationship = await get_role_relationship(role_relationship_id, party_id)
            if not updated_role_relationship:
                logger.warning(f"Updated role relationship not accessible: id={role_relationship_id}, party_id={party_id_int}")
                return None

            # Insert into role_relationship_history
            history_query = """
                INSERT INTO role_relationship_history (role_relationship_id, from_party_role_id, to_party_role_id, comment, relationship_type_id, priority_type_id, role_relationship_status_type_id, action)
                VALUES (:role_relationship_id, :from_party_role_id, :to_party_role_id, :comment, :relationship_type_id, :priority_type_id, :role_relationship_status_type_id, 'UPDATE')
            """
            history_values = {
                "role_relationship_id": role_relationship_id,
                "from_party_role_id": current_role_relationship.from_party_role_id,
                "to_party_role_id": current_role_relationship.to_party_role_id,
                "comment": values.get("comment", current_role_relationship.comment),
                "relationship_type_id": values.get("relationship_type_id", current_role_relationship.relationship_type_id),
                "priority_type_id": values.get("priority_type_id", current_role_relationship.priority_type_id),
                "role_relationship_status_type_id": values.get("role_relationship_status_type_id", current_role_relationship.role_relationship_status_type_id)
            }
            await database.execute(query=history_query, values=history_values)

            logger.info(f"Updated role relationship: id={role_relationship_id}")
            return RoleRelationshipOut(**result._mapping)
        except ValueError as e:
            logger.error(f"Invalid party_id format: {str(e)}")
            raise ValueError("Invalid party_id format")
        except Exception as e:
            logger.error(f"Error updating role relationship: {str(e)}")
            raise

# Delete role relationship (organization_user, person_user)
async def delete_role_relationship(role_relationship_id: int, party_id: str) -> Optional[int]:
    async with database.transaction():
        try:
            # Convert party_id to integer
            party_id_int = int(party_id)
            # Get current role relationship for history
            current_role_relationship = await get_role_relationship(role_relationship_id, party_id)
            if not current_role_relationship:
                logger.warning(f"Role relationship not found for deletion: id={role_relationship_id}, party_id={party_id_int}")
                return None

            # Verify party_id has a corresponding party_role
            query_check = """
                SELECT id FROM party_role WHERE party_id = :party_id
            """
            result_check = await database.fetch_one(query=query_check, values={"party_id": party_id_int})
            if not result_check:
                logger.warning(f"No party_role found for party_id={party_id_int}")
                return None

            # Insert into role_relationship_history
            history_query = """
                INSERT INTO role_relationship_history (role_relationship_id, from_party_role_id, to_party_role_id, comment, relationship_type_id, priority_type_id, role_relationship_status_type_id, action)
                VALUES (:role_relationship_id, :from_party_role_id, :to_party_role_id, :comment, :relationship_type_id, :priority_type_id, :role_relationship_status_type_id, 'DELETE')
            """
            history_values = {
                "role_relationship_id": role_relationship_id,
                "from_party_role_id": current_role_relationship.from_party_role_id,
                "to_party_role_id": current_role_relationship.to_party_role_id,
                "comment": current_role_relationship.comment,
                "relationship_type_id": current_role_relationship.relationship_type_id,
                "priority_type_id": current_role_relationship.priority_type_id,
                "role_relationship_status_type_id": current_role_relationship.role_relationship_status_type_id
            }
            await database.execute(query=history_query, values=history_values)

            # Delete role relationship
            query = "DELETE FROM role_relationship WHERE id = :id RETURNING id"
            result = await database.fetch_one(query=query, values={"id": role_relationship_id})
            logger.info(f"Deleted role relationship: id={role_relationship_id}")
            return result["id"] if result else None
        except ValueError as e:
            logger.error(f"Invalid party_id format: {str(e)}")
            raise ValueError("Invalid party_id format")
        except Exception as e:
            logger.error(f"Error deleting role relationship: {str(e)}")
            raise
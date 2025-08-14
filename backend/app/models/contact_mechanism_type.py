from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.contact_mechanism_type import ContactMechanismTypeCreate, ContactMechanismTypeUpdate, ContactMechanismTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a new contact mechanism type
async def create_contact_mechanism_type(contact_mechanism_type: ContactMechanismTypeCreate) -> Optional[ContactMechanismTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO contact_mechanism_types (description)
                VALUES (:description)
                RETURNING id, description
            """
            values = {"description": contact_mechanism_type.description}
            result = await database.fetch_one(query=query, values=values)
            logger.info(f"Created contact mechanism type: {contact_mechanism_type.description}")
            return ContactMechanismTypeOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error creating contact mechanism type: {str(e)}")
            raise

# Get contact mechanism type by ID
async def get_contact_mechanism_type(contact_mechanism_type_id: int) -> Optional[ContactMechanismTypeOut]:
    query = """
        SELECT id, description 
        FROM contact_mechanism_types WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": contact_mechanism_type_id})
    logger.info(f"Retrieved contact mechanism type: id={contact_mechanism_type_id}")
    return ContactMechanismTypeOut(**result._mapping) if result else None

# Get all contact mechanism types
async def get_all_contact_mechanism_types() -> List[ContactMechanismTypeOut]:
    query = """
        SELECT id, description 
        FROM contact_mechanism_types ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} contact mechanism types")
    return [ContactMechanismTypeOut(**result._mapping) for result in results]

# Update contact mechanism type
async def update_contact_mechanism_type(contact_mechanism_type_id: int, contact_mechanism_type: ContactMechanismTypeUpdate) -> Optional[ContactMechanismTypeOut]:
    async with database.transaction():
        try:
            values = {"id": contact_mechanism_type_id}
            query_parts = []

            if contact_mechanism_type.description is not None:
                query_parts.append("description = :description")
                values["description"] = contact_mechanism_type.description

            if not query_parts:
                logger.info(f"No fields to update for contact mechanism type id={contact_mechanism_type_id}")
                return None

            query = f"""
                UPDATE contact_mechanism_types
                SET {', '.join(query_parts)}
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values=values)
            logger.info(f"Updated contact mechanism type: id={contact_mechanism_type_id}")
            return ContactMechanismTypeOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error updating contact mechanism type: {str(e)}")
            raise

# Delete contact mechanism type
async def delete_contact_mechanism_type(contact_mechanism_type_id: int) -> Optional[int]:
    async with database.transaction():
        try:
            query = "DELETE FROM contact_mechanism_types WHERE id = :id RETURNING id"
            result = await database.fetch_one(query=query, values={"id": contact_mechanism_type_id})
            logger.info(f"Deleted contact mechanism type: id={contact_mechanism_type_id}")
            return result["id"] if result else None
        except Exception as e:
            logger.error(f"Error deleting contact mechanism type: {str(e)}")
            raise
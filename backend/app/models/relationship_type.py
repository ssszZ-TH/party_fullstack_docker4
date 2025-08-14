from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.relationship_type import RelationshipTypeCreate, RelationshipTypeUpdate, RelationshipTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a new relationship type
async def create_relationship_type(relationship_type: RelationshipTypeCreate) -> Optional[RelationshipTypeOut]:
    async with database.transaction():
        try:
            query = """
                INSERT INTO relationship_types (description)
                VALUES (:description)
                RETURNING id, description
            """
            values = {"description": relationship_type.description}
            result = await database.fetch_one(query=query, values=values)
            logger.info(f"Created relationship type: {relationship_type.description}")
            return RelationshipTypeOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error creating relationship type: {str(e)}")
            raise

# Get relationship type by ID
async def get_relationship_type(relationship_type_id: int) -> Optional[RelationshipTypeOut]:
    query = """
        SELECT id, description 
        FROM relationship_types WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": relationship_type_id})
    logger.info(f"Retrieved relationship type: id={relationship_type_id}")
    return RelationshipTypeOut(**result._mapping) if result else None

# Get all relationship types
async def get_all_relationship_types() -> List[RelationshipTypeOut]:
    query = """
        SELECT id, description 
        FROM relationship_types ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} relationship types")
    return [RelationshipTypeOut(**result._mapping) for result in results]

# Update relationship type
async def update_relationship_type(relationship_type_id: int, relationship_type: RelationshipTypeUpdate) -> Optional[RelationshipTypeOut]:
    async with database.transaction():
        try:
            values = {"id": relationship_type_id}
            query_parts = []

            if relationship_type.description is not None:
                query_parts.append("description = :description")
                values["description"] = relationship_type.description

            if not query_parts:
                logger.info(f"No fields to update for relationship type id={relationship_type_id}")
                return None

            query = f"""
                UPDATE relationship_types
                SET {', '.join(query_parts)}
                WHERE id = :id
                RETURNING id, description
            """
            result = await database.fetch_one(query=query, values=values)
            logger.info(f"Updated relationship type: id={relationship_type_id}")
            return RelationshipTypeOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error updating relationship type: {str(e)}")
            raise

# Delete relationship type
async def delete_relationship_type(relationship_type_id: int) -> Optional[int]:
    async with database.transaction():
        try:
            query = "DELETE FROM relationship_types WHERE id = :id RETURNING id"
            result = await database.fetch_one(query=query, values={"id": relationship_type_id})
            logger.info(f"Deleted relationship type: id={relationship_type_id}")
            return result["id"] if result else None
        except Exception as e:
            logger.error(f"Error deleting relationship type: {str(e)}")
            raise
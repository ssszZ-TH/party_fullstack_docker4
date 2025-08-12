from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.organization_type import OrganizationTypeCreate, OrganizationTypeUpdate, OrganizationTypeOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create organization type
# Role: basetype_admin
async def create_organization_type(organization_type: OrganizationTypeCreate) -> Optional[OrganizationTypeOut]:
    query = """
        INSERT INTO organization_types (description)
        VALUES (:description)
        RETURNING id, description
    """
    values = {"description": organization_type.description}
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Created organization type: {organization_type.description}")
    return OrganizationTypeOut(**result._mapping) if result else None

# Get organization type by ID
# Role: basetype_admin
async def get_organization_type(organization_type_id: int) -> Optional[OrganizationTypeOut]:
    query = "SELECT id, description FROM organization_types WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": organization_type_id})
    logger.info(f"Retrieved organization type: id={organization_type_id}")
    return OrganizationTypeOut(**result._mapping) if result else None

# Get all organization types
# Role: basetype_admin
async def get_all_organization_types() -> List[OrganizationTypeOut]:
    query = "SELECT id, description FROM organization_types ORDER BY id ASC"
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} organization types")
    return [OrganizationTypeOut(**result._mapping) for result in results]

# Update organization type
# Role: basetype_admin
async def update_organization_type(organization_type_id: int, organization_type: OrganizationTypeUpdate) -> Optional[OrganizationTypeOut]:
    query_parts = []
    values = {"id": organization_type_id}
    if organization_type.description is not None:
        query_parts.append("description = :description")
        values["description"] = organization_type.description
    if not query_parts:
        logger.info(f"No fields to update for organization type id={organization_type_id}")
        return None
    query = f"""
        UPDATE organization_types
        SET {', '.join(query_parts)}
        WHERE id = :id
        RETURNING id, description
    """
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Updated organization type: id={organization_type_id}")
    return OrganizationTypeOut(**result._mapping) if result else None

# Delete organization type
# Role: basetype_admin
async def delete_organization_type(organization_type_id: int) -> Optional[int]:
    query = "DELETE FROM organization_types WHERE id = :id RETURNING id"
    result = await database.fetch_one(query=query, values={"id": organization_type_id})
    logger.info(f"Deleted organization type: id={organization_type_id}")
    return result["id"] if result else None
from app.config.database import database
from app.config.settings import BCRYPT_SALT
import bcrypt
import logging
from typing import Optional, List
from datetime import datetime
from app.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create organization with hashed password, insert into party first
# Role: organization_admin
async def create_organization(organization: OrganizationCreate) -> Optional[OrganizationOut]:
    async with database.transaction():
        try:
            # Insert into party table to get party_id
            query_party = "INSERT INTO party DEFAULT VALUES RETURNING id"
            party_id = await database.fetch_val(query=query_party)

            # Insert into organizations table
            query = """
                INSERT INTO organizations (
                    id, federal_tax_id, name_en, name_th, organization_type_id, industry_type_id, 
                    employee_count_range_id, username, password, comment, created_at
                )
                VALUES (
                    :id, :federal_tax_id, :name_en, :name_th, :organization_type_id, :industry_type_id, 
                    :employee_count_range_id, :username, :password, :comment, :created_at
                )
                RETURNING id, federal_tax_id, name_en, name_th, organization_type_id, industry_type_id, 
                          employee_count_range_id, username, comment, created_at, updated_at
            """
            hashed_password = bcrypt.hashpw(organization.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
            now = datetime.utcnow()
            values = {
                "id": party_id,
                "federal_tax_id": organization.federal_tax_id,
                "name_en": organization.name_en,
                "name_th": organization.name_th,
                "organization_type_id": organization.organization_type_id,
                "industry_type_id": organization.industry_type_id,
                "employee_count_range_id": organization.employee_count_range_id,
                "username": organization.username,
                "password": hashed_password,
                "comment": organization.comment,
                "created_at": now
            }
            result = await database.fetch_one(query=query, values=values)
            if result:
                await log_organization_history(party_id, values, "create")
            logger.info(f"Created organization: {organization.name_en}")
            return OrganizationOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error creating organization: {str(e)}")
            raise

# Get organization by ID
# Role: organization_admin
async def get_organization(organization_id: int) -> Optional[OrganizationOut]:
    query = """
        SELECT id, federal_tax_id, name_en, name_th, organization_type_id, industry_type_id, 
               employee_count_range_id, username, comment, created_at, updated_at 
        FROM organizations WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": organization_id})
    logger.info(f"Retrieved organization: id={organization_id}")
    return OrganizationOut(**result._mapping) if result else None

# Get all organizations
# Role: organization_admin
async def get_all_organizations() -> List[OrganizationOut]:
    query = """
        SELECT id, federal_tax_id, name_en, name_th, organization_type_id, industry_type_id, 
               employee_count_range_id, username, comment, created_at, updated_at 
        FROM organizations ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} organizations")
    return [OrganizationOut(**result._mapping) for result in results]

# Update organization with optional fields
# Role: organization_admin
async def update_organization(organization_id: int, organization: OrganizationUpdate) -> Optional[OrganizationOut]:
    async with database.transaction():
        try:
            values = {"id": organization_id, "updated_at": datetime.utcnow()}
            query_parts = []

            if organization.federal_tax_id is not None:
                query_parts.append("federal_tax_id = :federal_tax_id")
                values["federal_tax_id"] = organization.federal_tax_id
            if organization.name_en is not None:
                query_parts.append("name_en = :name_en")
                values["name_en"] = organization.name_en
            if organization.name_th is not None:
                query_parts.append("name_th = :name_th")
                values["name_th"] = organization.name_th
            if organization.organization_type_id is not None:
                query_parts.append("organization_type_id = :organization_type_id")
                values["organization_type_id"] = organization.organization_type_id
            if organization.industry_type_id is not None:
                query_parts.append("industry_type_id = :industry_type_id")
                values["industry_type_id"] = organization.industry_type_id
            if organization.employee_count_range_id is not None:
                query_parts.append("employee_count_range_id = :employee_count_range_id")
                values["employee_count_range_id"] = organization.employee_count_range_id
            if organization.username is not None:
                query_parts.append("username = :username")
                values["username"] = organization.username
            if organization.password is not None:
                hashed_password = bcrypt.hashpw(organization.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
                query_parts.append("password = :password")
                values["password"] = hashed_password
            if organization.comment is not None:
                query_parts.append("comment = :comment")
                values["comment"] = organization.comment

            if not query_parts:
                logger.info(f"No fields to update for organization id={organization_id}")
                return None

            query = f"""
                UPDATE organizations
                SET {', '.join(query_parts)}, updated_at = :updated_at
                WHERE id = :id
                RETURNING id, federal_tax_id, name_en, name_th, organization_type_id, industry_type_id, 
                          employee_count_range_id, username, comment, created_at, updated_at
            """
            result = await database.fetch_one(query=query, values=values)
            if result:
                await log_organization_history(organization_id, values, "update")
            logger.info(f"Updated organization: id={organization_id}")
            return OrganizationOut(**result._mapping) if result else None
        except Exception as e:
            logger.error(f"Error updating organization: {str(e)}")
            raise

# Delete organization, deletes party explicitly to ensure no dangling party records
# Role: organization_admin
async def delete_organization(organization_id: int) -> Optional[int]:
    async with database.transaction():
        try:
            # Fetch organization data before deletion for history logging
            organization = await get_organization(organization_id)
            if not organization:
                logger.warning(f"Organization not found for deletion: id={organization_id}")
                return None

            # Log deletion history before actual deletion
            await log_organization_history(organization_id, {
                "federal_tax_id": organization.federal_tax_id,
                "name_en": organization.name_en,
                "name_th": organization.name_th,
                "organization_type_id": organization.organization_type_id,
                "industry_type_id": organization.industry_type_id,
                "employee_count_range_id": organization.employee_count_range_id,
                "username": organization.username,
                "comment": organization.comment
            }, "delete")

            # Explicitly delete from party table to avoid dangling records
            query_party = "DELETE FROM party WHERE id = :id RETURNING id"
            result_party = await database.fetch_one(query=query_party, values={"id": organization_id})
            if not result_party:
                logger.warning(f"Party not found for deletion: id={organization_id}")
                return None

            # Perform deletion from organizations table
            query_organization = "DELETE FROM organizations WHERE id = :id RETURNING id"
            result_organization = await database.fetch_one(query=query_organization, values={"id": organization_id})
            
            logger.info(f"Deleted organization and party: id={organization_id}")
            return result_organization["id"] if result_organization else None
        except Exception as e:
            logger.error(f"Error deleting organization: {str(e)}")
            raise

# Log organization history
# Role: organization_admin
async def log_organization_history(organization_id: int, data: dict, action: str):
    query = """
        INSERT INTO organization_history (
            organization_id, federal_tax_id, name_en, name_th, organization_type_id, 
            industry_type_id, employee_count_range_id, username, password, comment, action, action_at
        )
        VALUES (
            :organization_id, :federal_tax_id, :name_en, :name_th, :organization_type_id, 
            :industry_type_id, :employee_count_range_id, :username, :password, :comment, :action, :action_at
        )
    """
    values = {
        "organization_id": organization_id,
        "federal_tax_id": data.get("federal_tax_id"),
        "name_en": data.get("name_en"),
        "name_th": data.get("name_th"),
        "organization_type_id": data.get("organization_type_id"),
        "industry_type_id": data.get("industry_type_id"),
        "employee_count_range_id": data.get("employee_count_range_id"),
        "username": data.get("username"),
        "password": data.get("password"),
        "comment": data.get("comment"),
        "action": action,
        "action_at": datetime.utcnow()
    }
    await database.execute(query=query, values=values)
    logger.info(f"Logged organization history: id={organization_id}, action={action}")

# Verify organization credentials
# Role: organization_user
async def verify_organization_credentials(username: str, password: str) -> Optional[dict]:
    query = "SELECT id, username, password FROM organizations WHERE username = :username"
    result = await database.fetch_one(query=query, values={"username": username})
    if not result:
        logger.warning(f"Person not found for username: {username}")
        return None
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
    if hashed_password == result["password"]:
        logger.info(f"Verified credentials for organization: {username}")
        return {"id": result["id"], "username": result["username"]}
    logger.warning(f"Invalid password for organization: {username}")
    return None
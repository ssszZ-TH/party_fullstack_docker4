from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.passport import PassportCreate, PassportUpdate, PassportOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a new passport
async def create_passport(passport: PassportCreate) -> Optional[PassportOut]:
    async with database.transaction():
        try:
            # Insert into passports table
            query = """
                INSERT INTO passports (passport_id_number, issue_date, expire_date, person_id)
                VALUES (:passport_id_number, :issue_date, :expire_date, :person_id)
                RETURNING id, passport_id_number, issue_date, expire_date, person_id, created_at, updated_at
            """
            values = passport.dict()
            result = await database.fetch_one(query=query, values=values)
            if not result:
                logger.warning(f"Failed to create passport: {passport.passport_id_number}")
                return None

            # Insert into passport_history table
            history_query = """
                INSERT INTO passport_history (passport_id, passport_id_number, issue_date, expire_date, person_id, action)
                VALUES (:passport_id, :passport_id_number, :issue_date, :expire_date, :person_id, 'CREATE')
            """
            history_values = {
                "passport_id": result["id"],
                "passport_id_number": passport.passport_id_number,
                "issue_date": passport.issue_date,
                "expire_date": passport.expire_date,
                "person_id": passport.person_id
            }
            await database.execute(query=history_query, values=history_values)

            logger.info(f"Created passport: {passport.passport_id_number}")
            return PassportOut(**result._mapping)
        except Exception as e:
            logger.error(f"Error creating passport: {str(e)}")
            raise

# Get passport by ID
async def get_passport(passport_id: int) -> Optional[PassportOut]:
    query = """
        SELECT id, passport_id_number, issue_date, expire_date, person_id, created_at, updated_at
        FROM passports WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": passport_id})
    logger.info(f"Retrieved passport: id={passport_id}")
    return PassportOut(**result._mapping) if result else None

# Get all passports
async def get_all_passports() -> List[PassportOut]:
    query = """
        SELECT id, passport_id_number, issue_date, expire_date, person_id, created_at, updated_at
        FROM passports ORDER BY id ASC
    """
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} passports")
    return [PassportOut(**result._mapping) for result in results]

# Update passport
async def update_passport(passport_id: int, passport: PassportUpdate) -> Optional[PassportOut]:
    async with database.transaction():
        try:
            # Get current passport data for history
            current_passport = await get_passport(passport_id)
            if not current_passport:
                logger.warning(f"Passport not found for update: id={passport_id}")
                return None

            values = {"id": passport_id}
            query_parts = []

            if passport.passport_id_number is not None:
                query_parts.append("passport_id_number = :passport_id_number")
                values["passport_id_number"] = passport.passport_id_number
            if passport.issue_date is not None:
                query_parts.append("issue_date = :issue_date")
                values["issue_date"] = passport.issue_date
            if passport.expire_date is not None:
                query_parts.append("expire_date = :expire_date")
                values["expire_date"] = passport.expire_date
            if passport.person_id is not None:
                query_parts.append("person_id = :person_id")
                values["person_id"] = passport.person_id
            if query_parts:
                query_parts.append("updated_at = CURRENT_TIMESTAMP")

            if not query_parts:
                logger.info(f"No fields to update for passport id={passport_id}")
                return None

            # Update passport
            query = f"""
                UPDATE passports
                SET {', '.join(query_parts)}
                WHERE id = :id
                RETURNING id, passport_id_number, issue_date, expire_date, person_id, created_at, updated_at
            """
            result = await database.fetch_one(query=query, values=values)
            if not result:
                logger.warning(f"Passport not found or no changes made: id={passport_id}")
                return None

            # Insert into passport_history table
            history_query = """
                INSERT INTO passport_history (passport_id, passport_id_number, issue_date, expire_date, person_id, action)
                VALUES (:passport_id, :passport_id_number, :issue_date, :expire_date, :person_id, 'UPDATE')
            """
            history_values = {
                "passport_id": passport_id,
                "passport_id_number": values.get("passport_id_number", current_passport.passport_id_number),
                "issue_date": values.get("issue_date", current_passport.issue_date),
                "expire_date": values.get("expire_date", current_passport.expire_date),
                "person_id": values.get("person_id", current_passport.person_id)
            }
            await database.execute(query=history_query, values=history_values)

            logger.info(f"Updated passport: id={passport_id}")
            return PassportOut(**result._mapping)
        except Exception as e:
            logger.error(f"Error updating passport: {str(e)}")
            raise

# Delete passport
async def delete_passport(passport_id: int) -> Optional[int]:
    async with database.transaction():
        try:
            # Get current passport data for history
            current_passport = await get_passport(passport_id)
            if not current_passport:
                logger.warning(f"Passport not found for deletion: id={passport_id}")
                return None

            # Insert into passport_history table
            history_query = """
                INSERT INTO passport_history (passport_id, passport_id_number, issue_date, expire_date, person_id, action)
                VALUES (:passport_id, :passport_id_number, :issue_date, :expire_date, :person_id, 'DELETE')
            """
            history_values = {
                "passport_id": passport_id,
                "passport_id_number": current_passport.passport_id_number,
                "issue_date": current_passport.issue_date,
                "expire_date": current_passport.expire_date,
                "person_id": current_passport.person_id
            }
            await database.execute(query=history_query, values=history_values)

            # Delete passport
            query = "DELETE FROM passports WHERE id = :id RETURNING id"
            result = await database.fetch_one(query=query, values={"id": passport_id})
            logger.info(f"Deleted passport: id={passport_id}")
            return result["id"] if result else None
        except Exception as e:
            logger.error(f"Error deleting passport: {str(e)}")
            raise
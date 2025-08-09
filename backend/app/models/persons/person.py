from app.config.database import database
from app.config.settings import BCRYPT_SALT
from app.schemas.person import PersonCreate, PersonUpdate, PersonOut
import bcrypt
import logging
from typing import Optional, List
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_person(person: PersonCreate) -> Optional[PersonOut]:
    try:
        query = """
            INSERT INTO persons (
                username, password, personal_id_number, first_name, middle_name, last_name, 
                nick_name, birth_date, gender_type_id, marital_status_type_id, country_id, 
                height, weight, ethnicity_type_id, income_range_id, comment, created_at
            )
            VALUES (
                :username, :password, :personal_id_number, :first_name, :middle_name, :last_name, 
                :nick_name, :birth_date, :gender_type_id, :marital_status_type_id, :country_id, 
                :height, :weight, :ethnicity_type_id, :income_range_id, :comment, :created_at
            )
            RETURNING id, username, personal_id_number, first_name, middle_name, last_name, 
                      nick_name, birth_date, gender_type_id, marital_status_type_id, country_id, 
                      height, weight, ethnicity_type_id, income_range_id, comment, created_at, updated_at
        """
        hashed_password = bcrypt.hashpw(person.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        now = datetime.utcnow()
        values = {
            "username": person.username,
            "password": hashed_password,
            "personal_id_number": person.personal_id_number,
            "first_name": person.first_name,
            "middle_name": person.middle_name,
            "last_name": person.last_name,
            "nick_name": person.nick_name,
            "birth_date": person.birth_date,
            "gender_type_id": person.gender_type_id,
            "marital_status_type_id": person.marital_status_type_id,
            "country_id": person.country_id,
            "height": person.height,
            "weight": person.weight,
            "ethnicity_type_id": person.ethnicity_type_id,
            "income_range_id": person.income_range_id,
            "comment": person.comment,
            "created_at": now
        }
        result = await database.fetch_one(query=query, values=values)
        if result:
            await log_person_history(result["id"], values, "create")
        logger.info(f"Created person: {person.username}")
        return PersonOut(**result._mapping) if result else None
    except ValueError as e:
        logger.error(f"Error creating person: {str(e)}")
        raise

async def get_person(person_id: int) -> Optional[PersonOut]:
    query = """
        SELECT id, username, personal_id_number, first_name, middle_name, last_name, 
               nick_name, birth_date, gender_type_id, marital_status_type_id, country_id, 
               height, weight, ethnicity_type_id, income_range_id, comment, created_at, updated_at 
        FROM persons WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": person_id})
    logger.info(f"Retrieved person: id={person_id}")
    return PersonOut(**result._mapping) if result else None

async def update_person(person_id: int, person: PersonUpdate) -> Optional[PersonOut]:
    values = {"id": person_id, "updated_at": datetime.utcnow()}
    query_parts = []
    
    if person.username is not None:
        query_parts.append("username = :username")
        values["username"] = person.username
    if person.password is not None:
        hashed_password = bcrypt.hashpw(person.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        query_parts.append("password = :password")
        values["password"] = hashed_password
    if person.personal_id_number is not None:
        query_parts.append("personal_id_number = :personal_id_number")
        values["personal_id_number"] = person.personal_id_number
    if person.first_name is not None:
        query_parts.append("first_name = :first_name")
        values["first_name"] = person.first_name
    if person.middle_name is not None:
        query_parts.append("middle_name = :middle_name")
        values["middle_name"] = person.middle_name
    if person.last_name is not None:
        query_parts.append("last_name = :last_name")
        values["last_name"] = person.last_name
    if person.nick_name is not None:
        query_parts.append("nick_name = :nick_name")
        values["nick_name"] = person.nick_name
    if person.birth_date is not None:
        query_parts.append("birth_date = :birth_date")
        values["birth_date"] = person.birth_date
    if person.gender_type_id is not None:
        query_parts.append("gender_type_id = :gender_type_id")
        values["gender_type_id"] = person.gender_type_id
    if person.marital_status_type_id is not None:
        query_parts.append("marital_status_type_id = :marital_status_type_id")
        values["marital_status_type_id"] = person.marital_status_type_id
    if person.country_id is not None:
        query_parts.append("country_id = :country_id")
        values["country_id"] = person.country_id
    if person.height is not None:
        query_parts.append("height = :height")
        values["height"] = person.height
    if person.weight is not None:
        query_parts.append("weight = :weight")
        values["weight"] = person.weight
    if person.ethnicity_type_id is not None:
        query_parts.append("ethnicity_type_id = :ethnicity_type_id")
        values["ethnicity_type_id"] = person.ethnicity_type_id
    if person.income_range_id is not None:
        query_parts.append("income_range_id = :income_range_id")
        values["income_range_id"] = person.income_range_id
    if person.comment is not None:
        query_parts.append("comment = :comment")
        values["comment"] = person.comment

    if not query_parts:
        logger.info(f"No fields to update for person id={person_id}")
        return None

    query = f"""
        UPDATE persons
        SET {', '.join(query_parts)}, updated_at = :updated_at
        WHERE id = :id
        RETURNING id, username, personal_id_number, first_name, middle_name, last_name, 
                  nick_name, birth_date, gender_type_id, marital_status_type_id, country_id, 
                  height, weight, ethnicity_type_id, income_range_id, comment, created_at, updated_at
    """
    result = await database.fetch_one(query=query, values=values)
    if result:
        await log_person_history(person_id, values, "update")
    logger.info(f"Updated person: id={person_id}")
    return PersonOut(**result._mapping) if result else None

async def delete_person(person_id: int) -> Optional[int]:
    query = "DELETE FROM persons WHERE id = :id RETURNING id"
    result = await database.fetch_one(query=query, values={"id": person_id})
    if result:
        await log_person_history(person_id, {"id": person_id}, "delete")
    logger.info(f"Deleted person: id={person_id}")
    return result["id"] if result else None

async def log_person_history(person_id: int, data: dict, action: str):
    query = """
        INSERT INTO person_history (
            person_id, username, password, personal_id_number, first_name, middle_name, last_name, 
            nick_name, birth_date, gender_type_id, marital_status_type_id, country_id, 
            height, weight, ethnicity_type_id, income_range_id, comment, action, action_at
        )
        VALUES (
            :person_id, :username, :password, :personal_id_number, :first_name, :middle_name, :last_name, 
            :nick_name, :birth_date, :gender_type_id, :marital_status_type_id, :country_id, 
            :height, :weight, :ethnicity_type_id, :income_range_id, :comment, :action, :action_at
        )
    """
    values = {
        "person_id": person_id,
        "username": data.get("username"),
        "password": data.get("password"),
        "personal_id_number": data.get("personal_id_number"),
        "first_name": data.get("first_name"),
        "middle_name": data.get("middle_name"),
        "last_name": data.get("last_name"),
        "nick_name": data.get("nick_name"),
        "birth_date": data.get("birth_date"),
        "gender_type_id": data.get("gender_type_id"),
        "marital_status_type_id": data.get("marital_status_type_id"),
        "country_id": data.get("country_id"),
        "height": data.get("height"),
        "weight": data.get("weight"),
        "ethnicity_type_id": data.get("ethnicity_type_id"),
        "income_range_id": data.get("income_range_id"),
        "comment": data.get("comment"),
        "action": action,
        "action_at": datetime.utcnow()
    }
    await database.execute(query=query, values=values)
    logger.info(f"Logged person history: id={person_id}, action={action}")
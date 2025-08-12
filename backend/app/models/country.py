from app.config.database import database
import logging
from typing import Optional, List
from app.schemas.country import CountryCreate, CountryUpdate, CountryOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create country
# Role: basetype_admin
async def create_country(country: CountryCreate) -> Optional[CountryOut]:
    query = """
        INSERT INTO countries (iso_code, name_en, name_th)
        VALUES (:iso_code, :name_en, :name_th)
        RETURNING id, iso_code, name_en, name_th
    """
    values = {"iso_code": country.iso_code, "name_en": country.name_en, "name_th": country.name_th}
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Created country: {country.name_en}")
    return CountryOut(**result._mapping) if result else None

# Get country by ID
# Role: basetype_admin
async def get_country(country_id: int) -> Optional[CountryOut]:
    query = "SELECT id, iso_code, name_en, name_th FROM countries WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": country_id})
    logger.info(f"Retrieved country: id={country_id}")
    return CountryOut(**result._mapping) if result else None

# Get all countries
# Role: basetype_admin
async def get_all_countries() -> List[CountryOut]:
    query = "SELECT id, iso_code, name_en, name_th FROM countries ORDER BY id ASC"
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} countries")
    return [CountryOut(**result._mapping) for result in results]

# Update country
# Role: basetype_admin
async def update_country(country_id: int, country: CountryUpdate) -> Optional[CountryOut]:
    query_parts = []
    values = {"id": country_id}
    if country.iso_code is not None:
        query_parts.append("iso_code = :iso_code")
        values["iso_code"] = country.iso_code
    if country.name_en is not None:
        query_parts.append("name_en = :name_en")
        values["name_en"] = country.name_en
    if country.name_th is not None:
        query_parts.append("name_th = :name_th")
        values["name_th"] = country.name_th
    if not query_parts:
        logger.info(f"No fields to update for country id={country_id}")
        return None
    query = f"""
        UPDATE countries
        SET {', '.join(query_parts)}
        WHERE id = :id
        RETURNING id, iso_code, name_en, name_th
    """
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Updated country: id={country_id}")
    return CountryOut(**result._mapping) if result else None

# Delete country
# Role: basetype_admin
async def delete_country(country_id: int) -> Optional[int]:
    query = "DELETE FROM countries WHERE id = :id RETURNING id"
    result = await database.fetch_one(query=query, values={"id": country_id})
    logger.info(f"Deleted country: id={country_id}")
    return result["id"] if result else None
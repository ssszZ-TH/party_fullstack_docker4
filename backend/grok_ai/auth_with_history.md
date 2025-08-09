จากที่ดู test case รู้ละว่าที่ทำมาผิด เอาใหม่ๆ 

role เปลี่ยนคำใหม่ดีกว่า จะได้ไม่งง
role system_admin คือคนที่จัดการ user ทุก role ในระบบ 

account_admin เปลี่ยนชื่อเป็น basetype_admin เเทน

มี endpoint register ไว้เป็น backdoor หน่อย ไม่งั้นผมสร้าง user ในระบบไม่ได้

เพื่อไม่ให้งง สรุปตอนนี้มี role อยู่ดังนี้
system_admin
basetype_admin
hr_admin
organization_admin

person กับ organization มี table เเยกเป็นของตัวเองไปเลย ไม่ต้องเป็น role ใน account เเล้ว

person เก็บข้อมูลดังนี้
username
password
personal_id _number
first_name
middle_name (null able)
last_name
nick_name
birth_date
gender_type_id (เดี๋ยวจะมีตาราง gender type เก็บ id description ไว้ ทำให้ด้วย)
marital_status_type_id ( เดี๋ยวจะมีตารา marital status type เก็บ id description)
country_id (เดี๋ยวจะมี table country เก็บ id iso_code name_en name_th)
height INT
weight INT
ethnicity_type_id (เดี๋ยวมี table id description อีกเหมือนเดิม)
income_range_id
comment

อยากให้ช่วย design ให้หน่อย ผมต้องการเก็บประวัติย้อนหลังทั้งหมดของการ update ข้อมูลของ person

organization เก็บข้อมูลดังนี้
federal_tax_id (null able)
name_en
name_th (null able)
organization_type_id (เดี๋ยวมี table id description อีกเหมือนเดิม)

organization ผมอยากให้ช่วย design เหมือนกัน ต้องการเก็บประวิติการเเก้ใขข้อมูลย้อนหลังทั้งหมด

ตรง table user เเก้ใขหน่อย update_at timestamp ต้องเป็น null ได้ เพราะตอนที่ create ยังไม่เคยถูกเเก้ใข ให้เป็น null ไว้ก่อน พอโดนเเก้ใขค่อยใส่ timestamp ตอนเเก้ใข

เขียน code ทั้งหมดมาใหม่ 
เขียน sql สร้าง table มา
เขียน test plan มาด้วย


Below are the updated files for the FastAPI backend, SQL for creating tables, and a test plan based on your requirements. The design includes a backdoor `/auth/register` endpoint, new role definitions, separate `person` and `organization` tables, and history tracking for updates to `person` and `organization` data. The `users` table has been updated to allow `updated_at` to be nullable. Additionally, supporting tables (`gender_types`, `marital_status_types`, `countries`, `income_ranges`, `ethnicity_types`, `organization_types`) are included.

---

<xaiArtifact artifact_id="02e0c1c3-8f05-46cd-a000-503e5a6363f6" artifact_version_id="8f1ea5a3-68e5-464e-8c0d-80531d8891bd" title="main.py" contentType="text/python">
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import database
from app.controllers.auth.auth import router as auth_router
from app.controllers.users.user import router as user_router
from app.controllers.persons.person import router as person_router
from app.controllers.organizations.organization import router as organization_router

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(person_router)
app.include_router(organization_router)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message": "FastAPI Backend", "github": "https://github.com/ssszZ-TH/party_fullstack_docker4"}
</xaiArtifact>

<xaiArtifact artifact_id="31830e4c-447a-4743-9460-7f888b3c56e1" artifact_version_id="c7319a1e-e3d2-42ca-96e3-3488d1887898" title="schemas/user.py" contentType="text/python">
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class BasetypeAdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
</xaiArtifact>

<xaiArtifact artifact_id="c77d4648-1e10-4121-9cc5-54dc2f32636c" artifact_version_id="af1bf698-1800-43a3-a6b8-68bb68993f6b" title="schemas/person.py" contentType="text/python">
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class PersonCreate(BaseModel):
    username: str
    password: str
    personal_id_number: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    nick_name: Optional[str] = None
    birth_date: date
    gender_type_id: int
    marital_status_type_id: int
    country_id: int
    height: int
    weight: int
    ethnicity_type_id: int
    income_range_id: int
    comment: Optional[str] = None

class PersonUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    personal_id_number: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    nick_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender_type_id: Optional[int] = None
    marital_status_type_id: Optional[int] = None
    country_id: Optional[int] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    ethnicity_type_id: Optional[int] = None
    income_range_id: Optional[int] = None
    comment: Optional[str] = None

class PersonOut(BaseModel):
    id: int
    username: str
    personal_id_number: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    nick_name: Optional[str] = None
    birth_date: date
    gender_type_id: int
    marital_status_type_id: int
    country_id: int
    height: int
    weight: int
    ethnicity_type_id: int
    income_range_id: int
    comment: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
</xaiArtifact>

<xaiArtifact artifact_id="c14fbd68-9acd-4d68-a1a8-4a5b049dc599" artifact_version_id="dd85f4ad-a472-4c5c-9727-965a75ce7aa2" title="schemas/organization.py" contentType="text/python">
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrganizationCreate(BaseModel):
    federal_tax_id: Optional[str] = None
    name_en: str
    name_th: Optional[str] = None
    organization_type_id: int

class OrganizationUpdate(BaseModel):
    federal_federal_tax_id: Optional[str] = None
    name_en: Optional[str] = None
    name_th: Optional[str] = None
    organization_type_id: Optional[int] = None

class OrganizationOut(BaseModel):
    id: int
    federal_tax_id: Optional[str] = None
    name_en: str
    name_th: Optional[str] = None
    organization_type_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
</xaiArtifact>

<xaiArtifact artifact_id="5c96eced-5afc-4323-b78f-a91eab61fd7c" artifact_version_id="4efcc6ba-aa8c-402a-bf4a-1c261e6e62ab" title="models/users/user.py" contentType="text/python">
from app.config.database import database
from app.config.settings import BCRYPT_SALT
from app.schemas.user import UserCreate, UserUpdate, UserOut, BasetypeAdminCreate
import bcrypt
import logging
from typing import Optional, List
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Role permissions:
# system_admin: CRUD all users
# basetype_admin: CRUD users with roles hr_admin, organization_admin
# hr_admin: CRUD person-related data
# organization_admin: CRUD organization-related data

async def get_user_by_email(email: str) -> Optional[dict]:
    query = "SELECT id, name, email, password, role, created_at, updated_at FROM users WHERE email = :email"
    result = await database.fetch_one(query=query, values={"email": email})
    logger.info(f"Queried user with email {email}: {result}")
    return result

async def create_user(user: UserCreate) -> Optional[UserOut]:
    try:
        existing_user = await get_user_by_email(user.email)
        if existing_user:
            logger.warning(f"Attempt to create user with existing email: {user.email}")
            return None
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        now = datetime.utcnow()
        query = """
            INSERT INTO users (name, email, password, role, created_at)
            VALUES (:name, :email, :password, :role, :created_at)
            RETURNING id, name, email, role, created_at, updated_at
        """
        values = {
            "name": user.name,
            "email": user.email,
            "password": hashed_password,
            "role": user.role or "hr_admin",
            "created_at": now
        }
        result = await database.fetch_one(query=query, values=values)
        logger.info(f"Created user: {user.email}, role: {user.role}")
        return UserOut(**result._mapping) if result else None
    except ValueError as e:
        logger.error(f"Error hashing password for {user.email}: {str(e)}")
        raise

async def create_basetype_admin(user: BasetypeAdminCreate) -> Optional[UserOut]:
    try:
        existing_user = await get_user_by_email(user.email)
        if existing_user:
            logger.warning(f"Attempt to create basetype admin with existing email: {user.email}")
            return None
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        now = datetime.utcnow()
        query = """
            INSERT INTO users (name, email, password, role, created_at)
            VALUES (:name, :email, :password, :role, :created_at)
            RETURNING id, name, email, role, created_at, updated_at
        """
        values = {
            "name": user.name,
            "email": user.email,
            "password": hashed_password,
            "role": "basetype_admin",
            "created_at": now
        }
        result = await database.fetch_one(query=query, values=values)
        logger.info(f"Created basetype admin: {user.email}")
        return UserOut(**result._mapping) if result else None
    except ValueError as e:
        logger.error(f"Error hashing password for {user.email}: {str(e)}")
        raise

async def get_user(user_id: int) -> Optional[UserOut]:
    query = "SELECT id, name, email, role, created_at, updated_at FROM users WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": user_id})
    logger.info(f"Retrieved user: id={user_id}")
    return UserOut(**result._mapping) if result else None

async def get_all_users() -> List[UserOut]:
    query = "SELECT id, name, email, role, created_at, updated_at FROM users ORDER BY id ASC"
    results = await database.fetch_all(query=query)
    logger.info(f"Retrieved {len(results)} users")
    return [UserOut(**result._mapping) for result in results]

async def update_user(user_id: int, user: UserUpdate) -> Optional[UserOut]:
    values = {"id": user_id, "updated_at": datetime.utcnow()}
    query_parts = []
    
    if user.name is not None:
        query_parts.append("name = :name")
        values["name"] = user.name
    if user.email is not None:
        query_parts.append("email = :email")
        values["email"] = user.email
    if user.password is not None:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        query_parts.append("password = :password")
        values["password"] = hashed_password

    if not query_parts:
        logger.info(f"No fields to update for user id={user_id}")
        return None

    query = f"""
        UPDATE users
        SET {', '.join(query_parts)}, updated_at = :updated_at
        WHERE id = :id
        RETURNING id, name, email, role, created_at, updated_at
    """
    result = await database.fetch_one(query=query, values=values)
    logger.info(f"Updated user: id={user_id}")
    return UserOut(**result._mapping) if result else None

async def delete_user(user_id: int) -> Optional[int]:
    query = "DELETE FROM users WHERE id = :id RETURNING id"
    result = await database.fetch_one(query=query, values={"id": user_id})
    logger.info(f"Deleted user: id={user_id}")
    return result["id"] if result else None

async def verify_user_password(user_id: int, password: str) -> bool:
    query = "SELECT password FROM users WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": user_id})
    if not result:
        logger.warning(f"User not found for password verification: id={user_id}")
        return False
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
    logger.info(f"Verified password for user id={user_id}")
    return hashed_password == result["password"]
</xaiArtifact>

<xaiArtifact artifact_id="1f9413bc-f2cc-4a13-8e99-4951a75802e5" artifact_version_id="f4c8d696-226b-484c-908d-1bdffe9032ed" title="models/persons/person.py" contentType="text/python">
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
</xaiArtifact>

<xaiArtifact artifact_id="4df0e203-736a-4ed2-b1a4-320a2ebc1cb1" artifact_version_id="79d6a9fc-818d-4cd4-a81a-b4b9f9c17eb7" title="models/organizations/organization.py" contentType="text/python">
from app.config.database import database
import logging
from typing import Optional, List
from datetime import datetime
from app.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_organization(organization: OrganizationCreate) -> Optional[OrganizationOut]:
    try:
        query = """
            INSERT INTO organizations (federal_tax_id, name_en, name_th, organization_type_id, created_at)
            VALUES (:federal_tax_id, :name_en, :name_th, :organization_type_id, :created_at)
            RETURNING id, federal_tax_id, name_en, name_th, organization_type_id, created_at, updated_at
        """
        now = datetime.utcnow()
        values = {
            "federal_tax_id": organization.federal_tax_id,
            "name_en": organization.name_en,
            "name_th": organization.name_th,
            "organization_type_id": organization.organization_type_id,
            "created_at": now
        }
        result = await database.fetch_one(query=query, values=values)
        if result:
            await log_organization_history(result["id"], values, "create")
        logger.info(f"Created organization: {organization.name_en}")
        return OrganizationOut(**result._mapping) if result else None
    except ValueError as e:
        logger.error(f"Error creating organization: {str(e)}")
        raise

async def get_organization(organization_id: int) -> Optional[OrganizationOut]:
    query = """
        SELECT id, federal_tax_id, name_en, name_th, organization_type_id, created_at, updated_at 
        FROM organizations WHERE id = :id
    """
    result = await database.fetch_one(query=query, values={"id": organization_id})
    logger.info(f"Retrieved organization: id={organization_id}")
    return OrganizationOut(**result._mapping) if result else None

async def update_organization(organization_id: int, organization: OrganizationUpdate) -> Optional[OrganizationOut]:
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

    if not query_parts:
        logger.info(f"No fields to update for organization id={organization_id}")
        return None

    query = f"""
        UPDATE organizations
        SET {', '.join(query_parts)}, updated_at = :updated_at
        WHERE id = :id
        RETURNING id, federal_tax_id, name_en, name-dotorgname_th, organization_type_id, created_at, updated_at
    """
    result = await database.fetch_one(query=query, values=values)
    if result:
        await log_organization_history(organization_id, values, "update")
    logger.info(f"Updated organization: id={organization_id}")
    return OrganizationOut(**result._mapping) if result else None

async def delete_organization(organization_id: int) -> Optional[int]:
    query = "DELETE FROM organizations WHERE id = :id RETURNING id"
    result = await database.fetch_one(query=query, values={"id": organization_id})
    if result:
        await log_organization_history(organization_id, {"id": organization_id}, "delete")
    logger.info(f"Deleted organization: id={organization_id}")
    return result["id"] if result else None

async def log_organization_history(organization_id: int, data: dict, action: str):
    query = """
        INSERT INTO organization_history (
            organization_id, federal_tax_id, name_en, name_th, organization_type_id, action, action_at
        )
        VALUES (:organization_id, :federal_tax_id, :name_en, :name_th, :organization_type_id, :action, :action_at)
    """
    values = {
        "organization_id": organization_id,
        "federal_tax_id": data.get("federal_tax_id"),
        "name_en": data.get("name_en"),
        "name_th": data.get("name_th"),
        "organization_type_id": data.get("organization_type_id"),
        "action": action,
        "action_at": datetime.utcnow()
    }
    await database.execute(query=query, values=values)
    logger.info(f"Logged organization history: id={organization_id}, action={action}")
</xaiArtifact>

<xaiArtifact artifact_id="7fd4c493-707c-4849-9e7c-4d189577ce9c" artifact_version_id="26806b1f-45e6-4b04-b812-682f82c3fd85" title="controllers/users/user.py" contentType="text/python">
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List
import logging
from app.models.users.user import create_user, get_user, update_user, delete_user, get_all_users, create_basetype_admin
from app.schemas.user import UserCreate, UserUpdate, UserOut, BasetypeAdminCreate
from app.config.settings import SECRET_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        logger.info(f"Decoded JWT payload: {payload}")
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None:
            logger.error(f"Invalid token: missing 'sub'")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.info(f"Authenticated user: id={user_id}, role={role}")
        return {"id": user_id, "role": role}
    except JWTError as e:
        logger.error(f"JWT decode failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/", response_model=UserOut)
async def create_user_endpoint(user: UserCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["system_admin", "basetype_admin"]:
        logger.warning(f"Unauthorized attempt to create user by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="System or basetype admin access required")
    if current_user["role"] == "basetype_admin" and user.role not in ["hr_admin", "organization_admin"]:
        logger.warning(f"Basetype admin attempted to create unauthorized role: {user.role}")
        raise HTTPException(status_code=403, detail="Basetype admin can only create hr_admin or organization_admin")
    result = await create_user(user)
    if not result:
        logger.warning(f"Failed to create user: {user.email}")
        raise HTTPException(status_code=400, detail="Email already exists")
    logger.info(f"Created user: {user.email}, role={result.role}")
    return result

@router.post("/basetype-admin", response_model=UserOut)
async def create_basetype_admin_endpoint(user: BasetypeAdminCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "system_admin":
        logger.warning(f"Unauthorized attempt to create basetype admin by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="System admin access required")
    result = await create_basetype_admin(user)
    if not result:
        logger.warning(f"Failed to create basetype admin: {user.email}")
        raise HTTPException(status_code=400, detail="Email already exists")
    logger.info(f"Created basetype admin: {user.email}")
    return result

@router.get("/me", response_model=UserOut)
async def get_current_user_endpoint(current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["id"])
    result = await get_user(user_id)
    if not result:
        logger.warning(f"User not found: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Retrieved current user: id={user_id}, role={result.role}")
    return result

@router.get("/{user_id}", response_model=UserOut)
async def get_user_endpoint(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "system_admin":
        logger.warning(f"Unauthorized attempt to get user by id={user_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="System admin access required")
    result = await get_user(user_id)
    if not result:
        logger.warning(f"User not found: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Retrieved user: id={user_id}, role={result.role}")
    return result

@router.get("/", response_model=List[UserOut])
async def get_all_users_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "system_admin":
        logger.warning(f"Unauthorized attempt to list all users by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="System admin access required")
    results = await get_all_users()
    logger.info(f"Retrieved {len(results)} users")
    return results

@router.put("/me", response_model=UserOut)
async def update_user_endpoint(user: UserUpdate, current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["id"])
    result = await update_user(user_id, user)
    if not result:
        logger.warning(f"User not found for update: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger CNAI(1): info(f"Updated user: id={user_id}, role={result.role}")
    return result

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "system_admin":
        logger.warning(f"Unauthorized attempt to delete user by id={user_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="System admin access required")
    result = await delete_user(user_id)
    if not result:
        logger.warning(f"User not found for deletion: id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Deleted user: id={user_id}")
    return {"message": "User deleted"}
</xaiArtifact>

<xaiArtifact artifact_id="31ab7647-72e8-4b55-a84e-ca73c5b582f2" artifact_version_id="bf29c903-1573-43ba-b027-418c16fbfb81" title="controllers/persons/person.py" contentType="text/python">
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List
import logging
from app.models.persons.person import create_person, get_person, update_person, delete_person
from app.schemas.person import PersonCreate, PersonUpdate, PersonOut
from app.config.settings import SECRET_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/persons", tags=["persons"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        logger.info(f"Decoded JWT payload: {payload}")
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None:
            logger.error(f"Invalid token: missing 'sub'")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.info(f"Authenticated user: id={user_id}, role={role}")
        return {"id": user_id, "role": role}
    except JWTError as e:
        logger.error(f"JWT decode failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/", response_model=PersonOut)
async def create_person_endpoint(person: PersonCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to create person by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="HR admin access required")
    result = await create_person(person)
    if not result:
        logger.warning(f"Failed to create person: {person.username}")
        raise HTTPException(status_code=400, detail="Person already exists")
    logger.info(f"Created person: {person.username}")
    return result

@router.get("/{person_id}", response_model=PersonOut)
async def get_person_endpoint(person_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to get person by id={person_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="HR admin access required")
    result = await get_person(person_id)
    if not result:
        logger.warning(f"Person not found: id={person_id}")
        raise HTTPException(status_code=404, detail="Person not found")
    logger.info(f"Retrieved person: id={person_id}")
    return result

@router.put("/{person_id}", response_model=PersonOut)
async def update_person_endpoint(person_id: int, person: PersonUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to update person by id={person_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="HR admin access required")
    result = await update_person(person_id, person)
    if not result:
        logger.warning(f"Person not found for update: id={person_id}")
        raise HTTPException(status_code=404, detail="Person not found")
    logger.info(f"Updated person: id={person_id}")
    return result

@router.delete("/{person_id}")
async def delete_person_endpoint(person_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr_admin":
        logger.warning(f"Unauthorized attempt to delete person by id={person_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="HR admin access required")
    result = await delete_person(person_id)
    if not result:
        logger.warning(f"Person not found for deletion: id={person_id}")
        raise HTTPException(status_code=404, detail="Person not found")
    logger.info(f"Deleted person: id={person_id}")
    return {"message": "Person deleted"}
</xaiArtifact>

<xaiArtifact artifact_id="c41519d4-5c9e-41ca-8afe-8e718472c589" artifact_version_id="01c4fc80-c4b7-47b7-93db-5964f19b89dd" title="controllers/organizations/organization.py" contentType="text/python">
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List
import logging
from app.models.organizations.organization import create_organization, get_organization, update_organization, delete_organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationOut
from app.config.settings import SECRET_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/organizations", tags=["organizations"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        logger.info(f"Decoded JWT payload: {payload}")
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None:
            logger.error(f"Invalid token: missing 'sub'")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.info(f"Authenticated user: id={user_id}, role={role}")
        return {"id": user_id, "role": role}
    except JWTError as e:
        logger.error(f"JWT decode failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/", response_model=OrganizationOut)
async def create_organization_endpoint(organization: OrganizationCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "organization_admin":
        logger.warning(f"Unauthorized attempt to create organization by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Organization admin access required")
    result = await create_organization(organization)
    if not result:
        logger.warning(f"Failed to create organization: {organization.name_en}")
        raise HTTPException(status_code=400, detail="Organization already exists")
    logger.info(f"Created organization: {organization.name_en}")
    return result

@router.get("/{organization_id}", response_model=OrganizationOut)
async def get_organization_endpoint(organization_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "organization_admin":
        logger.warning(f"Unauthorized attempt to get organization by id={organization_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Organization admin access required")
    result = await get_organization(organization_id)
    if not result:
        logger.warning(f"Organization not found: id={organization_id}")
        raise HTTPException(status_code=404, detail="Organization not found")
    logger.info(f"Retrieved organization: id={organization_id}")
    return result

@router.put("/{organization_id}", response_model=OrganizationOut)
async def update_organization_endpoint(organization_id: int, organization: OrganizationUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "organization_admin":
        logger.warning(f"Unauthorized attempt to update organization by id={organization_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Organization admin access required")
    result = await update_organization(organization_id, organization)
    if not result:
        logger.warning(f"Organization not found for update: id={organization_id}")
        raise HTTPException(status_code=404, detail="Organization not found")
    logger.info(f"Updated organization: id={organization_id}")
    return result

@router.delete("/{organization_id}")
async def delete_organization_endpoint(organization_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "organization_admin":
        logger.warning(f"Unauthorized attempt to delete organization by id={organization_id} by user: id={current_user['id']}, role={current_user['role']}")
        raise HTTPException(status_code=403, detail="Organization admin access required")
    result = await delete_organization(organization_id)
    if not result:
        logger.warning(f"Organization not found for deletion: id={organization_id}")
        raise HTTPException(status_code=404, detail="Organization not found")
    logger.info(f"Deleted organization: id={organization_id}")
    return {"message": "Organization deleted"}
</xaiArtifact>

<xaiArtifact artifact_id="6b68a75b-6a7c-4e66-a3f2-33f883ec0396" artifact_version_id="ccdc3701-4eef-4277-a31c-5b2f5efbaaf9" title="controllers/auth/auth.py" contentType="text/python">
from fastapi import APIRouter, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config.settings import SECRET_KEY, BCRYPT_SALT
from app.config.database import database
import bcrypt
import logging
from app.schemas.user import UserCreate, UserLogin
from app.models.users.user import create_user, get_user_by_email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

ALGORITHM = "HS256"

def create_access_token(data: dict):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info(f"Created JWT for user: id={data.get('sub')}, role={data.get('role')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating JWT: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create token")

@router.post("/register")
async def register(user: UserCreate):
    try:
        result = await create_user(user)
        if not result:
            logger.warning(f"Registration failed: Email {user.email} already exists")
            raise HTTPException(status_code=400, detail="Email already exists")
        logger.info(f"User registered: {user.email}, role={result.role}")
        return {"message": "User created"}
    except ValueError as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Invalid BCRYPT_SALT")

@router.post("/login")
async def login(user: UserLogin):
    db_user = await get_user_by_email(user.email)
    if not db_user:
        logger.warning(f"Login attempt with invalid email: {user.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    logger.info(f"Found user: id={db_user['id']}, email={db_user['email']}, role={db_user['role']}")
    try:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), BCRYPT_SALT.encode('utf-8')).decode('utf-8')
        if hashed_password != db_user["password"]:
            logger.warning(f"Invalid password for email: {user.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except ValueError as e:
        logger.error(f"Error verifying password for {user.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Invalid BCRYPT_SALT")
    token = create_access_token({"sub": str(db_user["id"]), "role": db_user["role"]})
    logger.info(f"User logged in: {user.email}, token sub={db_user['id']}, role={db_user['role']}")
    return {"access_token": token, "token_type": "bearer"}
</xaiArtifact>

<xaiArtifact artifact_id="533d980a-104b-44a0-bd3a-d56dead62042" artifact_version_id="3032185b-dda9-4cfd-88d7-ecad70792046" title="create_tables.sql" contentType="text/sql">
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) CHECK (role IN ('system_admin', 'basetype_admin', 'hr_admin', 'organization_admin')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE gender_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE marital_status_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    iso_code VARCHAR(3) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    name_th VARCHAR(100)
);

CREATE TABLE ethnicity_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE income_ranges (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE organization_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE persons (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    personal_id_number VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    middle_name VARCHAR(255),
    last_name VARCHAR(255) NOT NULL,
    nick_name VARCHAR(255),
    birth_date DATE NOT NULL,
    gender_type_id INT REFERENCES gender_types(id),
    marital_status_type_id INT REFERENCES marital_status_types(id),
    country_id INT REFERENCES countries(id),
    height INT NOT NULL,
    weight INT NOT NULL,
    ethnicity_type_id INT REFERENCES ethnicity_types(id),
    income_range_id INT REFERENCES income_ranges(id),
    comment TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE person_history (
    id SERIAL PRIMARY KEY,
    person_id INT REFERENCES persons(id),
    username VARCHAR(255),
    password VARCHAR(255),
    personal_id_number VARCHAR(50),
    first_name VARCHAR(255),
    middle_name VARCHAR(255),
    last_name VARCHAR(255),
    nick_name VARCHAR(255),
    birth_date DATE,
    gender_type_id INT,
    marital_status_type_id INT,
    country_id INT,
    height INT,
    weight INT,
    ethnicity_type_id INT,
    income_range_id INT,
    comment TEXT,
    action VARCHAR(50) NOT NULL,
    action_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    federal_tax_id VARCHAR(50),
    name_en VARCHAR(255) NOT NULL,
    name_th VARCHAR(255),
    organization_type_id INT REFERENCES organization_types(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE organization_history (
    id SERIAL PRIMARY KEY,
    organization_id INT REFERENCES organizations(id),
    federal_tax_id VARCHAR(50),
    name_en VARCHAR(255),
    name_th VARCHAR(255),
    organization_type_id INT,
    action VARCHAR(50) NOT NULL,
    action_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
</xaiArtifact>

<xaiArtifact artifact_id="e58e0a79-1f4a-4e73-b1f1-bb5e513cc284" artifact_version_id="46aeaf70-100e-47f7-9a0d-a7ba4d827d77" title="test_plan.py" contentType="text/python">
# Test Plan for FastAPI Backend using Postman
# Date: August 09, 2025

# 1. Register User (Backdoor)
Method: POST
Path: /auth/register
Payload:
{
    "name": "System Admin",
    "email": "sysadmin@example.com",
    "password": "syspassword123",
    "role": "system_admin"
}
Headers:
- Content-Type: application/json
Expected Response:
- 200 OK: {"message": "User created"}
- 400 Bad Request: {"detail": "Email already exists"}
Notes: Use to create initial system_admin. Save token for further tests.

# 2. Login
Method: POST
Path: /auth/login
Payload:
{
    "email": "sysadmin@example.com",
    "password": "syspassword123"
}
Headers:
- Content-Type: application/json
Expected Response:
- 200 OK: {"access_token": "<token>", "token_type": "bearer"}
- 401 Unauthorized: {"detail": "Invalid credentials"} (if email/password wrong)
Notes: Save token for authenticated requests.

# 3. Create Basetype Admin (requires system_admin token)
Method: POST
Path: /users/basetype-admin
Payload:
{
    "name": "Basetype Admin",
    "email": "basetypeadmin@example.com",
    "password": "basepassword123"
}
Headers:
- Content-Type: application/json
- Authorization: Bearer <system_admin_token>
Expected Response:
- 200 OK: {"id": 1, "name": "Basetype Admin", "email": "basetypeadmin@example.com", "role": "basetype_admin", "created_at": "...", "updated_at": null}
- 400 Bad Request: {"detail": "Email already exists"}
- 403 Forbidden: {"detail": "System admin access required"} (if not system_admin)
Notes: Only system_admin can create basetype_admin.

# 4. Create User (requires system_admin or basetype_admin token)
Method: POST
Path: /users/
Payload:
{
    "name": "HR Admin",
    "email": "hradmin@example.com",
    "password": "hrpassword123",
    "role": "hr_admin"
}
Headers:
- Content-Type: application/json
- Authorization: Bearer <system_admin_token or basetype_admin_token>
Expected Response:
- 200 OK: {"id": 2, "name": "HR Admin", "email": "hradmin@example.com", "role": "hr_admin", "created_at": "...", "updated_at": null}
- 400 Bad Request: {"detail": "Email already exists"}
- 403 Forbidden: {"detail": "System or basetype admin access required"} (if not authorized)
- 403 Forbidden: {"detail": "Basetype admin can only create hr_admin or organization_admin"} (if basetype_admin tries invalid role)
Notes: Basetype_admin can only create hr_admin or organization_admin.

# 5. Get Current User (requires any valid token)
Method: GET
Path: /users/me
Payload: None
Headers:
- Authorization: Bearer <any_token>
Expected Response:
- 200 OK: {"id": 1, "name": "...", "email": "...", "role": "...", "created_at": "...", "updated_at": null}
- 401 Unauthorized: {"detail": "Invalid token"} (if token invalid)
- 404 Not Found: {"detail": "User not found"}
Notes: All roles can access their own data.

# 6. Get User by ID (requires system_admin token)
Method: GET
Path: /users/{user_id}
Payload: None
Headers:
- Authorization: Bearer <system_admin_token>
Expected Response:
- 200 OK: {"id": 1, "name": "...", "email": "...", "role": "...", "created_at": "...", "updated_at": null}
- 403 Forbidden: {"detail": "System admin access required"} (if not system_admin)
- 404 Not Found: {"detail": "User not found"}
Notes: Only system_admin can access.

# 7. Get All Users (requires system_admin token)
Method: GET
Path: /users/
Payload: None
Headers:
- Authorization: Bearer <system_admin_token>
Expected Response:
- 200 OK: [{"id": 1, "name": "...", "email": "...", "role": "...", "created_at": "...", "updated_at": null}, ...]
- 403 Forbidden: {"detail": "System admin access required"} (if not system_admin)
Notes: Only system_admin can list all users.

# 8. Update Current User (requires any valid token)
Method: PUT
Path: /users/me
Payload:
{
    "name": "Updated Name",
    "email": "updated@example.com",
    "password": "newpassword123"
}
Headers:
- Content-Type: application/json
- Authorization: Bearer <any_token>
Expected Response:
- 200 OK: {"id": 1, "name": "Updated Name", "email": "updated@example.com", "role": "...", "created_at": "...", "updated_at": "..."}
- 404 Not Found: {"detail": "User not found"}
Notes: All roles can update their own name, email, password. Role cannot be updated.

# 9. Delete User (requires system_admin token)
Method: DELETE
Path: /users/{user_id}
Payload: None
Headers:
- Authorization: Bearer <system_admin_token>
Expected Response:
- 200 OK: {"message": "User deleted"}
- 403 Forbidden: {"detail": "System admin access required"} (if not system_admin)
- 404 Not Found: {"detail": "User not found"}
Notes: Only system_admin can delete users.

# 10. Create Person (requires hr_admin token)
Method: POST
Path: /persons/
Payload:
{
    "username": "person1",
    "password": "personpass123",
    "personal_id_number": "1234567890123",
    "first_name": "John",
    "middle_name": null,
    "last_name": "Doe",
    "nick_name": "Johnny",
    "birth_date": "1990-01-01",
    "gender_type_id": 1,
    "marital_status_type_id": 1,
    "country_id": 1,
    "height": 175,
    "weight": 70,
    "ethnicity_type_id": 1,
    "income_range_id": 1,
    "comment": "Test person"
}
Headers:
- Content-Type: application/json
- Authorization: Bearer <hr_admin_token>
Expected Response:
- 200 OK: {"id": 1, "username": "person1", ...}
- 400 Bad Request: {"detail": "Person already exists"}
- 403 Forbidden: {"detail": "HR admin access required"}
Notes: Only hr_admin can create persons.

# 11. Get Person by ID (requires hr_admin token)
Method: GET
Path: /persons/{person_id}
Payload: None
Headers:
- Authorization: Bearer <hr_admin_token>
Expected Response:
- 200 OK: {"id": 1, "username": "person1", ...}
- 403 Forbidden: {"detail": "HR admin access required"}
- 404 Not Found: {"detail": "Person not found"}
Notes: Only hr_admin can access.

# 12. Update Person (requires hr_admin token)
Method: PUT
Path: /persons/{person_id}
Payload:
{
    "username": "updated_person",
    "password": "newpass123",
    "first_name": "Jane"
}
Headers:
- Content-Type: application/json
- Authorization: Bearer <hr_admin_token>
Expected Response:
- 200 OK: {"id": 1, "username": "updated_person", ...}
- 403 Forbidden: {"detail": "HR admin access required"}
- 404 Not Found: {"detail": "Person not found"}
Notes: Only hr_admin can update. Updates are logged in person_history.

# 13. Delete Person (requires hr_admin token)
Method: DELETE
Path: /persons/{person_id}
Payload: None
Headers:
- Authorization: Bearer <hr_admin_token>
Expected Response:
- 200 OK: {"message": "Person deleted"}
- 403 Forbidden: {"detail": "HR admin access required"}
- 404 Not Found: {"detail": "Person not found"}
Notes: Only hr_admin can delete. Deletion is logged in person_history.

# 14. Create Organization (requires organization_admin token)
Method: POST
Path: /organizations/
Payload:
{
    "federal_tax_id": "123456789",
    "name_en": "Test Org",
    "name_th": "องค์กรทดสอบ",
    "organization_type_id": 1
}
Headers:
- Content-Type: application/json
- Authorization: Bearer <organization_admin_token>
Expected Response:
- 200 OK: {"id": 1, "name_en": "Test Org", ...}
- 400 Bad Request: {"detail": "Organization already exists"}
- 403 Forbidden: {"detail": "Organization admin access required"}
Notes: Only organization_admin can create organizations.

# 15. Get Organization by ID (requires organization_admin token)
Method: GET
Path: /organizations/{organization_id}
Payload: None
Headers:
- Authorization: Bearer <organization_admin_token>
Expected Response:
- 200 OK: {"id": 1, "name_en": "Test Org", ...}
- 403 Forbidden: {"detail": "Organization admin access required"}
- 404 Not Found: {"detail": "Organization not found"}
Notes: Only organization_admin can access.

# 16. Update Organization (requires organization_admin token)
Method: PUT
Path: /organizations/{organization_id}
Payload:
{
    "name_en": "Updated Org",
    "name_th": "องค์กรอัพเดท"
}
Headers:
- Content-Type: application/json
- Authorization: Bearer <organization_admin_token>
Expected Response:
- 200 OK: {"id": 1, "name_en": "Updated Org", ...}
- 403 Forbidden: {"detail": "Organization admin access required"}
- 404 Not Found: {"detail": "Organization not found"}
Notes: Only organization_admin can update. Updates are logged in organization_history.

# 17. Delete Organization (requires organization_admin token)
Method: DELETE
Path: /organizations/{organization_id}
Payload: None
Headers:
- Authorization: Bearer <organization_admin_token>
Expected Response:
- 200 OK: {"message": "Organization deleted"}
- 403 Forbidden: {"detail": "Organization admin access required"}
- 404 Not Found: {"detail": "Organization not found"}
Notes: Only organization_admin can delete. Deletion is logged in organization_history.

# Test Flow:
1. Use /auth/register to create a system_admin user.
2. Login as system_admin to get token.
3. Use system_admin token to create basetype_admin.
4. Use basetype_admin token to create hr_admin and organization_admin.
5. Login as hr_admin to create and manage persons.
6. Login as organization_admin to create and manage organizations.
7. Test /users/me with all role tokens.
8. Test /users/ and /users/{id} with system_admin token (should work) and other roles (should fail with 403).
9. Test person and organization endpoints with respective admin tokens.
10. Verify person_history and organization_history tables for create/update/delete actions.
11. Test edge cases: duplicate emails/usernames, invalid tokens, non-existent IDs, invalid foreign keys.

# Notes:
- Populate gender_types, marital_status_types, countries, ethnicity_types, income_ranges, organization_types tables with sample data before testing.
- Use Postman environment variables for tokens and IDs.
- Verify timestamps in responses and history tables.
- Test invalid payloads (e.g., invalid email, missing required fields) to ensure validation works.
- Ensure role-based access control is strictly enforced.
```
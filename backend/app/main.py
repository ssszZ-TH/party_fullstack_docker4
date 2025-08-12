from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config.database import database
from app.controllers.auth.auth import router as auth_router
from app.controllers.users.user import router as user_router
from app.controllers.persons.person import router as person_router
from app.controllers.organizations.organization import router as organization_router
from app.controllers.gendertype import router as gendertype_router
from app.controllers.marital_status_type import router as marital_status_type_router
from app.controllers.country import router as country_router
from app.controllers.ethnicity_type import router as ethnicity_type_router
from app.controllers.income_range import router as income_range_router
from app.controllers.organization_type import router as organization_type_router
from app.controllers.industry_type import router as industry_type_router
from app.controllers.employee_count_range import router as employee_count_range_router

load_dotenv()

# https://fastapi.tiangolo.com/advanced/events/#lifespan

# Define lifespan event handler for FastAPI application
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the database when the application starts
    await database.connect()
    # Yield control back to FastAPI to handle requests
    yield
    # Disconnect from the database when the application shuts down
    await database.disconnect()

# Initialize FastAPI app with lifespan event handler
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(person_router)
app.include_router(organization_router)
app.include_router(gendertype_router)
app.include_router(marital_status_type_router)
app.include_router(country_router)
app.include_router(ethnicity_type_router)
app.include_router(income_range_router)
app.include_router(organization_type_router)
app.include_router(industry_type_router)
app.include_router(employee_count_range_router)

@app.get("/")
async def root():
    return {"message": "FastAPI Backend", "github": "https://github.com/ssszZ-TH/party_fullstack_docker4"}
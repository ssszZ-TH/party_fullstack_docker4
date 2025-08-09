from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import database
from app.controllers.auth.auth import router as auth_router



# โหลด .env ก่อน import อื่นๆ
load_dotenv()

app = FastAPI()

# CORS สำหรับ frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# รวม routers
app.include_router(auth_router)


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message": "FastAPI Backend","github":"https://github.com/ssszZ-TH/party_fullstack_docker3"}
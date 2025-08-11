import jwt 
SECRET_KEY = "8c2f7a9b3d6e1f0c4a8b2d5e7f9a1c3b6d8e0f2a4b7c9d1e3f5a8b0c2d4e6f"
ALGORITHM = "HS256"
SAMPLE_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0Iiwicm9sZSI6Im9yZ2FuaXphdGlvbl9hZG1pbiIsImV4cCI6MTc1NDkxNzU1Mn0.RZ-daaDsBpWSAWaOFpHm2NaSfOvNU6jEtyOkQcC8Pgo"

payload = jwt.decode(SAMPLE_JWT_TOKEN, SECRET_KEY, algorithms=[ALGORITHM])
print(payload)
import jwt

# กำหนดค่าคงที่ (constants) ที่ต้องใช้ในการสร้าง token
# ค่าเหล่านี้ต้องเหมือนกับที่ใช้ในการถอดรหัส (decoder) ด้วยนะคะ
SECRET_KEY = "8c2f7a9b3d6e1f0c4a8b2d5e7f9a1c3b6d8e0f2a4b7c9d1e3f5a8b0c2d4e6f"
ALGORITHM = "HS256"
to_encode = {"sub": "i love F16", "role": "fuckyou"}

encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
print(encoded_jwt)
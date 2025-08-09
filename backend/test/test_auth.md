# Test Plan for FastAPI Backend using Postman
# Date: August 09, 2025

# 1. Register System Admin (Backdoor)
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
Notes: Create initial system_admin. Save token for further tests.

# 2. Login System Admin
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
- 200 OK: {"access_token": "<system_admin_token>", "token_type": "bearer"}
- 401 Unauthorized: {"detail": "Invalid credentials"}
Notes: Save system_admin_token for creating other users.

# 3. Create Basetype Admin
Method: POST
Path: /users/
Payload:
{
    "name": "Basetype Admin",
    "email": "basetypeadmin@example.com",
    "password": "basepassword123",
    "role": "basetype_admin"
}
Headers:
- Content-Type: application/json
- Authorization: Bearer <system_admin_token>
Expected Response:
- 200 OK: {"id": 2, "name": "Basetype Admin", "email": "basetypeadmin@example.com", "role": "basetype_admin", "created_at": "...", "updated_at": null}
- 400 Bad Request: {"detail": "Email already exists"}
- 403 Forbidden: {"detail": "System admin access required"}
- 422 Unprocessable Entity: {"detail": "Role must be one of ['system_admin', 'basetype_admin', 'hr_admin', 'organization_admin']"}
Notes: Only system_admin can create users.

# 4. Create HR Admin
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
- Authorization: Bearer <system_admin_token>
Expected Response:
- 200 OK: {"id": 3, "name": "HR Admin", "email": "hradmin@example.com", "role": "hr_admin", "created_at": "...", "updated_at": null}
- 400 Bad Request: {"detail": "Email already exists"}
- 403 Forbidden: {"detail": "System admin access required"}
- 422 Unprocessable Entity: {"detail": "Role must be one of ['system_admin', 'basetype_admin', 'hr_admin', 'organization_admin']"}
Notes: Only system_admin can create users.

# 5. Create Organization Admin
Method: POST
Path: /users/
Payload:
{
    "name": "Org Admin",
    "email": "orgadmin@example.com",
    "password": "orgpassword123",
    "role": "organization_admin"
}
Headers:
- Content-Type: application/json
- Authorization: Bearer <system_admin_token>
Expected Response:
- 200 OK: {"id": 4, "name": "Org Admin", "email": "orgadmin@example.com", "role": "organization_admin", "created_at": "...", "updated_at": null}
- 400 Bad Request: {"detail": "Email already exists"}
- 403 Forbidden: {"detail": "System admin access required"}
- 422 Unprocessable Entity: {"detail": "Role must be one of ['system_admin', 'basetype_admin', 'hr_admin', 'organization_admin']"}
Notes: Only system_admin can create users.

# 6. Login Basetype Admin
Method: POST
Path: /auth/login
Payload:
{
    "email": "basetypeadmin@example.com",
    "password": "basepassword123"
}
Headers:
- Content-Type: application/json
Expected Response:
- 200 OK: {"access_token": "<basetype_admin_token>", "token_type": "bearer"}
- 401 Unauthorized: {"detail": "Invalid credentials"}
Notes: Save basetype_admin_token for tests.

# 7. Login HR Admin
Method: POST
Path: /auth/login
Payload:
{
    "email": "hradmin@example.com",
    "password": "hrpassword123"
}
Headers:
- Content-Type: application/json
Expected Response:
- 200 OK: {"access_token": "<hr_admin_token>", "token_type": "bearer"}
- 401 Unauthorized: {"detail": "Invalid credentials"}
Notes: Save hr_admin_token for tests.

# 8. Login Organization Admin
Method: POST
Path: /auth/login
Payload:
{
    "email": "orgadmin@example.com",
    "password": "orgpassword123"
}
Headers:
- Content-Type: application/json
Expected Response:
- 200 OK: {"access_token": "<org_admin_token>", "token_type": "bearer"}
- 401 Unauthorized: {"detail": "Invalid credentials"}
Notes: Save org_admin_token for tests.

# 9. Get All Users (System Admin)
Method: GET
Path: /users/
Payload: None
Headers:
- Authorization: Bearer <system_admin_token>
Expected Response:
- 200 OK: [{"id": 1, "name": "System Admin", ...}, {"id": 2, "name": "Basetype Admin", ...}, ...]
- 403 Forbidden: {"detail": "System admin access required"}
Notes: Only system_admin can list all users.

# 10. Get User by ID (System Admin)
Method: GET
Path: /users/2
Payload: None
Headers:
- Authorization: Bearer <system_admin_token>
Expected Response:
- 200 OK: {"id": 2, "name": "Basetype Admin", "email": "basetypeadmin@example.com", "role": "basetype_admin", ...}
- 403 Forbidden: {"detail": "System admin access required"}
- 404 Not Found: {"detail": "User not found"}
Notes: Only system_admin can get user by ID.

# 11. Get Current User (System Admin)
Method: GET
Path: /users/me
Payload: None
Headers:
- Authorization: Bearer <system_admin_token>
Expected Response:
- 200 OK: {"id": 1, "name": "System Admin", "email": "sysadmin@example.com", "role": "system_admin", ...}
- 401 Unauthorized: {"detail": "Invalid token"}
- 404 Not Found: {"detail": "User not found"}
Notes: System_admin gets own data.

# 12. Get Current User (Basetype Admin)
Method: GET
Path: /users/me
Payload: None
Headers:
- Authorization: Bearer <basetype_admin_token>
Expected Response:
- 200 OK: {"id": 2, "name": "Basetype Admin", "email": "basetypeadmin@example.com", "role": "basetype_admin", ...}
- 401 Unauthorized: {"detail": "Invalid token"}
- 404 Not Found: {"detail": "User not found"}
Notes: Basetype_admin gets own data.

# 13. Get Current User (HR Admin)
Method: GET
Path: /users/me
Payload: None
Headers:
- Authorization: Bearer <hr_admin_token>
Expected Response:
- 200 OK: {"id": 3, "name": "HR Admin", "email": "hradmin@example.com", "role": "hr_admin", ...}
- 401 Unauthorized: {"detail": "Invalid token"}
- 404 Not Found: {"detail": "User not found"}
Notes: HR_admin gets own data.

# 14. Get Current User (Organization Admin)
Method: GET
Path: /users/me
Payload: None
Headers:
- Authorization: Bearer <org_admin_token>
Expected Response:
- 200 OK: {"id": 4, "name": "Org Admin", "email": "orgadmin@example.com", "role": "organization_admin", ...}
- 401 Unauthorized: {"detail": "Invalid token"}
- 404 Not Found: {"detail": "User not found"}
Notes: Organization_admin gets own data.

# 15. Update Current User (System Admin)
Method: PUT
Path: /users/me
Payload:
{
    "name": "Updated System Admin",
    "email": "updated_sysadmin@example.com",
    "password": "newsyspassword123"
}
Headers:
- Content-Type: application/json
- Authorization: Bearer <system_admin_token>
Expected Response:
- 200 OK: {"id": 1, "name": "Updated System Admin", "email": "updated_sysadmin@example.com", ...}
- 404 Not Found: {"detail": "User not found"}
Notes: System_admin updates own data.

# 16. Update Other User (System Admin)
Method: PUT
Path: /users/2
Payload:
{
    "name": "Updated Basetype Admin",
    "email": "updated_basetypeadmin@example.com"
}
Headers:
- Content-Type: application/json
- Authorization: Bearer <system_admin_token>
Expected Response:
- 200 OK: {"id": 2, "name": "Updated Basetype Admin", "email": "updated_basetypeadmin@example.com", ...}
- 403 Forbidden: {"detail": "System admin access required"}
- 404 Not Found: {"detail": "User not found"}
Notes: System_admin updates basetype_admin.

# 17. Update Current User (Basetype Admin)
Method: PUT
Path: /users/me
Payload:
{
    "name": "Updated Basetype Admin",
    "email": "updated_basetypeadmin@example.com"
}
Headers:
- Content-Type: application/json
- Authorization: Bearer <basetype_admin_token>
Expected Response:
- 200 OK: {"id": 2, "name": "Updated Basetype Admin", "email": "updated_basetypeadmin@example.com", ...}
- 404 Not Found: {"detail": "User not found"}
Notes: Basetype_admin updates own data.

# 18. Update Current User (HR Admin)
Method: PUT
Path: /users/me
Payload:
{
    "name": "Updated HR Admin",
    "email": "updated_hradmin@example.com"
}
Headers:
- Content-Type: application/json
- Authorization: Bearer <hr_admin_token>
Expected Response:
- 200 OK: {"id": 3, "name": "Updated HR Admin", "email": "updated_hradmin@example.com", ...}
- 404 Not Found: {"detail": "User not found"}
Notes: HR_admin updates own data.

# 19. Update Current User (Organization Admin)
Method: PUT
Path: /users/me
Payload:
{
    "name": "Updated Org Admin",
    "email": "updated_orgadmin@example.com"
}
Headers:
- Content-Type: application/json
- Authorization: Bearer <org_admin_token>
Expected Response:
- 200 OK: {"id": 4, "name": "Updated Org Admin", "email": "updated_orgadmin@example.com", ...}
- 404 Not Found: {"detail": "User not found"}
Notes: Organization_admin updates own data.

# 20. Delete Other User (System Admin)
Method: DELETE
Path: /users/2
Payload: None
Headers:
- Authorization: Bearer <system_admin_token>
Expected Response:
- 200 OK: {"message": "User deleted"}
- 403 Forbidden: {"detail": "System admin access required"}
- 404 Not Found: {"detail": "User not found"}
Notes: System_admin deletes basetype_admin.

# 21. Delete Self (System Admin)
Method: DELETE
Path: /users/me
Payload: None
Headers:
- Authorization: Bearer <system_admin_token>
Expected Response:
- 200 OK: {"message": "User deleted"}
- 404 Not Found: {"detail": "User not found"}
Notes: System_admin deletes self.

# 22. Delete Self (Basetype Admin)
Method: DELETE
Path: /users/me
Payload: None
Headers:
- Authorization: Bearer <basetype_admin_token>
Expected Response:
- 200 OK: {"message": "User deleted"}
- 404 Not Found: {"detail": "User not found"}
Notes: Basetype_admin deletes self.

# 23. Delete Self (HR Admin)
Method: DELETE
Path: /users/me
Payload: None
Headers:
- Authorization: Bearer <hr_admin_token>
Expected Response:
- 200 OK: {"message": "User deleted"}
- 404 Not Found: {"detail": "User not found"}
Notes: HR_admin deletes self.

# 24. Delete Self (Organization Admin)
Method: DELETE
Path: /users/me
Payload: None
Headers:
- Authorization: Bearer <org_admin_token>
Expected Response:
- 200 OK: {"message": "User deleted"}
- 404 Not Found: {"detail": "User not found"}
Notes: Organization_admin deletes self.

# Test Flow:
1. Register system_admin via /auth/register.
2. Login system_admin to get token.
3. Use system_admin token to create basetype_admin, hr_admin, organization_admin.
4. Login each admin role to get respective tokens.
5. Test read operations: system_admin lists all users, gets user by ID, gets self; other roles test /users/me.
6. Test update operations: system_admin updates self and others; other roles update self.
7. Test delete operations: system_admin deletes others and self; other roles delete self.
8. Test edge cases: duplicate emails, invalid roles, invalid tokens, non-existent IDs.

# Notes:
- Use Postman environment variables for tokens and IDs.
- Verify timestamps in responses.
- Test invalid payloads (e.g., invalid email, missing fields).
- Ensure role-based access control is enforced (e.g., non-system_admin cannot create/delete users).
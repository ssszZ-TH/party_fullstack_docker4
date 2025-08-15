# Test Plan for Passport Endpoints

Base URL: `{{backend}}/`

## Notes
- Content-Type: `application/json`
- Token format: `Authorization: Bearer {{admin_token}}`
- `{{admin_token}}`: Token from user login with `hr_admin` role
- Replace `{{id}}` with actual passport ID
- Replace `{{person_id}}` with actual person ID from persons table

## Passport Endpoints
1. **Create Passport**
   - **Method**: POST
   - **Path**: `/passports/`
   - **Token/Role**: `{{admin_token}}` (hr_admin)
   - **JSON Body**:
     ```json
     {
         "passport_id_number": "123456789",
         "issue_date": "2023-01-01",
         "expire_date": "2033-01-01",
         "person_id": {{person_id}}
     }
     ```

2. **Get Passport by ID**
   - **Method**: GET
   - **Path**: `/passports/{{id}}`
   - **Token/Role**: `{{admin_token}}` (hr_admin)
   - **JSON Body**: None

3. **List All Passports**
   - **Method**: GET
   - **Path**: `/passports/`
   - **Token/Role**: `{{admin_token}}` (hr_admin)
   - **JSON Body**: None

4. **Update Passport**
   - **Method**: PUT
   - **Path**: `/passports/{{id}}`
   - **Token/Role**: `{{admin_token}}` (hr_admin)
   - **JSON Body**:
     ```json
     {
         "passport_id_number": "987654321",
         "issue_date": "2024-01-01",
         "expire_date": "2034-01-01",
         "person_id": {{person_id}}
     }
     ```

5. **Delete Passport**
   - **Method**: DELETE
   - **Path**: `/passports/{{id}}`
   - **Token/Role**: `{{admin_token}}` (hr_admin)
   - **JSON Body**: None
   - **Expected Response**: 
     ```json
     {"message": "Passport deleted"}
     ```
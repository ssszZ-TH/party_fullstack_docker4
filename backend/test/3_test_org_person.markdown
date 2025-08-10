# Test Plan for Organization and Person Endpoints

Base URL: `{{backend}}/`

## Notes
- Content-Type: `application/json`
- Token format: `Authorization: Bearer {{token}}`
- Replace `{{org_id}}`, `{{person_id}}` with actual IDs
- `{{admin_token}}`: Token from user login with `organization_admin` or `hr_admin` role
- `{{org_token}}`: Token from organization login
- `{{person_token}}`: Token from person login

## Organization Endpoints

1. **Create Organization**
   - **Method**: POST
   - **Path**: `/organizations/`
   - **Token/Role**: `{{admin_token}}` (organization_admin)
   - **JSON Body**:
     ```json
     {
       "federal_tax_id": "123456789",
       "name_en": "Test Org",
       "name_th": "องค์กรทดสอบ",
       "organization_type_id": null,
       "industry_type_id": null,
       "employee_count_range_id": null,
       "username": "testorg",
       "password": "securepassword",
       "comment": "Test comment"
     }
     ```

2. **Organization Login**
   - **Method**: POST
   - **Path**: `/organizations/login`
   - **Token/Role**: None (organization_user)
   - **JSON Body**:
     ```json
     {
       "username": "testorg",
       "password": "securepassword"
     }
     ```

3. **Get Current Organization**
   - **Method**: GET
   - **Path**: `/organizations/me`
   - **Token/Role**: `{{org_token}}` (organization_user)
   - **JSON Body**: None

4. **Get Organization by ID**
   - **Method**: GET
   - **Path**: `/organizations/{{org_id}}`
   - **Token/Role**: `{{admin_token}}` (organization_admin)
   - **JSON Body**: None

5. **List All Organizations**
   - **Method**: GET
   - **Path**: `/organizations/`
   - **Token/Role**: `{{admin_token}}` (organization_admin)
   - **JSON Body**: None

6. **Update Organization**
   - **Method**: PUT
   - **Path**: `/organizations/{{org_id}}`
   - **Token/Role**: `{{admin_token}}` (organization_admin)
   - **JSON Body**:
     ```json
     {
       "name_en": "Updated Org",
       "name_th": "องค์กรอัปเดต",
       "comment": "Updated comment"
     }
     ```

7. **Delete Organization**
   - **Method**: DELETE
   - **Path**: `/organizations/{{org_id}}`
   - **Token/Role**: `{{admin_token}}` (organization_admin)
   - **JSON Body**: None

## Person Endpoints

1. **Create Person**
   - **Method**: POST
   - **Path**: `/persons/`
   - **Token/Role**: `{{admin_token}}` (hr_admin)
   - **JSON Body**:
     ```json
     {
       "username": "testperson",
       "password": "securepassword",
       "personal_id_number": "1234567890123",
       "first_name": "John",
       "last_name": "Doe",
       "birth_date": "1990-01-01",
       "gender_type_id": null,
       "marital_status_type_id": null,
       "country_id": null,
       "height": 175,
       "weight": 70,
       "ethnicity_type_id": null,
       "income_range_id": null,
       "comment": "Test comment"
     }
     ```

2. **Person Login**
   - **Method**: POST
   - **Path**: `/persons/login`
   - **Token/Role**: None (person_user)
   - **JSON Body**:
     ```json
     {
       "username": "testperson",
       "password": "securepassword"
     }
     ```

3. **Get Current Person**
   - **Method**: GET
   - **Path**: `/persons/me`
   - **Token/Role**: `{{person_token}}` (person_user)
   - **JSON Body**: None

4. **Get Person by ID**
   - **Method**: GET
   - **Path**: `/persons/{{person_id}}`
   - **Token/Role**: `{{admin_token}}` (hr_admin)
   - **JSON Body**: None

5. **List All Persons**
   - **Method**: GET
   - **Path**: `/persons/`
   - **Token/Role**: `{{admin_token}}` (hr_admin)
   - **JSON Body**: None

6. **Update Person**
   - **Method**: PUT
   - **Path**: `/persons/{{person_id}}`
   - **Token/Role**: `{{admin_token}}` (hr_admin)
   - **JSON Body**:
     ```json
     {
       "first_name": "Jane",
       "last_name": "Doe",
       "comment": "Updated comment"
     }
     ```

7. **Delete Person**
   - **Method**: DELETE
   - **Path**: `/persons/{{person_id}}`
   - **Token/Role**: `{{admin_token}}` (hr_admin)
   - **JSON Body**: None
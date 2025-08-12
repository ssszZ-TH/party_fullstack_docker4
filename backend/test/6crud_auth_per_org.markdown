# Test Plan for Base Type Endpoints

Base URL: `{{backend}}/`

## Notes
- Content-Type: `application/json`
- Token format: `Authorization: Bearer {{admin_token}}`
- `{{admin_token}}`: Token from user login with `basetype_admin` role
- Replace `{{id}}` with actual ID for each type

## Gender Type Endpoints
1. **Create Gender Type**
   - **Method**: POST
   - **Path**: `/gender_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Male"}
     ```

2. **Get Gender Type by ID**
   - **Method**: GET
   - **Path**: `/gender_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

3. **List All Gender Types**
   - **Method**: GET
   - **Path**: `/gender_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

4. **Update Gender Type**
   - **Method**: PUT
   - **Path**: `/gender_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Updated Male"}
     ```

5. **Delete Gender Type**
   - **Method**: DELETE
   - **Path**: `/gender_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

## Marital Status Type Endpoints
1. **Create Marital Status Type**
   - **Method**: POST
   - **Path**: `/marital_status_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Single"}
     ```

2. **Get Marital Status Type by ID**
   - **Method**: GET
   - **Path**: `/marital_status_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

3. **List All Marital Status Types**
   - **Method**: GET
   - **Path**: `/marital_status_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

4. **Update Marital Status Type**
   - **Method**: PUT
   - **Path**: `/marital_status_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Updated Single"}
     ```

5. **Delete Marital Status Type**
   - **Method**: DELETE
   - **Path**: `/marital_status_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

## Country Endpoints
1. **Create Country**
   - **Method**: POST
   - **Path**: `/countries/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"iso_code": "TH", "name_en": "Thailand", "name_th": "ประเทศไทย"}
     ```

2. **Get Country by ID**
   - **Method**: GET
   - **Path**: `/countries/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

3. **List All Countries**
   - **Method**: GET
   - **Path**: `/countries/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

4. **Update Country**
   - **Method**: PUT
   - **Path**: `/countries/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"name_en": "Updated Thailand"}
     ```

5. **Delete Country**
   - **Method**:
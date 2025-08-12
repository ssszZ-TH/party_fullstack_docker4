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
   - **Method**: DELETE
   - **Path**: `/countries/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

## Ethnicity Type Endpoints
1. **Create Ethnicity Type**
   - **Method**: POST
   - **Path**: `/ethnicity_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Thai"}
     ```

2. **Get Ethnicity Type by ID**
   - **Method**: GET
   - **Path**: `/ethnicity_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

3. **List All Ethnicity Types**
   - **Method**: GET
   - **Path**: `/ethnicity_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

4. **Update Ethnicity Type**
   - **Method**: PUT
   - **Path**: `/ethnicity_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Updated Thai"}
     ```

5. **Delete Ethnicity Type**
   - **Method**: DELETE
   - **Path**: `/ethnicity_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

## Income Range Endpoints
1. **Create Income Range**
   - **Method**: POST
   - **Path**: `/income_ranges/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "0-10000"}
     ```

2. **Get Income Range by ID**
   - **Method**: GET
   - **Path**: `/income_ranges/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

3. **List All Income Ranges**
   - **Method**: GET
   - **Path**: `/income_ranges/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

4. **Update Income Range**
   - **Method**: PUT
   - **Path**: `/income_ranges/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Updated 0-10000"}
     ```

5. **Delete Income Range**
   - **Method**: DELETE
   - **Path**: `/income_ranges/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

## Organization Type Endpoints
1. **Create Organization Type**
   - **Method**: POST
   - **Path**: `/organization_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Corporation"}
     ```

2. **Get Organization Type by ID**
   - **Method**: GET
   - **Path**: `/organization_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

3. **List All Organization Types**
   - **Method**: GET
   - **Path**: `/organization_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

4. **Update Organization Type**
   - **Method**: PUT
   - **Path**: `/organization_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Updated Corporation"}
     ```

5. **Delete Organization Type**
   - **Method**: DELETE
   - **Path**: `/organization_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

## Industry Type Endpoints
1. **Create Industry Type**
   - **Method**: POST
   - **Path**: `/industry_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"naisc": "541511", "description": "Software Development"}
     ```

2. **Get Industry Type by ID**
   - **Method**: GET
   - **Path**: `/industry_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

3. **List All Industry Types**
   - **Method**: GET
   - **Path**: `/industry_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

4. **Update Industry Type**
   - **Method**: PUT
   - **Path**: `/industry_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Updated Software Development"}
     ```

5. **Delete Industry Type**
   - **Method**: DELETE
   - **Path**: `/industry_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

## Employee Count Range Endpoints
1. **Create Employee Count Range**
   - **Method**: POST
   - **Path**: `/employee_count_ranges/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "1-10"}
     ```

2. **Get Employee Count Range by ID**
   - **Method**: GET
   - **Path**: `/employee_count_ranges/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

3. **List All Employee Count Ranges**
   - **Method**: GET
   - **Path**: `/employee_count_ranges/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

4. **Update Employee Count Range**
   - **Method**: PUT
   - **Path**: `/employee_count_ranges/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Updated 1-10"}
     ```

5. **Delete Employee Count Range**
   - **Method**: DELETE
   - **Path**: `/employee_count_ranges/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None
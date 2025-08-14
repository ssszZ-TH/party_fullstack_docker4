# Test Plan for Base Type Endpoints

Base URL: `{{backend}}/`

## Notes
- Content-Type: `application/json`
- Token format: `Authorization: Bearer {{admin_token}}`
- `{{admin_token}}`: Token from user login with `basetype_admin` role
- Replace `{{id}}` with actual ID for each type

## Role Type Endpoints
1. **Create Role Type**
   - **Method**: POST
   - **Path**: `/role_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Admin"}
     ```

2. **Get Role Type by ID**
   - **Method**: GET
   - **Path**: `/role_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

3. **List All Role Types**
   - **Method**: GET
   - **Path**: `/role_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

4. **Update Role Type**
   - **Method**: PUT
   - **Path**: `/role_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Updated Admin"}
     ```

5. **Delete Role Type**
   - **Method**: DELETE
   - **Path**: `/role_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

## Relationship Type Endpoints
1. **Create Relationship Type**
   - **Method**: POST
   - **Path**: `/relationship_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Employee"}
     ```

2. **Get Relationship Type by ID**
   - **Method**: GET
   - **Path**: `/relationship_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

3. **List All Relationship Types**
   - **Method**: GET
   - **Path**: `/relationship_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

4. **Update Relationship Type**
   - **Method**: PUT
   - **Path**: `/relationship_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Updated Employee"}
     ```

5. **Delete Relationship Type**
   - **Method**: DELETE
   - **Path**: `/relationship_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

## Priority Type Endpoints
1. **Create Priority Type**
   - **Method**: POST
   - **Path**: `/priority_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "High"}
     ```

2. **Get Priority Type by ID**
   - **Method**: GET
   - **Path**: `/priority_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

3. **List All Priority Types**
   - **Method**: GET
   - **Path**: `/priority_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

4. **Update Priority Type**
   - **Method**: PUT
   - **Path**: `/priority_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Updated High"}
     ```

5. **Delete Priority Type**
   - **Method**: DELETE
   - **Path**: `/priority_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

## Role Relationship Status Type Endpoints
1. **Create Role Relationship Status Type**
   - **Method**: POST
   - **Path**: `/role_relationship_status_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Active"}
     ```

2. **Get Role Relationship Status Type by ID**
   - **Method**: GET
   - **Path**: `/role_relationship_status_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

3. **List All Role Relationship Status Types**
   - **Method**: GET
   - **Path**: `/role_relationship_status_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

4. **Update Role Relationship Status Type**
   - **Method**: PUT
   - **Path**: `/role_relationship_status_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Updated Active"}
     ```

5. **Delete Role Relationship Status Type**
   - **Method**: DELETE
   - **Path**: `/role_relationship_status_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

## Contact Mechanism Type Endpoints
1. **Create Contact Mechanism Type**
   - **Method**: POST
   - **Path**: `/contact_mechanism_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Email"}
     ```

2. **Get Contact Mechanism Type by ID**
   - **Method**: GET
   - **Path**: `/contact_mechanism_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

3. **List All Contact Mechanism Types**
   - **Method**: GET
   - **Path**: `/contact_mechanism_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

4. **Update Contact Mechanism Type**
   - **Method**: PUT
   - **Path**: `/contact_mechanism_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Updated Email"}
     ```

5. **Delete Contact Mechanism Type**
   - **Method**: DELETE
   - **Path**: `/contact_mechanism_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

## Communication Event Status Type Endpoints
1. **Create Communication Event Status Type**
   - **Method**: POST
   - **Path**: `/communication_event_status_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Completed"}
     ```

2. **Get Communication Event Status Type by ID**
   - **Method**: GET
   - **Path**: `/communication_event_status_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

3. **List All Communication Event Status Types**
   - **Method**: GET
   - **Path**: `/communication_event_status_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

4. **Update Communication Event Status Type**
   - **Method**: PUT
   - **Path**: `/communication_event_status_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Updated Completed"}
     ```

5. **Delete Communication Event Status Type**
   - **Method**: DELETE
   - **Path**: `/communication_event_status_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

## Communication Event Purpose Type Endpoints
1. **Create Communication Event Purpose Type**
   - **Method**: POST
   - **Path**: `/communication_event_purpose_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Follow-up"}
     ```

2. **Get Communication Event Purpose Type by ID**
   - **Method**: GET
   - **Path**: `/communication_event_purpose_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

3. **List All Communication Event Purpose Types**
   - **Method**: GET
   - **Path**: `/communication_event_purpose_types/`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None

4. **Update Communication Event Purpose Type**
   - **Method**: PUT
   - **Path**: `/communication_event_purpose_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**:
     ```json
     {"description": "Updated Follow-up"}
     ```

5. **Delete Communication Event Purpose Type**
   - **Method**: DELETE
   - **Path**: `/communication_event_purpose_types/{{id}}`
   - **Token/Role**: `{{admin_token}}` (basetype_admin)
   - **JSON Body**: None
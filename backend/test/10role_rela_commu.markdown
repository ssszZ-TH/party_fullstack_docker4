# Test Plan for CRUD Endpoints

Base URL: `{{backend}}/`

## Notes
- Content-Type: `application/json`
- Token format: `Authorization: Bearer {{user_token}}`
- `{{user_token}}`: Token from user login with `organization_user` or `person_user` role
- Replace `{{id}}` with actual record ID
- Replace `{{role_type_id}}`, `{{to_party_role_id}}`, `{{relationship_type_id}}`, `{{priority_type_id}}`, `{{role_relationship_status_type_id}}`, `{{contact_mechanism_type_id}}`, `{{communication_event_status_type_id}}`, `{{communication_event_id}}`, `{{communication_event_purpose_type_id}}` with valid IDs from respective tables
- All endpoints filter by `party_id` from JWT (`current_user["id"]`) for `party_role`, `communication_event`, and `communication_event_purpose`
- For `role_relationship`, `from_party_role_id` is set to `current_user["id"]` and filtered by `party_id` matching `from_party_role_id`

## Party Role Endpoints
1. **Create Party Role**
   - **Method**: POST
   - **Path**: `/party_role/`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**:
     ```json
     {
         "note": "Test role",
         "role_type_id": {{role_type_id}}
     }
     ```
   - **Expected Response**: Created party role details

2. **Get Party Role by ID**
   - **Method**: GET
   - **Path**: `/party_role/{{id}}`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**: None
   - **Expected Response**: Party role details or 404 if not found

3. **List All Party Roles**
   - **Method**: GET
   - **Path**: `/party_role/`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**: None
   - **Expected Response**: List of party roles for the user’s party_id

4. **Update Party Role**
   - **Method**: PUT
   - **Path**: `/party_role/{{id}}`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**:
     ```json
     {
         "note": "Updated role",
         "role_type_id": {{role_type_id}}
     }
     ```
   - **Expected Response**: Updated party role details or 404 if not found

5. **Delete Party Role**
   - **Method**: DELETE
   - **Path**: `/party_role/{{id}}`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**: None
   - **Expected Response**:
     ```json
     {"message": "Party role deleted"}
     ```

## Role Relationship Endpoints
1. **Create Role Relationship**
   - **Method**: POST
   - **Path**: `/role_relationship/`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**:
     ```json
     {
         "to_party_role_id": {{to_party_role_id}},
         "comment": "Test relationship",
         "relationship_type_id": {{relationship_type_id}},
         "priority_type_id": {{priority_type_id}},
         "role_relationship_status_type_id": {{role_relationship_status_type_id}}
     }
     ```
   - **Expected Response**: Created role relationship details with `from_party_role_id` set to user’s `party_id`

2. **Get Role Relationship by ID**
   - **Method**: GET
   - **Path**: `/role_relationship/{{id}}`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**: None
   - **Expected Response**: Role relationship details where `from_party_role_id` matches user’s `party_id` or 404 if not found

3. **List All Role Relationships**
   - **Method**: GET
   - **Path**: `/role_relationship/`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**: None
   - **Expected Response**: List of role relationships where `from_party_role_id` matches user’s `party_id`

4. **Update Role Relationship**
   - **Method**: PUT
   - **Path**: `/role_relationship/{{id}}`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**:
     ```json
     {
         "to_party_role_id": {{to_party_role_id}},
         "comment": "Updated relationship",
         "relationship_type_id": {{relationship_type_id}},
         "priority_type_id": {{priority_type_id}},
         "role_relationship_status_type_id": {{role_relationship_status_type_id}}
     }
     ```
   - **Expected Response**: Updated role relationship details with `from_party_role_id` set to user’s `party_id` or 404 if not found

5. **Delete Role Relationship**
   - **Method**: DELETE
   - **Path**: `/role_relationship/{{id}}`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**: None
   - **Expected Response**:
     ```json
     {"message": "Role relationship deleted"}
     ```

## Communication Event Endpoints
1. **Create Communication Event**
   - **Method**: POST
   - **Path**: `/communication_event/`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**:
     ```json
     {
         "note": "Test event",
         "role_relationship_id": {{role_relationship_id}},
         "contact_mechanism_type_id": {{contact_mechanism_type_id}},
         "communication_event_status_type_id": {{communication_event_status_type_id}}
     }
     ```
   - **Expected Response**: Created communication event details

2. **Get Communication Event by ID**
   - **Method**: GET
   - **Path**: `/communication_event/{{id}}`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**: None
   - **Expected Response**: Communication event details or 404 if not found

3. **List All Communication Events**
   - **Method**: GET
   - **Path**: `/communication_event/`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**: None
   - **Expected Response**: List of communication events linked to user’s party_id

4. **Update Communication Event**
   - **Method**: PUT
   - **Path**: `/communication_event/{{id}}`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**:
     ```json
     {
         "note": "Updated event",
         "role_relationship_id": {{role_relationship_id}},
         "contact_mechanism_type_id": {{contact_mechanism_type_id}},
         "communication_event_status_type_id": {{communication_event_status_type_id}}
     }
     ```
   - **Expected Response**: Updated communication event details or 404 if not found

5. **Delete Communication Event**
   - **Method**: DELETE
   - **Path**: `/communication_event/{{id}}`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**: None
   - **Expected Response**:
     ```json
     {"message": "Communication event deleted"}
     ```

## Communication Event Purpose Endpoints
1. **Create Communication Event Purpose**
   - **Method**: POST
   - **Path**: `/communication_event_purpose/`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**:
     ```json
     {
         "note": "Test purpose",
         "communication_event_id": {{communication_event_id}},
         "communication_event_purpose_type_id": {{communication_event_purpose_type_id}}
     }
     ```
   - **Expected Response**: Created communication event purpose details

2. **Get Communication Event Purpose by ID**
   - **Method**: GET
   - **Path**: `/communication_event_purpose/{{id}}`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**: None
   - **Expected Response**: Communication event purpose details or 404 if not found

3. **List All Communication Event Purposes**
   - **Method**: GET
   - **Path**: `/communication_event_purpose/`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**: None
   - **Expected Response**: List of communication event purposes linked to user’s party_id

4. **Update Communication Event Purpose**
   - **Method**: PUT
   - **Path**: `/communication_event_purpose/{{id}}`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**:
     ```json
     {
         "note": "Updated purpose",
         "communication_event_id": {{communication_event_id}},
         "communication_event_purpose_type_id": {{communication_event_purpose_type_id}}
     }
     ```
   - **Expected Response**: Updated communication event purpose details or 404 if not found

5. **Delete Communication Event Purpose**
   - **Method**: DELETE
   - **Path**: `/communication_event_purpose/{{id}}`
   - **Token/Role**: `{{user_token}}` (organization_user, person_user)
   - **JSON Body**: None
   - **Expected Response**:
     ```json
     {"message": "Communication event purpose deleted"}
     ```
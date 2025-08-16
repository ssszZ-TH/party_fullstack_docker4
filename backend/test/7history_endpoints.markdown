# Test Plan for History Endpoints

Base URL: `{{backend}}/`

## Notes
- Content-Type: `application/json`
- Token format: `Authorization: Bearer {{admin_token}}`
- `{{hr_admin_token}}`: Token from user login with `hr_admin` role
- `{{organization_admin_token}}`: Token from user login with `organization_admin` role
- Replace `{{history_id}}` with actual history record ID
- All endpoints require authentication with the specified roles

## Person History Endpoints
1. **Get Person History by ID**
   - **Method**: GET
   - **Path**: `/person_history/{{history_id}}`
   - **Token/Role**: `{{hr_admin_token}}` (hr_admin)
   - **JSON Body**: None
   - **Expected Response**: Person history details or 404 if not found

2. **List All Person Histories**
   - **Method**: GET
   - **Path**: `/person_history/`
   - **Token/Role**: `{{hr_admin_token}}` (hr_admin)
   - **JSON Body**: None
   - **Expected Response**: List of person history records

## Organization History Endpoints
1. **Get Organization History by ID**
   - **Method**: GET
   - **Path**: `/organization_history/{{history_id}}`
   - **Token/Role**: `{{organization_admin_token}}` (organization_admin)
   - **JSON Body**: None
   - **Expected Response**: Organization history details or 404 if not found

2. **List All Organization Histories**
   - **Method**: GET
   - **Path**: `/organization_history/`
   - **Token/Role**: `{{organization_admin_token}}` (organization_admin)
   - **JSON Body**: None
   - **Expected Response**: List of organization history records

## Passport History Endpoints
1. **Get Passport History by ID**
   - **Method**: GET
   - **Path**: `/passport_history/{{history_id}}`
   - **Token/Role**: `{{hr_admin_token}}` (hr_admin)
   - **JSON Body**: None
   - **Expected Response**: Passport history details or 404 if not found

2. **List All Passport Histories**
   - **Method**: GET
   - **Path**: `/passport_history/`
   - **Token/Role**: `{{hr_admin_token}}` (hr_admin)
   - **JSON Body**: None
   - **Expected Response**: List of passport history records

## Party Role History Endpoints
1. **Get Party Role History by ID**
   - **Method**: GET
   - **Path**: `/party_role_history/{{history_id}}`
   - **Token/Role**: `{{hr_admin_token}}` or `{{organization_admin_token}}` (hr_admin or organization_admin)
   - **JSON Body**: None
   - **Expected Response**: Party role history details or 404 if not found

2. **List All Party Role Histories**
   - **Method**: GET
   - **Path**: `/party_role_history/`
   - **Token/Role**: `{{hr_admin_token}}` or `{{organization_admin_token}}` (hr_admin or organization_admin)
   - **JSON Body**: None
   - **Expected Response**: List of party role history records

## Role Relationship History Endpoints
1. **Get Role Relationship History by ID**
   - **Method**: GET
   - **Path**: `/role_relationship_history/{{history_id}}`
   - **Token/Role**: `{{hr_admin_token}}` or `{{organization_admin_token}}` (hr_admin or organization_admin)
   - **JSON Body**: None
   - **Expected Response**: Role relationship history details or 404 if not found

2. **List All Role Relationship Histories**
   - **Method**: GET
   - **Path**: `/role_relationship_history/`
   - **Token/Role**: `{{hr_admin_token}}` or `{{organization_admin_token}}` (hr_admin or organization_admin)
   - **JSON Body**: None
   - **Expected Response**: List of role relationship history records

## Communication Event History Endpoints
1. **Get Communication Event History by ID**
   - **Method**: GET
   - **Path**: `/communication_event_history/{{history_id}}`
   - **Token/Role**: `{{hr_admin_token}}` or `{{organization_admin_token}}` (hr_admin or organization_admin)
   - **JSON Body**: None
   - **Expected Response**: Communication event history details or 404 if not found

2. **List All Communication Event Histories**
   - **Method**: GET
   - **Path**: `/communication_event_history/`
   - **Token/Role**: `{{hr_admin_token}}` or `{{organization_admin_token}}` (hr_admin or organization_admin)
   - **JSON Body**: None
   - **Expected Response**: List of communication event history records

## Communication Event Purpose History Endpoints
1. **Get Communication Event Purpose History by ID**
   - **Method**: GET
   - **Path**: `/communication_event_purpose_history/{{history_id}}`
   - **Token/Role**: `{{hr_admin_token}}` or `{{organization_admin_token}}` (hr_admin or organization_admin)
   - **JSON Body**: None
   - **Expected Response**: Communication event purpose history details or 404 if not found

2. **List All Communication Event Purpose Histories**
   - **Method**: GET
   - **Path**: `/communication_event_purpose_history/`
   - **Token/Role**: `{{hr_admin_token}}` or `{{organization_admin_token}}` (hr_admin or organization_admin)
   - **JSON Body**: None
   - **Expected Response**: List of communication event purpose history records
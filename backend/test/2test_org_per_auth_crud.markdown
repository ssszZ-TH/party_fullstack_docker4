# Test Plan for Organization and Person Endpoints

Base URL: `{{backend}}/`

## Notes
- All endpoints require JSON content type.
- Token is required for endpoints with authentication (specified below).
- Use `Authorization: Bearer {{token}}` in headers for authenticated requests.
- Replace `{{token}}` with JWT token from login endpoints.
- Replace `{{org_id}}` and `{{person_id}}` with actual IDs from created records.

## Organization Endpoints

### 1. Create Organization
- **Endpoint**: `POST {{backend}}/organizations/`
- **Role**: organization_admin
- **Token**: Required (from user login with organization_admin role)
- **Body**:
  ```json
  {
    "federal_tax_id": "123456789",
    "name_en": "Test Org",
    "name_th": "องค์กรทดสอบ",
    "organization_type_id": 1,
    "username": "testorg",
    "password": "securepassword"
  }
  ```
- **Expected**: 200, returns OrganizationOut
- **Steps**:
  1. Login as user with organization_admin role to get token.
  2. Set token in headers.
  3. Send POST request with body.
  4. Verify response contains organization ID and details.

### 2. Organization Login
- **Endpoint**: `POST {{backend}}/organizations/login`
- **Role**: organization_user
- **Token**: Not required
- **Body**:
  ```json
  {
    "username": "testorg",
    "password": "securepassword"
  }
  ```
- **Expected**: 200, returns access_token
- **Steps**:
  1. Send POST request with body.
  2. Verify response contains access_token and token_type "bearer".
  3. Save token for organization_user role.

### 3. Get Current Organization
- **Endpoint**: `GET {{backend}}/organizations/me`
- **Role**: organization_user
- **Token**: Required (from organization login)
- **Expected**: 200, returns OrganizationOut
- **Steps**:
  1. Use token from organization login.
  2. Send GET request.
  3. Verify response contains current organization details.

### 4. Get Organization by ID
- **Endpoint**: `GET {{backend}}/organizations/{{org_id}}`
- **Role**: organization_user (own data only)
- **Token**: Required (from organization login)
- **Expected**: 200, returns OrganizationOut; 403 if not own data
- **Steps**:
  1. Use token from organization login.
  2. Send GET request with valid org_id.
  3. Verify response contains organization details.
  4. Test with another org_id to verify 403 error.

### 5. List All Organizations
- **Endpoint**: `GET {{backend}}/organizations/`
- **Role**: organization_admin
- **Token**: Required (from user login with organization_admin role)
- **Expected**: 200, returns list of OrganizationOut
- **Steps**:
  1. Login as user with organization_admin role to get token.
  2. Set token in headers.
  3. Send GET request.
  4. Verify response contains list of organizations.

### 6. Update Organization
- **Endpoint**: `PUT {{backend}}/organizations/{{org_id}}`
- **Role**: organization_admin
- **Token**: Required (from user login with organization_admin role)
- **Body**:
  ```json
  {
    "name_en": "Updated Org",
    "name_th": "องค์กรอัปเดต"
  }
  ```
- **Expected**: 200, returns updated OrganizationOut
- **Steps**:
  1. Login as user with organization_admin role to get token.
  2. Set token in headers.
  3. Send PUT request with body and valid org_id.
  4. Verify response contains updated organization details.

### 7. Delete Organization
- **Endpoint**: `DELETE {{backend}}/organizations/{{org_id}}`
- **Role**: organization_admin
- **Token**: Required (from user login with organization_admin role)
- **Expected**: 200, returns {"message": "Organization deleted"}
- **Steps**:
  1. Login as user with organization_admin role to get token.
  2. Set token in headers.
  3. Send DELETE request with valid org_id.
  4. Verify response contains success message.

## Person Endpoints

### 1. Create Person
- **Endpoint**: `POST {{backend}}/persons/`
- **Role**: hr_admin
- **Token**: Required (from user login with hr_admin role)
- **Body**:
  ```json
  {
    "username": "testperson",
    "password": "securepassword",
    "personal_id_number": "1234567890123",
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "1990-01-01",
    "gender_type_id": 1,
    "marital_status_type_id": 1,
    "country_id": 1,
    "height": 175,
    "weight": 70,
    "ethnicity_type_id": 1,
    "income_range_id": 1
  }
  ```
- **Expected**: 200, returns PersonOut
- **Steps**:
  1. Login as user with hr_admin role to get token.
  2. Set token in headers.
  3. Send POST request with body.
  4. Verify response contains person ID and details.

### 2. Person Login
- **Endpoint**: `POST {{backend}}/persons/login`
- **Role**: person_user
- **Token**: Not required
- **Body**:
  ```json
  {
    "username": "testperson",
    "password": "securepassword"
  }
  ```
- **Expected**: 200, returns access_token
- **Steps**:
  1. Send POST request with body.
  2. Verify response contains access_token and token_type "bearer".
  3. Save token for person_user role.

### 3. Get Current Person
- **Endpoint**: `GET {{backend}}/persons/me`
- **Role**: person_user
- **Token**: Required (from person login)
- **Expected**: 200, returns PersonOut
- **Steps**:
  1. Use token from person login.
  2. Send GET request.
  3. Verify response contains current person details.

### 4. Get Person by ID
- **Endpoint**: `GET {{backend}}/persons/{{person_id}}`
- **Role**: hr_admin
- **Token**: Required (from user login with hr_admin role)
- **Expected**: 200, returns PersonOut
- **Steps**:
  1. Login as user with hr_admin role to get token.
  2. Set token in headers.
  3. Send GET request with valid person_id.
  4. Verify response contains person details.

### 5. List All Persons
- **Endpoint**: `GET {{backend}}/persons/`
- **Role**: hr_admin
- **Token**: Required (from user login with hr_admin role)
- **Expected**: 200, returns list of PersonOut
- **Steps**:
  1. Login as user with hr_admin role to get token.
  2. Set token in headers.
  3. Send GET request.
  4. Verify response contains list of persons.

### 6. Update Person
- **Endpoint**: `PUT {{backend}}/persons/{{person_id}}`
- **Role**: hr_admin
- **Token**: Required (from user login with hr_admin role)
- **Body**:
  ```json
  {
    "first_name": "Jane",
    "last_name": "Doe"
  }
  ```
- **Expected**: 200, returns updated PersonOut
- **Steps**:
  1. Login as user with hr_admin role to get token.
  2. Set token in headers.
  3. Send PUT request with body and valid person_id.
  4. Verify response contains updated person details.

### 7. Delete Person
- **Endpoint**: `DELETE {{backend}}/persons/{{person_id}}`
- **Role**: hr_admin
- **Token**: Required (from user login with hr_admin role)
- **Expected**: 200, returns {"message": "Person deleted"}
- **Steps**:
  1. Login as user with hr_admin role to get token.
  2. Set token in headers.
  3. Send DELETE request with valid person_id.
  4. Verify response contains success message.

## Additional Test Cases
- **Unauthorized Access**: Test each endpoint with invalid or missing token to verify 401 response.
- **Forbidden Access**: Test endpoints with incorrect role (e.g., person_user for organization_admin endpoints) to verify 403 response.
- **Not Found**: Test GET/PUT/DELETE with invalid IDs to verify 404 response.
- **Invalid Data**: Test POST/PUT with invalid data (e.g., missing required fields) to verify 422 response.
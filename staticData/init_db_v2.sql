-- Drop tables in reverse order to avoid foreign key conflicts
DROP TABLE IF EXISTS communication_event_purpose_history;
DROP TABLE IF EXISTS communication_event_purpose;
DROP TABLE IF EXISTS communication_event_history;
DROP TABLE IF EXISTS communication_event;
DROP TABLE IF EXISTS role_relationship_history;
DROP TABLE IF EXISTS role_relationship;
DROP TABLE IF EXISTS role_relationship_status_types;
DROP TABLE IF EXISTS priority_types;
DROP TABLE IF EXISTS relationship_types;
DROP TABLE IF EXISTS party_role_history;
DROP TABLE IF EXISTS party_role;
DROP TABLE IF EXISTS role_types;
DROP TABLE IF EXISTS communication_event_status_types;
DROP TABLE IF EXISTS contact_mechanism_types;
DROP TABLE IF EXISTS person_history;
DROP TABLE IF EXISTS organization_history;
DROP TABLE IF EXISTS passport_history;
DROP TABLE IF EXISTS passports;
DROP TABLE IF EXISTS persons;
DROP TABLE IF EXISTS organizations;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS gender_types;
DROP TABLE IF EXISTS marital_status_types;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS ethnicity_types;
DROP TABLE IF EXISTS income_ranges;
DROP TABLE IF EXISTS organization_types;
DROP TABLE IF EXISTS industry_types;
DROP TABLE IF EXISTS employee_count_ranges;
DROP TABLE IF EXISTS party;

-- Base Types Layer: Reference data for classifications
CREATE TABLE gender_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE marital_status_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    iso_code VARCHAR(3) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    name_th VARCHAR(100)
);

CREATE TABLE ethnicity_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE income_ranges (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE organization_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE industry_types (
    id SERIAL PRIMARY KEY,
    naisc VARCHAR(10) NOT NULL,
    description VARCHAR(255) NOT NULL
);

CREATE TABLE employee_count_ranges (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

-- Base Types Layer: Role-related reference data
CREATE TABLE role_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE relationship_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE priority_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE role_relationship_status_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE contact_mechanism_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE communication_event_status_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE communication_event_purpose_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

-- Core Layer: Party as supertype
CREATE TABLE party (
    id SERIAL PRIMARY KEY -- Unique identifier for each party
);

-- Core Layer: Users for authentication
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) CHECK (role IN ('system_admin', 'basetype_admin', 'hr_admin', 'organization_admin', 'organization_user', 'person_user')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Core Layer: Persons linked to party
CREATE TABLE persons (
    id INT PRIMARY KEY REFERENCES party(id) ON DELETE CASCADE,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    personal_id_number VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    middle_name VARCHAR(255),
    last_name VARCHAR(255) NOT NULL,
    nick_name VARCHAR(255),
    birth_date DATE NOT NULL,
    gender_type_id INT REFERENCES gender_types(id) ON DELETE SET NULL,
    marital_status_type_id INT REFERENCES marital_status_types(id) ON DELETE SET NULL,
    country_id INT REFERENCES countries(id) ON DELETE SET NULL,
    height INT NOT NULL,
    weight INT NOT NULL,
    ethnicity_type_id INT REFERENCES ethnicity_types(id) ON DELETE SET NULL,
    income_range_id INT REFERENCES income_ranges(id) ON DELETE SET NULL,
    comment TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Core Layer: Organizations linked to party
CREATE TABLE organizations (
    id INT PRIMARY KEY REFERENCES party(id) ON DELETE CASCADE,
    federal_tax_id VARCHAR(50),
    name_en VARCHAR(255) NOT NULL,
    name_th VARCHAR(255),
    organization_type_id INT REFERENCES organization_types(id) ON DELETE SET NULL,
    industry_type_id INT REFERENCES industry_types(id) ON DELETE SET NULL,
    employee_count_range_id INT REFERENCES employee_count_ranges(id) ON DELETE SET NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    comment TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- History Layer: Person history
CREATE TABLE person_history (
    id SERIAL PRIMARY KEY,
    person_id INT REFERENCES persons(id) ON DELETE SET NULL,
    username VARCHAR(255),
    password VARCHAR(255),
    personal_id_number VARCHAR(50),
    first_name VARCHAR(255),
    middle_name VARCHAR(255),
    last_name VARCHAR(255),
    nick_name VARCHAR(255),
    birth_date DATE,
    gender_type_id INT,
    marital_status_type_id INT,
    country_id INT,
    height INT,
    weight INT,
    ethnicity_type_id INT,
    income_range_id INT,
    comment TEXT,
    action VARCHAR(50) NOT NULL,
    action_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- History Layer: Organization history
CREATE TABLE organization_history (
    id SERIAL PRIMARY KEY,
    organization_id INT REFERENCES organizations(id) ON DELETE SET NULL,
    federal_tax_id VARCHAR(50),
    name_en VARCHAR(255),
    name_th VARCHAR(255),
    organization_type_id INT,
    industry_type_id INT,
    employee_count_range_id INT,
    username VARCHAR(255),
    password VARCHAR(255),
    comment TEXT,
    action VARCHAR(50) NOT NULL,
    action_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Core Layer: Passports linked to persons
CREATE TABLE passports (
    id SERIAL PRIMARY KEY,
    passport_id_number VARCHAR(50) UNIQUE NOT NULL,
    issue_date DATE NOT NULL,
    expire_date DATE NOT NULL,
    person_id INT REFERENCES persons(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- History Layer: Passport history
CREATE TABLE passport_history (
    id SERIAL PRIMARY KEY,
    passport_id INT REFERENCES passports(id) ON DELETE SET NULL,
    passport_id_number VARCHAR(50),
    issue_date DATE,
    expire_date DATE,
    person_id INT,
    action VARCHAR(50) NOT NULL,
    action_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Role Layer: Party roles
CREATE TABLE party_role (
    id SERIAL PRIMARY KEY,
    note TEXT,
    party_id INT REFERENCES party(id) ON DELETE CASCADE,
    role_type_id INT REFERENCES role_types(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- History Layer: Party role history
CREATE TABLE party_role_history (
    id SERIAL PRIMARY KEY,
    party_role_id INT REFERENCES party_role(id) ON DELETE SET NULL,
    note TEXT,
    party_id INT,
    role_type_id INT,
    action VARCHAR(50) NOT NULL,
    action_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Relationship Layer: Role relationships
CREATE TABLE role_relationship (
    id SERIAL PRIMARY KEY,
    from_party_role_id INT REFERENCES party_role(id) ON DELETE SET NULL,
    to_party_role_id INT REFERENCES party_role(id) ON DELETE SET NULL,
    comment TEXT,
    relationship_type_id INT REFERENCES relationship_types(id) ON DELETE SET NULL,
    priority_type_id INT REFERENCES priority_types(id) ON DELETE SET NULL,
    role_relationship_status_type_id INT REFERENCES role_relationship_status_types(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- History Layer: Role relationship history
CREATE TABLE role_relationship_history (
    id SERIAL PRIMARY KEY,
    role_relationship_id INT REFERENCES role_relationship(id) ON DELETE SET NULL,
    from_party_role_id INT,
    to_party_role_id INT,
    comment TEXT,
    relationship_type_id INT,
    priority_type_id INT,
    role_relationship_status_type_id INT,
    action VARCHAR(50) NOT NULL,
    action_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Communication Layer: Communication events
CREATE TABLE communication_event (
    id SERIAL PRIMARY KEY,
    note TEXT,
    role_relationship_id INT REFERENCES role_relationship(id) ON DELETE SET NULL,
    contact_mechanism_type_id INT REFERENCES contact_mechanism_types(id) ON DELETE SET NULL,
    communication_event_status_type_id INT REFERENCES communication_event_status_types(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- History Layer: Communication event history
CREATE TABLE communication_event_history (
    id SERIAL PRIMARY KEY,
    communication_event_id INT REFERENCES communication_event(id) ON DELETE SET NULL,
    note TEXT,
    role_relationship_id INT,
    contact_mechanism_type_id INT,
    communication_event_status_type_id INT,
    action VARCHAR(50) NOT NULL,
    action_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Communication Layer: Communication event purposes
CREATE TABLE communication_event_purpose (
    id SERIAL PRIMARY KEY,
    note TEXT,
    communication_event_id INT REFERENCES communication_event(id) ON DELETE SET NULL,
    communication_event_purpose_type_id INT REFERENCES communication_event_purpose_types(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- History Layer: Communication event purpose history
CREATE TABLE communication_event_purpose_history (
    id SERIAL PRIMARY KEY,
    communication_event_purpose_id INT REFERENCES communication_event_purpose(id) ON DELETE SET NULL,
    note TEXT,
    communication_event_id INT,
    communication_event_purpose_type_id INT,
    action VARCHAR(50) NOT NULL,
    action_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
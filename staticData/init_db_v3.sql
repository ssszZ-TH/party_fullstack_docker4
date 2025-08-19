-- Drop tables in reverse order to avoid foreign key conflicts, using CASCADE where necessary
DROP TABLE IF EXISTS communication_event_purpose_history CASCADE;
DROP TABLE IF EXISTS communication_event_purpose CASCADE;
DROP TABLE IF EXISTS communication_event_history CASCADE;
DROP TABLE IF EXISTS communication_event CASCADE;
DROP TABLE IF EXISTS party_relationship_history CASCADE;
DROP TABLE IF EXISTS party_relationship CASCADE;
DROP TABLE IF EXISTS passport_history CASCADE;
DROP TABLE IF EXISTS passports CASCADE;
DROP TABLE IF EXISTS person_history CASCADE;
DROP TABLE IF EXISTS organization_history CASCADE;
DROP TABLE IF EXISTS persons CASCADE;
DROP TABLE IF EXISTS organizations CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS gender_types CASCADE;
DROP TABLE IF EXISTS marital_status_types CASCADE;
DROP TABLE IF EXISTS countries CASCADE;
DROP TABLE IF EXISTS ethnicity_types CASCADE;
DROP TABLE IF EXISTS income_ranges CASCADE;
DROP TABLE IF EXISTS organization_types CASCADE;
DROP TABLE IF EXISTS industry_types CASCADE;
DROP TABLE IF EXISTS employee_count_ranges CASCADE;
DROP TABLE IF EXISTS party CASCADE;

-- Type Layer: Reference data for classifications
CREATE TABLE gender_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
    -- Part of Type Layer for person gender classification
);

CREATE TABLE marital_status_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
    -- Part of Type Layer for person marital status classification
);

CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    iso_code VARCHAR(3) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    name_th VARCHAR(100)
    -- Part of Type Layer for country classification
);

CREATE TABLE ethnicity_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
    -- Part of Type Layer for person ethnicity classification
);

CREATE TABLE income_ranges (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
    -- Part of Type Layer for person income range classification
);

CREATE TABLE organization_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
    -- Part of Type Layer for organization type classification
);

CREATE TABLE industry_types (
    id SERIAL PRIMARY KEY,
    naisc VARCHAR(10) NOT NULL,
    description VARCHAR(255) NOT NULL
    -- Part of Type Layer for organization industry classification
);

CREATE TABLE employee_count_ranges (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
    -- Part of Type Layer for organization employee count classification
);

-- Type Layer: Communication-related reference data
CREATE TABLE contact_mechanism_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
    -- Part of Type Layer for communication contact mechanism classification
);

CREATE TABLE communication_event_status_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
    -- Part of Type Layer for communication event status classification
);

CREATE TABLE communication_event_purpose_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
    -- Part of Type Layer for communication event purpose classification
);

-- Core Layer: Party as supertype
CREATE TABLE party (
    id SERIAL PRIMARY KEY
    -- Core Layer: Base entity for persons and organizations
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
    -- Core Layer: Authentication and authorization for system access
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
    -- Core Layer: Person entity linked to party
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
    -- Core Layer: Organization entity linked to party
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
    -- History Layer: Tracks changes to person records
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
    -- History Layer: Tracks changes to organization records
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
    -- Core Layer: Passport details for persons
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
    -- History Layer: Tracks changes to passport records
);

-- Relationship Layer: Party relationships
CREATE TABLE party_relationship (
    id SERIAL PRIMARY KEY,
    from_party_id INT REFERENCES party(id) ON DELETE SET NULL,
    to_party_id INT REFERENCES party(id) ON DELETE SET NULL,
    comment TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
    -- Relationship Layer: Defines relationships between parties
);

-- History Layer: Party relationship history
CREATE TABLE party_relationship_history (
    id SERIAL PRIMARY KEY,
    party_relationship_id INT REFERENCES party_relationship(id) ON DELETE SET NULL,
    from_party_id INT,
    to_party_id INT,
    comment TEXT,
    action VARCHAR(50) NOT NULL,
    action_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    -- History Layer: Tracks changes to party relationships
);

-- Communication Layer: Communication events
CREATE TABLE communication_event (
    id SERIAL PRIMARY KEY,
    note TEXT,
    party_relationship_id INT REFERENCES party_relationship(id) ON DELETE SET NULL,
    contact_mechanism_type_id INT REFERENCES contact_mechanism_types(id) ON DELETE SET NULL,
    communication_event_status_type_id INT REFERENCES communication_event_status_types(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
    -- Communication Layer: Records communication events
);

-- History Layer: Communication event history
CREATE TABLE communication_event_history (
    id SERIAL PRIMARY KEY,
    communication_event_id INT REFERENCES communication_event(id) ON DELETE SET NULL,
    note TEXT,
    party_relationship_id INT,
    contact_mechanism_type_id INT,
    communication_event_status_type_id INT,
    action VARCHAR(50) NOT NULL,
    action_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    -- History Layer: Tracks changes to communication events
);

-- Communication Layer: Communication event purposes
CREATE TABLE communication_event_purpose (
    id SERIAL PRIMARY KEY,
    note TEXT,
    communication_event_id INT REFERENCES communication_event(id) ON DELETE SET NULL,
    communication_event_purpose_type_id INT REFERENCES communication_event_purpose_types(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
    -- Communication Layer: Defines purposes for communication events
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
    -- History Layer: Tracks changes to communication event purposes
);
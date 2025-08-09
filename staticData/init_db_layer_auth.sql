DROP TABLE IF EXISTS person_history;
DROP TABLE IF EXISTS organization_history;
DROP TABLE IF EXISTS persons;
DROP TABLE IF EXISTS organizations;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS gender_types;
DROP TABLE IF EXISTS marital_status_types;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS ethnicity_types;
DROP TABLE IF EXISTS income_ranges;
DROP TABLE IF EXISTS organization_types;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) CHECK (role IN ('system_admin', 'basetype_admin', 'hr_admin', 'organization_admin')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

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

CREATE TABLE persons (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    personal_id_number VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    middle_name VARCHAR(255),
    last_name VARCHAR(255) NOT NULL,
    nick_name VARCHAR(255),
    birth_date DATE NOT NULL,
    gender_type_id INT REFERENCES gender_types(id),
    marital_status_type_id INT REFERENCES marital_status_types(id),
    country_id INT REFERENCES countries(id),
    height INT NOT NULL,
    weight INT NOT NULL,
    ethnicity_type_id INT REFERENCES ethnicity_types(id),
    income_range_id INT REFERENCES income_ranges(id),
    comment TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

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

CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    federal_tax_id VARCHAR(50),
    name_en VARCHAR(255) NOT NULL,
    name_th VARCHAR(255),
    organization_type_id INT REFERENCES organization_types(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE organization_history (
    id SERIAL PRIMARY KEY,
    organization_id INT REFERENCES organizations(id) ON DELETE SET NULL,
    federal_tax_id VARCHAR(50),
    name_en VARCHAR(255),
    name_th VARCHAR(255),
    organization_type_id INT,
    action VARCHAR(50) NOT NULL,
    action_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
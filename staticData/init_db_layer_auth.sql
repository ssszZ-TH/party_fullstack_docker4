-- Drop tables if they exist to ensure clean schema creation
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

-- Create users table with updated role check
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) CHECK (role IN ('system_admin', 'basetype_admin', 'hr_admin', 'organization_admin', 'organization_user', 'person_user')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Create gender_types table
CREATE TABLE gender_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

-- Create marital_status_types table
CREATE TABLE marital_status_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

-- Create countries table
CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    iso_code VARCHAR(3) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    name_th VARCHAR(100)
);

-- Create ethnicity_types table
CREATE TABLE ethnicity_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

-- Create income_ranges table
CREATE TABLE income_ranges (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

-- Create organization_types table
CREATE TABLE organization_types (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

-- Create industry_types table
CREATE TABLE industry_types (
    id SERIAL PRIMARY KEY,
    naisc VARCHAR(10) NOT NULL,
    description VARCHAR(255) NOT NULL
);

-- Create employee_count_ranges table
CREATE TABLE employee_count_ranges (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

-- Create persons table with nullable foreign keys
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

-- Create person_history table
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

-- Create passports table
CREATE TABLE passports (
    id SERIAL PRIMARY KEY,
    passport_id_number VARCHAR(50) UNIQUE NOT NULL,
    issue_date DATE NOT NULL,
    expire_date DATE NOT NULL,
    person_id INT REFERENCES persons(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Create passport_history table
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

-- Create organizations table with nullable foreign keys and additional columns
CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
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

-- Create organization_history table with additional columns
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
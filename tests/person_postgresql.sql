-- PostgreSQL Schema: Person (Target for MongoDB -> PostgreSQL migration)
-- 3NF Normalized from MongoDB nested document with 3-level nesting
-- All tables use VARCHAR primary keys (string IDs with prefixes)
-- Tests 3-level deep nesting: person.employment.company.address

-- Table 1: person (main entity)
-- ID from MongoDB _id (e.g., "p001")
CREATE TABLE person (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Table 2: address (extracted from person.address embedded object)
-- ID with "addr" prefix (e.g., "addr001", "addr002")
CREATE TABLE address (
    id VARCHAR(255) PRIMARY KEY,
    street VARCHAR(255),
    city VARCHAR(255),
    person_id VARCHAR(255) NOT NULL REFERENCES person(id)
);

-- Table 3: employment (extracted from person.employment - 1st level nesting)
-- ID with "emp" prefix (e.g., "emp001", "emp002")
CREATE TABLE employment (
    id VARCHAR(255) PRIMARY KEY,
    position VARCHAR(255),
    person_id VARCHAR(255) NOT NULL REFERENCES person(id)
);

-- Table 4: company (extracted from employment.company - 2nd level nesting)
-- ID with "comp" prefix (e.g., "comp001", "comp002")
CREATE TABLE company (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    employment_id VARCHAR(255) NOT NULL REFERENCES employment(id)
);

-- Table 5: company_address (extracted from company.address - 3rd level nesting)
-- ID with "caddr" prefix (e.g., "caddr001", "caddr002")
-- Demonstrates 3-level deep nesting: person -> employment -> company -> address
CREATE TABLE company_address (
    id VARCHAR(255) PRIMARY KEY,
    street VARCHAR(255),
    city VARCHAR(255),
    company_id VARCHAR(255) NOT NULL REFERENCES company(id)
);

-- Table 6: person_tag (flattened from value array)
-- ID with "t" prefix (e.g., "t001", "t002")
-- 'value' column renamed to 'tag_value' via RENAME clause
CREATE TABLE person_tag (
    id VARCHAR(255) PRIMARY KEY,
    tag_value VARCHAR(255) NOT NULL,
    person_id VARCHAR(255) NOT NULL REFERENCES person(id)
);

-- Table 7: person_knows (M:N self-reference join table)
-- Composite primary key (person_id, knows_person_id)
CREATE TABLE person_knows (
    person_id VARCHAR(255) NOT NULL REFERENCES person(id),
    knows_person_id VARCHAR(255) NOT NULL REFERENCES person(id),
    PRIMARY KEY (person_id, knows_person_id)
);

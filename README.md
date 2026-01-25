# SMEL - Schema Migration & Evolution Language

A formally defined language for schema migration and evolution between heterogeneous database systems.

## Overview

SMEL (Schema Migration & Evolution Language) provides a unified approach to:
- Define schema transformations across heterogeneous database systems
- Support bidirectional migration between SQL and NoSQL databases
- Support schema evolution within the same database type

## Supported Database Models

- **RELATIONAL**: PostgreSQL, MySQL, Oracle, SQL Server
- **DOCUMENT**: MongoDB, CouchDB, DocumentDB
- **GRAPH**: Neo4j, ArangoDB
- **COLUMNAR**: Cassandra, HBase

## Installation

### Prerequisites
- Python 3.10+
- ANTLR 4.13.2

### Setup
```bash
git clone https://github.com/baobaodaren0918/SMEL.git
cd SMEL

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Command Line Interface
```bash
python main.py
```

### Web Interface
```bash
python web_server.py
# Opens at http://localhost:5570
```

### Programmatic Usage
```python
from core import run_migration

# Run migration
result = run_migration('d2r')  # Document -> Relational
print(result['exported_target'])  # Generated target schema
```

## Project Structure

```
SMEL/
├── grammar/
│   ├── SMEL_Specific.g4           # Specific operations grammar (ADD_ATTRIBUTE, DELETE_ENTITY)
│   ├── SMEL_Pauschalisiert.g4     # Generalized operations grammar (ADD_PS, DELETE_PS)
│   ├── specific/                   # Generated parser for Specific grammar
│   │   ├── SMEL_SpecificLexer.py
│   │   ├── SMEL_SpecificParser.py
│   │   └── SMEL_SpecificListener.py
│   ├── pauschalisiert/            # Generated parser for Pauschalisiert grammar
│   │   ├── SMEL_PauschalisiertLexer.py
│   │   ├── SMEL_PauschalisiertParser.py
│   │   └── SMEL_PauschalisiertListener.py
│   ├── antlr-4.13.2-complete.jar
│   └── generate_parser_*.bat      # Parser generation scripts
├── Schema/
│   ├── adapters/
│   │   ├── postgresql_adapter.py  # PostgreSQL adapter
│   │   └── mongodb_adapter.py     # MongoDB adapter
│   └── unified_meta_schema.py     # Unified meta-schema
├── tests/
│   ├── *.smel                     # SMEL migration scripts
│   ├── *.sql                      # SQL schema files
│   └── *.json                     # JSON schema files
├── config.py                      # Configuration
├── core.py                        # Migration engine
├── smel_listeners.py              # SMEL listeners for both grammars
├── parser_factory.py              # Parser factory
├── main.py                        # CLI interface
└── web_server.py                  # Web interface
```

## Architecture

```
┌─────────────┐     Reverse Eng      ┌─────────────┐      SMEL         ┌─────────────┐     Forward Eng     ┌─────────────┐
│   Source    │ ──────────────────► │   Meta V1   │ ──────────────► │   Meta V2   │ ──────────────────► │   Target    │
│   Schema    │                      │  (Unified)  │                  │  (Unified)  │                      │   Schema    │
│ (DDL/JSON)  │                      │             │                  │             │                      │ (DDL/JSON)  │
└─────────────┘                      └─────────────┘                  └─────────────┘                      └─────────────┘
     │                                     │                                │                                    │
     │                                     │                                │                                    │
     ▼                                     ▼                                ▼                                    ▼
 PostgreSQL                           Unified                          Unified                             PostgreSQL
 MongoDB                              Meta-Schema                      Meta-Schema                         MongoDB
 Neo4j                                (Database                        (Database                           Neo4j
 Cassandra                            Agnostic)                        Agnostic)                           Cassandra
```

### Key Generation & Dependency Resolution

When extracting nested structures, SMEL automatically manages primary key generation:

```
FLATTEN person.employment AS employment
    GENERATE KEY id AS String PREFIX "emp"
    ADD REFERENCE person_id TO person
```

**Key Registry** tracks generated keys for traceability:

| Entity | Key Field | Prefix | Format | Source |
|--------|-----------|--------|--------|--------|
| person | _id | - | (original) | - |
| employment | id | emp | emp_{uuid6} | person |
| company | id | comp | comp_{uuid6} | employment |

**Auto Prefix Generation**: If PREFIX is not specified, automatically generates from entity name (first 3 + last 1 character):
- `employment` → `empt`
- `company` → `comy`
- `address` → `adds`

**Dependency Sorting**: Operations are automatically sorted by dependency order, so users don't need to worry about the execution sequence.

## Grammar Variants

SMEL provides two grammar variants:

1. **SMEL_Specific.g4**: Uses specific keywords (e.g., `ADD_ATTRIBUTE`, `DELETE_ENTITY`)
2. **SMEL_Pauschalisiert.g4**: Uses parameterized operations (e.g., `ADD_PS ATTRIBUTE`, `DELETE_PS ENTITY`)

Both grammars are functionally equivalent and generate the same internal operations.

## License

MIT License - See LICENSE file for details.

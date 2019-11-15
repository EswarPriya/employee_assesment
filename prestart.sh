#!/bin/bash
set -e

psql -u postgres <<-EOSQL
    CREATE USER employee3;
    CREATE DATABASE employee_ass;
    GRANT ALL PRIVILEGES ON DATABASE employee_ass TO employee3;
EOSQL
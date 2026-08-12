
CREATE DATABASE postgres;
CREATE USER postgres WITH password 'postgres';
GRANT ALL PRIVILEGES ON postgres to postgres;

-- app user
CREATE DATABASE taskly_db;
CREATE USER taskly_user WITH PASSWORD 'qwerty12345';
GRANT ALL PRIVILEGES ON taskly_db to taskly_user;

-- Database version 15.1 (Debian 15.1-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';
SET default_table_access_method = heap;

-- Drop schema.

DROP SCHEMA IF EXISTS cbe CASCADE;

-- Create schema.

CREATE SCHEMA cbe;

ALTER SCHEMA cbe OWNER TO postgres;

-- Create types.

CREATE TYPE cbe.function_enum AS ENUM (
    'director',
    'permanent_representative',
    'person_in_charge_of_daily_management'
);

ALTER TYPE cbe.function_enum OWNER TO postgres;

-- Create tables.

-- Table entities.

CREATE TABLE cbe.entities (
    id integer NOT NULL,
    enterprise_number integer NOT NULL UNIQUE
);

ALTER TABLE cbe.entities OWNER TO postgres;

CREATE SEQUENCE cbe.entities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE cbe.entities_id_seq OWNER TO postgres;

ALTER SEQUENCE cbe.entities_id_seq OWNED BY cbe.entities.id;

ALTER TABLE ONLY cbe.entities ALTER COLUMN id SET DEFAULT nextval('cbe.entities_id_seq'::regclass);

SELECT pg_catalog.setval('cbe.entities_id_seq', 1, false);

-- Table persons.

CREATE TABLE cbe.persons (
    id integer NOT NULL,
    last_name character varying(50) NOT NULL,
    first_name character varying(50) NOT NULL,
    UNIQUE(last_name, first_name)
);

ALTER TABLE cbe.persons OWNER TO postgres;

CREATE SEQUENCE cbe.persons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE cbe.persons_id_seq OWNER TO postgres;

ALTER SEQUENCE cbe.persons_id_seq OWNED BY cbe.persons.id;

ALTER TABLE ONLY cbe.persons ALTER COLUMN id SET DEFAULT nextval('cbe.persons_id_seq'::regclass);

SELECT pg_catalog.setval('cbe.persons_id_seq', 1, false);

-- Table entities_persons

CREATE TABLE cbe.entities_persons (
    id integer not null,
    entity_id integer NOT NULL,
    person_id integer NOT NULL,
    function cbe.function_enum NOT NULL,
    start_date date NOT NULL,
    UNIQUE(entity_id, person_id, function)
);

ALTER TABLE cbe.entities_persons OWNER TO postgres;

CREATE SEQUENCE cbe.entities_persons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE cbe.entities_persons_id_seq OWNER TO postgres;

ALTER SEQUENCE cbe.entities_persons_id_seq OWNED BY cbe.entities_persons.id;

ALTER TABLE ONLY cbe.entities_persons ALTER COLUMN id SET DEFAULT nextval('cbe.entities_persons_id_seq'::regclass);

SELECT pg_catalog.setval('cbe.entities_persons_id_seq', 1, false);

-- Table entities_entities.

CREATE TABLE cbe.entities_entities (
    id integer not null,
    represented_entity_id integer NOT NULL,
    representative_entity_id integer NOT NULL,
    function cbe.function_enum NOT NULL,
    person_id integer NOT NULL,
    start_date date NOT NULL,
    UNIQUE(represented_entity_id, representative_entity_id, function)
);

ALTER TABLE cbe.entities_entities OWNER TO postgres;

CREATE SEQUENCE cbe.entities_entities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE cbe.entities_entities_id_seq OWNER TO postgres;

ALTER SEQUENCE cbe.entities_entities_id_seq OWNED BY cbe.entities_entities.id;

ALTER TABLE ONLY cbe.entities_entities ALTER COLUMN id SET DEFAULT nextval('cbe.entities_entities_id_seq'::regclass);

SELECT pg_catalog.setval('cbe.entities_entities_id_seq', 1, false);

-- Add constraints to table.

ALTER TABLE ONLY cbe.entities
    ADD CONSTRAINT entities_pkey PRIMARY KEY (id);

ALTER TABLE ONLY cbe.persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (id);

ALTER TABLE ONLY cbe.entities_persons
    ADD CONSTRAINT entities_persons_pkey PRIMARY KEY (id);

ALTER TABLE ONLY cbe.entities_entities
    ADD CONSTRAINT entities_entities_pkey PRIMARY KEY (id);

ALTER TABLE ONLY cbe.entities_entities
    ADD CONSTRAINT entities_entities_person_id_fkey FOREIGN KEY (person_id) REFERENCES cbe.persons(id);

ALTER TABLE ONLY cbe.entities_entities
    ADD CONSTRAINT entities_entities_representative_entity_id_fkey FOREIGN KEY (representative_entity_id) REFERENCES cbe.entities(id);

ALTER TABLE ONLY cbe.entities_entities
    ADD CONSTRAINT entities_entities_represented_entity_id_fkey FOREIGN KEY (represented_entity_id) REFERENCES cbe.entities(id);

ALTER TABLE ONLY cbe.entities_persons
    ADD CONSTRAINT entities_persons_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES cbe.entities(id);

ALTER TABLE ONLY cbe.entities_persons
    ADD CONSTRAINT entities_persons_person_id_fkey FOREIGN KEY (person_id) REFERENCES cbe.persons(id);

--- Grant privileges to scraper.

GRANT CONNECT 
    ON DATABASE graphion
    TO scraper;

GRANT USAGE 
    ON SCHEMA cbe 
    TO scraper;

GRANT SELECT, INSERT, UPDATE, DELETE
    ON ALL TABLES IN SCHEMA cbe 
    TO scraper;

GRANT USAGE, SELECT 
    ON ALL SEQUENCES IN SCHEMA cbe 
    TO scraper;
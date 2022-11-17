--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1 (Debian 15.1-1.pgdg110+1)
-- Dumped by pg_dump version 15.0

-- Started on 2022-11-16 18:03:18


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

-- Drop schema

DROP SCHEMA IF EXISTS cbe CASCADE;

--
-- TOC entry 6 (class 2615 OID 16418)
-- Name: cbe; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA cbe;


ALTER SCHEMA cbe OWNER TO postgres;

--
-- TOC entry 849 (class 1247 OID 16498)
-- Name: entities_function_enum; Type: TYPE; Schema: cbe; Owner: postgres
--

CREATE TYPE cbe.entities_function_enum AS ENUM (
    'director',
    'person_in_charge_of_daily_management'
);


ALTER TYPE cbe.entities_function_enum OWNER TO postgres;

--
-- TOC entry 846 (class 1247 OID 16457)
-- Name: persons_function_enum; Type: TYPE; Schema: cbe; Owner: postgres
--

CREATE TYPE cbe.persons_function_enum AS ENUM (
    'director',
    'permanent_representative',
    'person_in_charge_of_daily_management'
);


ALTER TYPE cbe.persons_function_enum OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 16409)
-- Name: entities; Type: TABLE; Schema: cbe; Owner: postgres
--

CREATE TABLE cbe.entities (
    id integer NOT NULL,
    enterprise_number integer NOT NULL
);


ALTER TABLE cbe.entities OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16518)
-- Name: entities_entities; Type: TABLE; Schema: cbe; Owner: postgres
--

CREATE TABLE cbe.entities_entities (
    represented_entities_id integer NOT NULL,
    representative_entities_id integer NOT NULL,
    function cbe.entities_function_enum NOT NULL,
    persons_id integer NOT NULL,
    start_date date NOT NULL
);


ALTER TABLE cbe.entities_entities OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16408)
-- Name: entities_id_seq; Type: SEQUENCE; Schema: cbe; Owner: postgres
--

CREATE SEQUENCE cbe.entities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cbe.entities_id_seq OWNER TO postgres;

--
-- TOC entry 3364 (class 0 OID 0)
-- Dependencies: 215
-- Name: entities_id_seq; Type: SEQUENCE OWNED BY; Schema: cbe; Owner: postgres
--

ALTER SEQUENCE cbe.entities_id_seq OWNED BY cbe.entities.id;


--
-- TOC entry 219 (class 1259 OID 16482)
-- Name: entities_persons; Type: TABLE; Schema: cbe; Owner: postgres
--

CREATE TABLE cbe.entities_persons (
    entities_id integer NOT NULL,
    persons_id integer NOT NULL,
    function cbe.persons_function_enum NOT NULL,
    start_date date NOT NULL
);


ALTER TABLE cbe.entities_persons OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16414)
-- Name: persons; Type: TABLE; Schema: cbe; Owner: postgres
--

CREATE TABLE cbe.persons (
    id integer NOT NULL,
    last_name character varying(50) NOT NULL,
    first_name character varying(50) NOT NULL
);


ALTER TABLE cbe.persons OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16413)
-- Name: persons_id_seq; Type: SEQUENCE; Schema: cbe; Owner: postgres
--

CREATE SEQUENCE cbe.persons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cbe.persons_id_seq OWNER TO postgres;

--
-- TOC entry 3365 (class 0 OID 0)
-- Dependencies: 217
-- Name: persons_id_seq; Type: SEQUENCE OWNED BY; Schema: cbe; Owner: postgres
--

ALTER SEQUENCE cbe.persons_id_seq OWNED BY cbe.persons.id;


--
-- TOC entry 3196 (class 2604 OID 16412)
-- Name: entities id; Type: DEFAULT; Schema: cbe; Owner: postgres
--

ALTER TABLE ONLY cbe.entities ALTER COLUMN id SET DEFAULT nextval('cbe.entities_id_seq'::regclass);


--
-- TOC entry 3197 (class 2604 OID 16417)
-- Name: persons id; Type: DEFAULT; Schema: cbe; Owner: postgres
--

ALTER TABLE ONLY cbe.persons ALTER COLUMN id SET DEFAULT nextval('cbe.persons_id_seq'::regclass);


--
-- TOC entry 3354 (class 0 OID 16409)
-- Dependencies: 216
-- Data for Name: entities; Type: TABLE DATA; Schema: cbe; Owner: postgres
--

COPY cbe.entities (id, enterprise_number) FROM stdin;
\.


--
-- TOC entry 3358 (class 0 OID 16518)
-- Dependencies: 220
-- Data for Name: entities_entities; Type: TABLE DATA; Schema: cbe; Owner: postgres
--

COPY cbe.entities_entities (represented_entities_id, representative_entities_id, persons_id, function, start_date) FROM stdin;
\.


--
-- TOC entry 3357 (class 0 OID 16482)
-- Dependencies: 219
-- Data for Name: entities_persons; Type: TABLE DATA; Schema: cbe; Owner: postgres
--

COPY cbe.entities_persons (entities_id, persons_id, function, start_date) FROM stdin;
\.


--
-- TOC entry 3356 (class 0 OID 16414)
-- Dependencies: 218
-- Data for Name: persons; Type: TABLE DATA; Schema: cbe; Owner: postgres
--

COPY cbe.persons (id, last_name, first_name) FROM stdin;
\.


--
-- TOC entry 3366 (class 0 OID 0)
-- Dependencies: 215
-- Name: entities_id_seq; Type: SEQUENCE SET; Schema: cbe; Owner: postgres
--

SELECT pg_catalog.setval('cbe.entities_id_seq', 1, false);


--
-- TOC entry 3367 (class 0 OID 0)
-- Dependencies: 217
-- Name: persons_id_seq; Type: SEQUENCE SET; Schema: cbe; Owner: postgres
--

SELECT pg_catalog.setval('cbe.persons_id_seq', 1, false);


--
-- TOC entry 3205 (class 2606 OID 16522)
-- Name: entities_entities entities_entities_pkey; Type: CONSTRAINT; Schema: cbe; Owner: postgres
--

ALTER TABLE ONLY cbe.entities_entities
    ADD CONSTRAINT entities_entities_pkey PRIMARY KEY (represented_entities_id, representative_entities_id);


--
-- TOC entry 3203 (class 2606 OID 16486)
-- Name: entities_persons entities_persons_pkey; Type: CONSTRAINT; Schema: cbe; Owner: postgres
--

ALTER TABLE ONLY cbe.entities_persons
    ADD CONSTRAINT entities_persons_pkey PRIMARY KEY (entities_id, persons_id);


--
-- TOC entry 3199 (class 2606 OID 16469)
-- Name: entities entities_pkey; Type: CONSTRAINT; Schema: cbe; Owner: postgres
--

ALTER TABLE ONLY cbe.entities
    ADD CONSTRAINT entities_pkey PRIMARY KEY (id);


--
-- TOC entry 3201 (class 2606 OID 16471)
-- Name: persons persons_pkey; Type: CONSTRAINT; Schema: cbe; Owner: postgres
--

ALTER TABLE ONLY cbe.persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (id);


--
-- TOC entry 3208 (class 2606 OID 16533)
-- Name: entities_entities entities_entities_persons_id_fkey; Type: FK CONSTRAINT; Schema: cbe; Owner: postgres
--

ALTER TABLE ONLY cbe.entities_entities
    ADD CONSTRAINT entities_entities_persons_id_fkey FOREIGN KEY (persons_id) REFERENCES cbe.persons(id);


--
-- TOC entry 3209 (class 2606 OID 16528)
-- Name: entities_entities entities_entities_representative_entities_id_fkey; Type: FK CONSTRAINT; Schema: cbe; Owner: postgres
--

ALTER TABLE ONLY cbe.entities_entities
    ADD CONSTRAINT entities_entities_representative_entities_id_fkey FOREIGN KEY (representative_entities_id) REFERENCES cbe.entities(id);


--
-- TOC entry 3210 (class 2606 OID 16523)
-- Name: entities_entities entities_entities_represented_entities_id_fkey; Type: FK CONSTRAINT; Schema: cbe; Owner: postgres
--

ALTER TABLE ONLY cbe.entities_entities
    ADD CONSTRAINT entities_entities_represented_entities_id_fkey FOREIGN KEY (represented_entities_id) REFERENCES cbe.entities(id);


--
-- TOC entry 3206 (class 2606 OID 16487)
-- Name: entities_persons entities_persons_entities_id_fkey; Type: FK CONSTRAINT; Schema: cbe; Owner: postgres
--

ALTER TABLE ONLY cbe.entities_persons
    ADD CONSTRAINT entities_persons_entities_id_fkey FOREIGN KEY (entities_id) REFERENCES cbe.entities(id);


--
-- TOC entry 3207 (class 2606 OID 16492)
-- Name: entities_persons entities_persons_persons_id_fkey; Type: FK CONSTRAINT; Schema: cbe; Owner: postgres
--

ALTER TABLE ONLY cbe.entities_persons
    ADD CONSTRAINT entities_persons_persons_id_fkey FOREIGN KEY (persons_id) REFERENCES cbe.persons(id);


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

-- Completed on 2022-11-16 18:03:18

--
-- PostgreSQL database dump complete
--


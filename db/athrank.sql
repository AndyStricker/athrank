--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Name: award_enum; Type: TYPE; Schema: public; Owner: jugiuser
--

CREATE TYPE award_enum AS ENUM (
    'GOLD',
    'SILVER',
    'BRONZE',
    'AWARD'
);


ALTER TYPE public.award_enum OWNER TO jugiuser;

--
-- Name: category_enum; Type: TYPE; Schema: public; Owner: jugiuser
--

CREATE TYPE category_enum AS ENUM (
    'U8',
    'U10',
    'U12',
    'U14',
    'U16',
    'U18',
    'U20'
);


ALTER TYPE public.category_enum OWNER TO jugiuser;

--
-- Name: sex_enum; Type: TYPE; Schema: public; Owner: jugiuser
--

CREATE TYPE sex_enum AS ENUM (
    'female',
    'male'
);


ALTER TYPE public.sex_enum OWNER TO jugiuser;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: agecategory; Type: TABLE; Schema: public; Owner: jugiuser; Tablespace: 
--

CREATE TABLE agecategory (
    age_cohort integer NOT NULL,
    sex sex_enum NOT NULL,
    category category_enum NOT NULL,
    age integer NOT NULL
);


ALTER TABLE public.agecategory OWNER TO jugiuser;

--
-- Name: athlete; Type: TABLE; Schema: public; Owner: jugiuser; Tablespace: 
--

CREATE TABLE athlete (
    id_athlete integer NOT NULL,
    number integer,
    firstname text NOT NULL,
    lastname text NOT NULL,
    id_section integer DEFAULT 0 NOT NULL,
    age_cohort integer NOT NULL,
    sprint_result numeric(5,2),
    longjump_result numeric(5,2),
    sex sex_enum NOT NULL,
    highjump_result numeric(5,2),
    shotput_result numeric(5,2),
    ball_result numeric(5,2),
    endurance_run_result numeric(5,2),
    sprint_points integer,
    longjump_points integer,
    highjump_points integer,
    shotput_points integer,
    ball_points integer,
    endurance_run_points integer,
    total_points integer DEFAULT 0 NOT NULL,
    award award_enum,
    qualified boolean DEFAULT false NOT NULL,
    rank integer,
    verified boolean DEFAULT false NOT NULL
);


ALTER TABLE public.athlete OWNER TO jugiuser;

--
-- Name: athlete_id_athlete_seq; Type: SEQUENCE; Schema: public; Owner: jugiuser
--

CREATE SEQUENCE athlete_id_athlete_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.athlete_id_athlete_seq OWNER TO jugiuser;

--
-- Name: athlete_id_athlete_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jugiuser
--

ALTER SEQUENCE athlete_id_athlete_seq OWNED BY athlete.id_athlete;


--
-- Name: category; Type: TABLE; Schema: public; Owner: jugiuser; Tablespace: 
--

CREATE TABLE category (
    category category_enum NOT NULL,
    sex sex_enum NOT NULL,
    sprint_distance integer NOT NULL,
    has_longjump boolean NOT NULL,
    has_highjump boolean NOT NULL,
    has_shotput boolean NOT NULL,
    has_ball boolean NOT NULL,
    has_endurance_run boolean NOT NULL
);


ALTER TABLE public.category OWNER TO jugiuser;

--
-- Name: section; Type: TABLE; Schema: public; Owner: jugiuser; Tablespace: 
--

CREATE TABLE section (
    id_section integer NOT NULL,
    name text NOT NULL,
    canton character(2)
);


ALTER TABLE public.section OWNER TO jugiuser;

--
-- Name: section_id_section_seq; Type: SEQUENCE; Schema: public; Owner: jugiuser
--

CREATE SEQUENCE section_id_section_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.section_id_section_seq OWNER TO jugiuser;

--
-- Name: section_id_section_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jugiuser
--

ALTER SEQUENCE section_id_section_seq OWNED BY section.id_section;


--
-- Name: id_athlete; Type: DEFAULT; Schema: public; Owner: jugiuser
--

ALTER TABLE ONLY athlete ALTER COLUMN id_athlete SET DEFAULT nextval('athlete_id_athlete_seq'::regclass);


--
-- Name: id_section; Type: DEFAULT; Schema: public; Owner: jugiuser
--

ALTER TABLE ONLY section ALTER COLUMN id_section SET DEFAULT nextval('section_id_section_seq'::regclass);


--
-- Name: agecategory_pkey; Type: CONSTRAINT; Schema: public; Owner: jugiuser; Tablespace: 
--

ALTER TABLE ONLY agecategory
    ADD CONSTRAINT agecategory_pkey PRIMARY KEY (age_cohort, sex);


--
-- Name: athlete_number_key; Type: CONSTRAINT; Schema: public; Owner: jugiuser; Tablespace: 
--

ALTER TABLE ONLY athlete
    ADD CONSTRAINT athlete_number_key UNIQUE (number);


--
-- Name: athlete_pkey; Type: CONSTRAINT; Schema: public; Owner: jugiuser; Tablespace: 
--

ALTER TABLE ONLY athlete
    ADD CONSTRAINT athlete_pkey PRIMARY KEY (id_athlete);


--
-- Name: category_pkey; Type: CONSTRAINT; Schema: public; Owner: jugiuser; Tablespace: 
--

ALTER TABLE ONLY category
    ADD CONSTRAINT category_pkey PRIMARY KEY (category, sex);


--
-- Name: section_pkey; Type: CONSTRAINT; Schema: public; Owner: jugiuser; Tablespace: 
--

ALTER TABLE ONLY section
    ADD CONSTRAINT section_pkey PRIMARY KEY (id_section);


--
-- Name: agecategory_sex_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jugiuser
--

ALTER TABLE ONLY agecategory
    ADD CONSTRAINT agecategory_sex_fkey FOREIGN KEY (sex, category) REFERENCES category(sex, category);


--
-- Name: athlete_id_section_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jugiuser
--

ALTER TABLE ONLY athlete
    ADD CONSTRAINT athlete_id_section_fkey FOREIGN KEY (id_section) REFERENCES section(id_section);


--
-- Name: athlete_sex_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jugiuser
--

ALTER TABLE ONLY athlete
    ADD CONSTRAINT athlete_sex_fkey FOREIGN KEY (sex, age_cohort) REFERENCES agecategory(sex, age_cohort);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--


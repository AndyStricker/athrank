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
-- Data for Name: agecategory; Type: TABLE DATA; Schema: public; Owner: jugiuser
--

COPY agecategory (age_cohort, sex, category, age) FROM stdin;
2011	male	U8	5
2009	male	U8	7
2010	male	U8	6
2008	male	U10	8
2007	male	U10	9
2006	male	U12	10
2005	male	U12	11
2004	male	U14	12
2003	male	U14	13
2002	male	U16	14
2001	male	U16	15
2000	male	U18	16
1999	male	U18	17
1998	male	U20	18
1997	male	U20	19
2011	female	U8	5
2008	female	U10	8
2010	female	U8	6
2009	female	U8	7
2007	female	U10	9
2006	female	U12	10
2005	female	U12	11
2004	female	U14	12
2003	female	U14	13
2002	female	U16	14
2001	female	U16	15
2000	female	U18	16
1999	female	U18	17
1998	female	U20	18
1997	female	U20	19
\.


--
-- PostgreSQL database dump complete
--


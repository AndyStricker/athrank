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
-- Data for Name: section; Type: TABLE DATA; Schema: public; Owner: jugiuser
--

COPY section (id_section, name, canton) FROM stdin;
1	Neuhausen	SH
2	Schaffhausen	SH
3	Dachsen	ZH
4	Oerlikon	ZH
5	Dürnten	ZH
6	Frauenfeld	TG
7	Kreuzlingen	TG
8	Herisau	AR
\.


--
-- Name: section_id_section_seq; Type: SEQUENCE SET; Schema: public; Owner: jugiuser
--

SELECT pg_catalog.setval('section_id_section_seq', 1, false);


--
-- PostgreSQL database dump complete
--


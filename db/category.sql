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
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: jugiuser
--

COPY category (category, sex, sprint_distance, has_longjump, has_highjump, has_shotput, has_ball, has_endurance_run) FROM stdin;
U8	male	60	t	f	f	t	f
U10	male	60	t	f	f	t	f
U12	male	60	t	f	f	t	f
U14	male	60	t	f	f	t	f
U16	male	80	t	t	t	f	t
U18	male	100	t	t	t	f	t
U20	male	100	t	t	t	f	t
U8	female	60	t	f	f	t	f
U10	female	60	t	f	f	t	f
U12	female	60	t	f	f	t	f
U14	female	60	t	f	f	t	f
U16	female	80	t	t	t	f	t
U18	female	100	t	t	t	f	t
U20	female	100	t	t	t	f	t
\.


--
-- PostgreSQL database dump complete
--


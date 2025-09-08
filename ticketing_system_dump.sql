--
-- PostgreSQL database dump
--

\restrict WV0ybeztFX1c5fnLtvc0wkvnQlXgg7tVfQXmJgMj1p7PvJh7CkHdJMLotDx8eMQ

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: paymentstatus; Type: TYPE; Schema: public; Owner: bienvenu
--

CREATE TYPE public.paymentstatus AS ENUM (
    'pending',
    'success',
    'failed'
);


ALTER TYPE public.paymentstatus OWNER TO bienvenu;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO bienvenu;

--
-- Name: bus_routes; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.bus_routes (
    bus_id character varying NOT NULL,
    route_id character varying NOT NULL
);


ALTER TABLE public.bus_routes OWNER TO bienvenu;

--
-- Name: bus_schedules; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.bus_schedules (
    bus_id character varying NOT NULL,
    schedule_id character varying NOT NULL
);


ALTER TABLE public.bus_schedules OWNER TO bienvenu;

--
-- Name: bus_stations; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.bus_stations (
    id character varying NOT NULL,
    name character varying NOT NULL,
    location character varying,
    created_at timestamp without time zone,
    company_id character varying NOT NULL
);


ALTER TABLE public.bus_stations OWNER TO bienvenu;

--
-- Name: buses; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.buses (
    id character varying NOT NULL,
    plate_number character varying NOT NULL,
    capacity integer NOT NULL,
    available_seats integer NOT NULL,
    created_at timestamp without time zone,
    company_id character varying
);


ALTER TABLE public.buses OWNER TO bienvenu;

--
-- Name: companies; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.companies (
    id character varying NOT NULL,
    name character varying NOT NULL,
    email character varying,
    phone_number character varying,
    address character varying,
    created_at timestamp without time zone
);


ALTER TABLE public.companies OWNER TO bienvenu;

--
-- Name: payments; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.payments (
    id character varying NOT NULL,
    ticket_id character varying NOT NULL,
    user_id character varying,
    phone_number character varying(20) NOT NULL,
    amount double precision NOT NULL,
    provider character varying(50) NOT NULL,
    status public.paymentstatus,
    created_at timestamp without time zone
);


ALTER TABLE public.payments OWNER TO bienvenu;

--
-- Name: permissions; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.permissions (
    id character varying NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.permissions OWNER TO bienvenu;

--
-- Name: role_permissions; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.role_permissions (
    role_id character varying NOT NULL,
    permission_id character varying NOT NULL
);


ALTER TABLE public.role_permissions OWNER TO bienvenu;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.roles (
    id character varying NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.roles OWNER TO bienvenu;

--
-- Name: route_segments; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.route_segments (
    id character varying NOT NULL,
    route_id character varying NOT NULL,
    start_station_id character varying NOT NULL,
    end_station_id character varying NOT NULL,
    price double precision NOT NULL,
    stop_order integer NOT NULL,
    company_id character varying
);


ALTER TABLE public.route_segments OWNER TO bienvenu;

--
-- Name: routes; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.routes (
    id character varying NOT NULL,
    price integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    company_id character varying,
    origin_id character varying,
    destination_id character varying
);


ALTER TABLE public.routes OWNER TO bienvenu;

--
-- Name: schedules; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.schedules (
    id character varying NOT NULL,
    departure_time timestamp without time zone NOT NULL,
    arrival_time timestamp without time zone,
    company_id character varying NOT NULL,
    route_segment_id text,
    bus_id character varying
);


ALTER TABLE public.schedules OWNER TO bienvenu;

--
-- Name: tickets; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.tickets (
    id character varying NOT NULL,
    user_id character varying,
    bus_id character varying,
    route_id character varying,
    qr_code character varying NOT NULL,
    status character varying,
    mode character varying,
    created_at timestamp without time zone,
    company_id character varying,
    schedule_id character varying
);


ALTER TABLE public.tickets OWNER TO bienvenu;

--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.user_roles (
    user_id character varying NOT NULL,
    role_id character varying NOT NULL
);


ALTER TABLE public.user_roles OWNER TO bienvenu;

--
-- Name: users; Type: TABLE; Schema: public; Owner: bienvenu
--

CREATE TABLE public.users (
    id character varying NOT NULL,
    full_name character varying NOT NULL,
    email character varying,
    phone_number character varying,
    password_hash character varying NOT NULL,
    created_at timestamp without time zone,
    company_id character varying
);


ALTER TABLE public.users OWNER TO bienvenu;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.alembic_version (version_num) FROM stdin;
2f2287a7dcbd
\.


--
-- Data for Name: bus_routes; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.bus_routes (bus_id, route_id) FROM stdin;
2a22857f-5e2d-4511-a186-118d58928653	b79d130b-f29f-46b4-947c-c15b72f79ba1
\.


--
-- Data for Name: bus_schedules; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.bus_schedules (bus_id, schedule_id) FROM stdin;
\.


--
-- Data for Name: bus_stations; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.bus_stations (id, name, location, created_at, company_id) FROM stdin;
27b22491-d8ac-40a9-847c-f10d93284420	GISIZA	RUTSIRO GISIZA	2025-09-06 23:10:14.157755	b015baa3-1c59-4540-8499-35c86ac55c6b
0711ca8a-54d4-4554-ac5e-f666b8411b56	MUSHUBATI	MUSHUBATI1	2025-09-07 14:13:43.513221	b015baa3-1c59-4540-8499-35c86ac55c6b
\.


--
-- Data for Name: buses; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.buses (id, plate_number, capacity, available_seats, created_at, company_id) FROM stdin;
2a22857f-5e2d-4511-a186-118d58928653	RAB234O	10	1	2025-09-04 12:41:09.15145	\N
a4e42516-c426-415a-b49d-2a458408c7fe	RAB123Z	45	0	2025-09-04 23:30:24.449908	b015baa3-1c59-4540-8499-35c86ac55c6b
72774404-c709-415a-b912-dbdb9d0a9b07	RAD123X	45	0	2025-09-04 23:31:51.026002	fe0e33e3-a4bd-455b-84e0-90620de29226
9cbd20ea-68bb-4301-993e-1a90213f11f7	RAB	20	6	2025-09-04 14:35:33.239188	b015baa3-1c59-4540-8499-35c86ac55c6b
\.


--
-- Data for Name: companies; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.companies (id, name, email, phone_number, address, created_at) FROM stdin;
b015baa3-1c59-4540-8499-35c86ac55c6b	KIVU BELT	kivubelt@gmail.com	0788289198	RUBAVU	2025-09-04 13:53:37.454161
fe0e33e3-a4bd-455b-84e0-90620de29226	VIRUNGA	virunga@gmail.com	0781300739	KIGALI	2025-09-04 23:26:55.128177
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.payments (id, ticket_id, user_id, phone_number, amount, provider, status, created_at) FROM stdin;
\.


--
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.permissions (id, name) FROM stdin;
696f98f1-430a-462b-a810-b22f54fad497	create_user
6516d275-8053-4909-945f-95072286a395	view_user
4a19375c-b6a5-4025-8150-7ac7f4abf8b4	update_user
fc1b8115-ea4a-42b9-ad92-fe8e74042b4a	delete_user
3549f256-c0a7-4b6a-b7c7-dd29af5aeb59	view_ticket
88e41c2c-1af2-4084-bc02-9fe4376dca9d	update_ticket
56cf73f5-c0b5-4a67-b719-f4481b9f9c89	delete_ticket
21f21eea-a334-4793-8f61-68a1b12c494b	create_payment
86d3ba3c-4622-40b8-ad3f-6c879c186b42	view_payment
59bf3bbd-5f74-4e2c-844e-da0c020e3a6b	update_payment
e1b67670-a0cc-4aad-acd8-a861ee52db1c	delete_payment
bac6d055-27db-451e-9598-a41998099439	create_role
f7d245b6-20c6-4383-bc6c-ee558d38e9fd	view_role
28f45dc9-c20a-430a-ac59-251234c91cbc	update_role
eb0c8ff7-d208-4afb-a914-989090b5f819	delete_role
838ca9f5-8dec-4d4e-8117-1a1ea4d23c23	assign_role
1b836d28-3a4a-4318-b339-70ac25cb6e22	access_dashboard
42c7337b-e0de-4da8-9f82-a731d11a2e93	manage_permissions
e9d9702a-864e-4a5c-a3c8-d12cea6adb43	create_permission
41b9c441-56c6-4dd5-a895-e9e236fc900e	assign_permission
91c05ac9-128d-4b34-ae87-53195993779f	get_permission
7b77033b-da6b-4e23-8fde-ee5db856877f	delete_permission
c1f01aa5-e5da-4b58-953b-2d26648276bf	view_users
244422cb-62b0-4699-8b8d-8984dd338116	list_all_roles
64c67587-db9d-411b-93ce-84ca6e4b72f7	create_route
d6b4cf86-aa78-463f-820b-92d4c82209b8	update_route
fc98764c-c410-43da-aba9-66626f75cb5c	delete_route
62f90a53-0629-4c99-9c28-8a6e74559d5d	assign_bus_route
4c356884-8053-456a-8046-17b2034fdfd3	delete_db
972974b8-16f0-4a82-84c2-0f2950c8e9d1	create_ticket
c0b6259e-bb1c-4744-8c46-0ae419431214	see_all_tickets
4b040bc2-03c4-43fc-913c-ba6677658042	delete_bus
254dc576-0a4b-465d-8eaf-b923f95c2018	bus_management
\.


--
-- Data for Name: role_permissions; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.role_permissions (role_id, permission_id) FROM stdin;
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	42c7337b-e0de-4da8-9f82-a731d11a2e93
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	91c05ac9-128d-4b34-ae87-53195993779f
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	e9d9702a-864e-4a5c-a3c8-d12cea6adb43
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	41b9c441-56c6-4dd5-a895-e9e236fc900e
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	244422cb-62b0-4699-8b8d-8984dd338116
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	7b77033b-da6b-4e23-8fde-ee5db856877f
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	bac6d055-27db-451e-9598-a41998099439
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	eb0c8ff7-d208-4afb-a914-989090b5f819
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	64c67587-db9d-411b-93ce-84ca6e4b72f7
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	fc98764c-c410-43da-aba9-66626f75cb5c
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	4b040bc2-03c4-43fc-913c-ba6677658042
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	62f90a53-0629-4c99-9c28-8a6e74559d5d
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	d6b4cf86-aa78-463f-820b-92d4c82209b8
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	696f98f1-430a-462b-a810-b22f54fad497
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	6516d275-8053-4909-945f-95072286a395
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	c1f01aa5-e5da-4b58-953b-2d26648276bf
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	fc1b8115-ea4a-42b9-ad92-fe8e74042b4a
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	4a19375c-b6a5-4025-8150-7ac7f4abf8b4
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	972974b8-16f0-4a82-84c2-0f2950c8e9d1
bf26aad1-17ac-4070-bdb2-8ee2f563a321	972974b8-16f0-4a82-84c2-0f2950c8e9d1
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	3549f256-c0a7-4b6a-b7c7-dd29af5aeb59
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	c0b6259e-bb1c-4744-8c46-0ae419431214
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	254dc576-0a4b-465d-8eaf-b923f95c2018
33fb4194-e371-49d3-bd9e-73247998fd0c	64c67587-db9d-411b-93ce-84ca6e4b72f7
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.roles (id, name) FROM stdin;
bf26aad1-17ac-4070-bdb2-8ee2f563a321	user
bf26aad1-17ac-4070-bdb2-8ee2f563a01d	super_admin
33fb4194-e371-49d3-bd9e-73247998fd0c	company_admin
\.


--
-- Data for Name: route_segments; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.route_segments (id, route_id, start_station_id, end_station_id, price, stop_order, company_id) FROM stdin;
b0bd1b0e-d039-4439-89b9-f421b729755d	9f46328f-0ea2-4ea3-a49e-c2d2aa38335a	27b22491-d8ac-40a9-847c-f10d93284420	0711ca8a-54d4-4554-ac5e-f666b8411b56	800	2	b015baa3-1c59-4540-8499-35c86ac55c6b
\.


--
-- Data for Name: routes; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.routes (id, price, created_at, updated_at, company_id, origin_id, destination_id) FROM stdin;
266ea486-25c9-439d-8c63-7dc652af097e	0	2025-09-07 19:36:01.7204	\N	b015baa3-1c59-4540-8499-35c86ac55c6b	\N	\N
b79d130b-f29f-46b4-947c-c15b72f79ba1	1500	2025-09-04 12:32:44.731842	2025-09-04 12:35:10.83653	\N	27b22491-d8ac-40a9-847c-f10d93284420	0711ca8a-54d4-4554-ac5e-f666b8411b56
ff5d1f48-4e52-47c5-824b-96975d345ef5	500	2025-09-07 21:27:44.409265	\N	b015baa3-1c59-4540-8499-35c86ac55c6b	27b22491-d8ac-40a9-847c-f10d93284420	0711ca8a-54d4-4554-ac5e-f666b8411b56
a72f3402-7cca-492c-9de2-40bc8d114552	500	2025-09-07 21:27:44.409265	\N	b015baa3-1c59-4540-8499-35c86ac55c6b	27b22491-d8ac-40a9-847c-f10d93284420	0711ca8a-54d4-4554-ac5e-f666b8411b56
9f46328f-0ea2-4ea3-a49e-c2d2aa38335a	5000	2025-09-04 15:35:17.054113	2025-09-04 15:35:17.054134	b015baa3-1c59-4540-8499-35c86ac55c6b	27b22491-d8ac-40a9-847c-f10d93284420	0711ca8a-54d4-4554-ac5e-f666b8411b56
\.


--
-- Data for Name: schedules; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.schedules (id, departure_time, arrival_time, company_id, route_segment_id, bus_id) FROM stdin;
8405e22e-653a-4000-b1d7-8cc7016ec01e	2025-09-07 16:18:53.799	2025-09-07 16:18:53.799	b015baa3-1c59-4540-8499-35c86ac55c6b	b0bd1b0e-d039-4439-89b9-f421b729755d	a4e42516-c426-415a-b49d-2a458408c7fe
\.


--
-- Data for Name: tickets; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.tickets (id, user_id, bus_id, route_id, qr_code, status, mode, created_at, company_id, schedule_id) FROM stdin;
c1335cd4-7298-482f-ab6e-2dcbef6b27e9	b460feb3-9db0-41bd-92d4-257281d44fc4	9cbd20ea-68bb-4301-993e-1a90213f11f7	9f46328f-0ea2-4ea3-a49e-c2d2aa38335a	YzEzMzVjZDQtNzI5OC00ODJmLWFiNmUtMmRjYmVmNmIyN2U5Lp9tzSxhdlU96Nqce4XY1aoTU5pHbe2Yj9GYi8krWRpA	booked	active	2025-09-04 17:04:42.81236	b015baa3-1c59-4540-8499-35c86ac55c6b	\N
d910e2e5-3e51-4c10-89e3-fa85cc6f6011	01929ff4-a229-4946-a371-1f1fe951c7f2	9cbd20ea-68bb-4301-993e-1a90213f11f7	9f46328f-0ea2-4ea3-a49e-c2d2aa38335a	ZDkxMGUyZTUtM2U1MS00YzEwLTg5ZTMtZmE4NWNjNmY2MDExLpeXqZVrrBw0KQnGyyS8gLYvGxRXjvjhv1SQ_LMEGekX	cancelled	deleted	2025-09-08 21:57:39.528122	b015baa3-1c59-4540-8499-35c86ac55c6b	\N
2082f5a8-5a53-4b17-969d-2be132f086be	01929ff4-a229-4946-a371-1f1fe951c7f2	9cbd20ea-68bb-4301-993e-1a90213f11f7	9f46328f-0ea2-4ea3-a49e-c2d2aa38335a	MjA4MmY1YTgtNWE1My00YjE3LTk2OWQtMmJlMTMyZjA4NmJlLvdxzgz-zCRgB_EJTxHUfmGOUrKzf1KiKZyxCXLmeUtf	booked	active	2025-09-08 21:59:52.461034	b015baa3-1c59-4540-8499-35c86ac55c6b	\N
\.


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.user_roles (user_id, role_id) FROM stdin;
7314d3b0-20f7-4e4b-9f2a-0a26fcb603a5	bf26aad1-17ac-4070-bdb2-8ee2f563a01d
b460feb3-9db0-41bd-92d4-257281d44fc4	bf26aad1-17ac-4070-bdb2-8ee2f563a321
01929ff4-a229-4946-a371-1f1fe951c7f2	33fb4194-e371-49d3-bd9e-73247998fd0c
c713b0be-ef92-467a-9ba2-f9c6026175a3	33fb4194-e371-49d3-bd9e-73247998fd0c
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: bienvenu
--

COPY public.users (id, full_name, email, phone_number, password_hash, created_at, company_id) FROM stdin;
7314d3b0-20f7-4e4b-9f2a-0a26fcb603a5	Mwis	exaplme@gmail.com	1111111111	$2b$12$zdM8fd69GKDWp8trL188Je6lnyEAG/VE4r79K8c/e/k2zM0aw3Y.K	2025-09-03 23:24:01.119512	\N
b460feb3-9db0-41bd-92d4-257281d44fc4	Bags 	ex@gmail.com	1111111111	$2b$12$JWZB5p00j3dONU.kC4msEON6DO0lAKmLnA6G6VeK5ssMWeSAy38s.	2025-09-04 12:28:27.553459	\N
01929ff4-a229-4946-a371-1f1fe951c7f2	Muns	ex@gmail.com	1111111111	$2b$12$l3eMLSe3RqV.1bZFGOKgw.8WK7C3HRDkH8rJKiOR3hCd6h/8YFPxS	2025-09-04 13:53:37.786898	b015baa3-1c59-4540-8499-35c86ac55c6b
c713b0be-ef92-467a-9ba2-f9c6026175a3	Kans JOSH	ex@gmail.com	1111111111	$2b$12$nicVnNeTcYUHmYVPgvCLBeN2aFM2p2Z/MeNUW7GnTzUlMd87rG7UW	2025-09-04 23:26:55.870081	fe0e33e3-a4bd-455b-84e0-90620de29226
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: bus_routes bus_routes_pkey; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.bus_routes
    ADD CONSTRAINT bus_routes_pkey PRIMARY KEY (bus_id, route_id);


--
-- Name: bus_schedules bus_schedules_pkey; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.bus_schedules
    ADD CONSTRAINT bus_schedules_pkey PRIMARY KEY (bus_id, schedule_id);


--
-- Name: bus_stations bus_stations_pkey; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.bus_stations
    ADD CONSTRAINT bus_stations_pkey PRIMARY KEY (id);


--
-- Name: buses buses_pkey; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.buses
    ADD CONSTRAINT buses_pkey PRIMARY KEY (id);


--
-- Name: buses buses_plate_number_key; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.buses
    ADD CONSTRAINT buses_plate_number_key UNIQUE (plate_number);


--
-- Name: companies companies_email_key; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_email_key UNIQUE (email);


--
-- Name: companies companies_name_key; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_name_key UNIQUE (name);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- Name: permissions permissions_name_key; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_name_key UNIQUE (name);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (role_id, permission_id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: route_segments route_segments_pkey; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.route_segments
    ADD CONSTRAINT route_segments_pkey PRIMARY KEY (id);


--
-- Name: routes routes_pkey; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_pkey PRIMARY KEY (id);


--
-- Name: schedules schedules_pkey; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_pkey PRIMARY KEY (id);


--
-- Name: tickets tickets_pkey; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_pkey PRIMARY KEY (id);


--
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (user_id, role_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_payments_id; Type: INDEX; Schema: public; Owner: bienvenu
--

CREATE INDEX ix_payments_id ON public.payments USING btree (id);


--
-- Name: ix_permissions_id; Type: INDEX; Schema: public; Owner: bienvenu
--

CREATE INDEX ix_permissions_id ON public.permissions USING btree (id);


--
-- Name: ix_roles_id; Type: INDEX; Schema: public; Owner: bienvenu
--

CREATE INDEX ix_roles_id ON public.roles USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: bienvenu
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: bus_routes bus_routes_bus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.bus_routes
    ADD CONSTRAINT bus_routes_bus_id_fkey FOREIGN KEY (bus_id) REFERENCES public.buses(id);


--
-- Name: bus_routes bus_routes_route_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.bus_routes
    ADD CONSTRAINT bus_routes_route_id_fkey FOREIGN KEY (route_id) REFERENCES public.routes(id);


--
-- Name: bus_schedules bus_schedules_bus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.bus_schedules
    ADD CONSTRAINT bus_schedules_bus_id_fkey FOREIGN KEY (bus_id) REFERENCES public.buses(id);


--
-- Name: bus_schedules bus_schedules_schedule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.bus_schedules
    ADD CONSTRAINT bus_schedules_schedule_id_fkey FOREIGN KEY (schedule_id) REFERENCES public.schedules(id);


--
-- Name: bus_stations bus_stations_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.bus_stations
    ADD CONSTRAINT bus_stations_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: buses buses_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.buses
    ADD CONSTRAINT buses_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: payments payments_ticket_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES public.tickets(id);


--
-- Name: payments payments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: role_permissions role_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id);


--
-- Name: role_permissions role_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: route_segments route_segments_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.route_segments
    ADD CONSTRAINT route_segments_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: route_segments route_segments_end_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.route_segments
    ADD CONSTRAINT route_segments_end_station_id_fkey FOREIGN KEY (end_station_id) REFERENCES public.bus_stations(id);


--
-- Name: route_segments route_segments_route_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.route_segments
    ADD CONSTRAINT route_segments_route_id_fkey FOREIGN KEY (route_id) REFERENCES public.routes(id);


--
-- Name: route_segments route_segments_start_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.route_segments
    ADD CONSTRAINT route_segments_start_station_id_fkey FOREIGN KEY (start_station_id) REFERENCES public.bus_stations(id);


--
-- Name: routes routes_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: routes routes_destination_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_destination_fkey FOREIGN KEY (destination_id) REFERENCES public.bus_stations(id);


--
-- Name: routes routes_origin_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_origin_fkey FOREIGN KEY (origin_id) REFERENCES public.bus_stations(id);


--
-- Name: schedules schedules_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: tickets tickets_bus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_bus_id_fkey FOREIGN KEY (bus_id) REFERENCES public.buses(id);


--
-- Name: tickets tickets_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: tickets tickets_route_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_route_id_fkey FOREIGN KEY (route_id) REFERENCES public.routes(id);


--
-- Name: tickets tickets_schedule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_schedule_id_fkey FOREIGN KEY (schedule_id) REFERENCES public.schedules(id);


--
-- Name: tickets tickets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users users_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bienvenu
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO bienvenu;


--
-- PostgreSQL database dump complete
--

\unrestrict WV0ybeztFX1c5fnLtvc0wkvnQlXgg7tVfQXmJgMj1p7PvJh7CkHdJMLotDx8eMQ


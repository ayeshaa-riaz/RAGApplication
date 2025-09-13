--
-- PostgreSQL database dump
--

-- Dumped from database version 14.17 (Homebrew)
-- Dumped by pg_dump version 14.17 (Homebrew)

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

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: chat_messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_messages (
    id integer NOT NULL,
    chat_id integer NOT NULL,
    sender character varying NOT NULL,
    message text NOT NULL,
    created_at timestamp without time zone,
    user_id integer NOT NULL
);


ALTER TABLE public.chat_messages OWNER TO postgres;

--
-- Name: chat_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.chat_messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chat_messages_id_seq OWNER TO postgres;

--
-- Name: chat_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.chat_messages_id_seq OWNED BY public.chat_messages.id;


--
-- Name: chat_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_sessions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp without time zone,
    title character varying NOT NULL
);


ALTER TABLE public.chat_sessions OWNER TO postgres;

--
-- Name: chat_sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.chat_sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chat_sessions_id_seq OWNER TO postgres;

--
-- Name: chat_sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.chat_sessions_id_seq OWNED BY public.chat_sessions.id;


--
-- Name: chat_summaries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_summaries (
    id integer NOT NULL,
    chat_id integer NOT NULL,
    summary_text text NOT NULL,
    last_updated timestamp without time zone
);


ALTER TABLE public.chat_summaries OWNER TO postgres;

--
-- Name: chat_summaries_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.chat_summaries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chat_summaries_id_seq OWNER TO postgres;

--
-- Name: chat_summaries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.chat_summaries_id_seq OWNED BY public.chat_summaries.id;


--
-- Name: user_memory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_memory (
    user_id character varying NOT NULL,
    memory_context character varying,
    last_updated timestamp without time zone DEFAULT now(),
    topics character varying[],
    books_engaged character varying[],
    declined_questions character varying[],
    tone_preference character varying
);


ALTER TABLE public.user_memory OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    password_hash character varying NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: chat_messages id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_messages ALTER COLUMN id SET DEFAULT nextval('public.chat_messages_id_seq'::regclass);


--
-- Name: chat_sessions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_sessions ALTER COLUMN id SET DEFAULT nextval('public.chat_sessions_id_seq'::regclass);


--
-- Name: chat_summaries id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_summaries ALTER COLUMN id SET DEFAULT nextval('public.chat_summaries_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
648ea80e1115
\.


--
-- Data for Name: chat_messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chat_messages (id, chat_id, sender, message, created_at, user_id) FROM stdin;
195	38	user	what is name of story?	2025-04-03 16:29:32.627348	1
196	38	assistant	The name of the story is "The Lost Research Paper."	2025-04-03 16:29:35.319903	1
199	38	user	very bad reason he gave 	2025-04-03 16:30:12.557673	1
200	38	assistant	The hacker's exact motivations are not explicitly stated in the provided context, but the message they left behind—"Innovation belongs to everyone, not just universities"—may offer a hint. It seems that the hacker wanted to make Dr. Carter's research accessible to the public and may have believed that keeping the research within the confines of the university was restricting its reach. It's possible that the hacker saw themselves as a sort of vigilante, trying to "liberate" knowledge and innovation from what they perceived as an exclusive or elitist system.	2025-04-03 16:30:16.820464	1
7	20	user	whoami	2025-03-28 10:37:00.116205	4
8	20	user	who are you	2025-03-28 10:37:29.292555	4
9	20	user	rply me	2025-03-28 10:37:37.356473	4
10	20	user	😩😩😩	2025-03-28 10:37:46.283066	4
145	26	user	what is story about?	2025-04-02 12:21:11.015494	2
197	38	user	why he stole the paper?	2025-04-03 16:29:45.595822	1
146	26	assistant	The story is about a Stanford University AI researcher, Dr. Alice Carter, who encounters a situation where her research paper on "Ethical AI in Healthcare" is stolen. While attending a conference, she realizes that her USB drive containing the final draft of her paper is missing, and upon returning to her office, she finds that her computer has been hacked and the file is gone. With the help of her assistant and a cybersecurity expert, she discovers a cryptic message left by the hacker suggesting that innovation should be accessible to everyone, not just universities. They eventually trace the hacker and find that the paper has been uploaded to an anonymous online forum, and they successfully retrieve the document before any misuse. The story highlights the importance of cybersecurity and the potential risks and consequences of intellectual property theft in academic research.	2025-04-02 12:21:11.019325	2
147	26	user	what is your name	2025-04-02 12:21:41.634227	2
148	26	assistant	I don't have a name.	2025-04-02 12:21:41.637875	2
198	38	assistant	The hacker's exact motivations are not explicitly stated in the provided context. However, the message they left behind, "Innovation belongs to everyone, not just universities," suggests that they wanted to make Dr. Carter's research accessible to the public and may have believed that keeping it confined to academic institutions was contrary to the spirit of sharing and open access. It's possible that the hacker saw themselves as a sort of vigilante, trying to "liberate" knowledge and innovation from what they perceived as exclusivity or gatekeeping by universities.	2025-04-03 16:29:49.175491	1
149	26	user	call me ayesha	2025-04-02 12:22:21.104434	2
150	26	assistant	A good name for the assistant, John Miller, that conveys his role and contribution to the story could be "Reliable Ryan."	2025-04-02 12:22:21.10952	2
\.


--
-- Data for Name: chat_sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chat_sessions (id, user_id, created_at, title) FROM stdin;
18	3	2025-03-27 19:14:50.520287	New Chat 2025-03-27 19:14
20	4	2025-03-28 10:36:53.221607	New Chat 2025-03-28 05:36
21	4	2025-03-28 10:38:29.144089	New Chat 2025-03-28 05:38
26	2	2025-04-02 12:19:33.479964	New Chat 2025-04-02 07:19
34	1	2025-04-03 16:21:22.488095	New Chat 2025-04-03 11:21
38	1	2025-04-03 16:28:58.030109	New Chat 2025-04-03 11:28
39	1	2025-04-07 14:57:48.457233	New Chat 2025-04-07 09:57
40	1	2025-04-07 15:04:10.844518	New Chat 2025-04-07 10:04
41	1	2025-04-07 15:07:15.61913	New Chat 2025-04-07 10:07
42	1	2025-04-17 11:38:09.890212	New Chat 2025-04-17 06:38
43	1	2025-04-17 11:45:19.315278	New Chat 2025-04-17 06:45
\.


--
-- Data for Name: chat_summaries; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chat_summaries (id, chat_id, summary_text, last_updated) FROM stdin;
\.


--
-- Data for Name: user_memory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_memory (user_id, memory_context, last_updated, topics, books_engaged, declined_questions, tone_preference) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password_hash, created_at) FROM stdin;
1	ayesha	ayesha@gmail.com	$2b$12$rQafMJcjAjtEi5hOgYBYCenbmY2xxXchx74EPE3RzTFF7KsyVCQZe	2025-03-26 18:57:51.814627
2	ayesha123	ayesha123@gmail.com	$2b$12$UEUq92UOZ/opvaeX9Zyq0eQnW8eEQQCobTYH6mwPUnNYnTTmqu/9K	2025-03-26 19:05:41.810205
3	ayesha234	ayesha234@gmail.com	$2b$12$Eb7FzBfyFBJ95yIr4pS8TuoiB3NzloeGFQpJPati6vR2QZSDNAhEu	2025-03-26 19:09:34.322613
4	umer	umer...@gmail.com	$2b$12$cgPU9bdR9PyAGHDWYmYK0uzflcEdR5YnsKW/ZE.gaitCFWhgd5rYy	2025-03-28 10:36:24.310038
5			$2b$12$BvzB4LVt5W2QFAmDYvewUOJpNrn2TL5BseIiw.zs7NTHeV0kRY/dW	2025-04-02 15:21:07.928649
\.


--
-- Name: chat_messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chat_messages_id_seq', 200, true);


--
-- Name: chat_sessions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chat_sessions_id_seq', 43, true);


--
-- Name: chat_summaries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chat_summaries_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 5, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: chat_messages chat_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_pkey PRIMARY KEY (id);


--
-- Name: chat_sessions chat_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_sessions
    ADD CONSTRAINT chat_sessions_pkey PRIMARY KEY (id);


--
-- Name: chat_summaries chat_summaries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_summaries
    ADD CONSTRAINT chat_summaries_pkey PRIMARY KEY (id);


--
-- Name: user_memory user_memory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_memory
    ADD CONSTRAINT user_memory_pkey PRIMARY KEY (user_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ix_chat_messages_chat_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_chat_messages_chat_id ON public.chat_messages USING btree (chat_id);


--
-- Name: ix_chat_messages_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_chat_messages_id ON public.chat_messages USING btree (id);


--
-- Name: ix_chat_sessions_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_chat_sessions_id ON public.chat_sessions USING btree (id);


--
-- Name: ix_chat_sessions_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_chat_sessions_user_id ON public.chat_sessions USING btree (user_id);


--
-- Name: ix_chat_summaries_chat_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_chat_summaries_chat_id ON public.chat_summaries USING btree (chat_id);


--
-- Name: ix_chat_summaries_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_chat_summaries_id ON public.chat_summaries USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: chat_messages chat_messages_chat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_chat_id_fkey FOREIGN KEY (chat_id) REFERENCES public.chat_sessions(id);


--
-- Name: chat_messages chat_messages_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: chat_sessions chat_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_sessions
    ADD CONSTRAINT chat_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: chat_summaries chat_summaries_chat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_summaries
    ADD CONSTRAINT chat_summaries_chat_id_fkey FOREIGN KEY (chat_id) REFERENCES public.chat_sessions(id);


--
-- PostgreSQL database dump complete
--


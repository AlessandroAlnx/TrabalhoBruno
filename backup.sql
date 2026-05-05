--
-- PostgreSQL database dump
--

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

-- Database
CREATE DATABASE "Trabalho.bruno" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Portuguese_Brazil.1252';

\connect "Trabalho.bruno"

-- Tables
CREATE TABLE public.usuarios (
    id_usuario integer NOT NULL PRIMARY KEY,
    nome character varying(100) NOT NULL,
    email character varying(100) NOT NULL UNIQUE,
    senha character varying(100) NOT NULL
);

CREATE TABLE public.codigos (
    id_codigo integer NOT NULL PRIMARY KEY,
    usuario_id integer NOT NULL REFERENCES public.usuarios(id_usuario),
    codigo text NOT NULL,
    linguagem character varying(20),
    criado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE public.analises (
    id integer NOT NULL PRIMARY KEY,
    codigo_id integer NOT NULL REFERENCES public.codigos(id_codigo),
    erro text,
    explicacao text,
    codigo_corrigido text,
    nivel_severidade character varying(20),
    criado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE public.logs (
    id integer NOT NULL PRIMARY KEY,
    usuario_id integer NOT NULL REFERENCES public.usuarios(id_usuario),
    acao character varying(100),
    descricao text,
    criado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

-- Sequences
CREATE SEQUENCE public.ususarios_id_login_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE public.codigos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE public.analises_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE public.logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

-- Ownership
ALTER SEQUENCE public.ususarios_id_login_seq OWNED BY public.usuarios.id_usuario;
ALTER SEQUENCE public.codigos_id_seq OWNED BY public.codigos.id_codigo;
ALTER SEQUENCE public.analises_id_seq OWNED BY public.analises.id;
ALTER SEQUENCE public.logs_id_seq OWNED BY public.logs.id;

-- Defaults
ALTER TABLE ONLY public.usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('public.ususarios_id_login_seq'::regclass);
ALTER TABLE ONLY public.codigos ALTER COLUMN id_codigo SET DEFAULT nextval('public.codigos_id_seq'::regclass);
ALTER TABLE ONLY public.analises ALTER COLUMN id SET DEFAULT nextval('public.analises_id_seq'::regclass);
ALTER TABLE ONLY public.logs ALTER COLUMN id SET DEFAULT nextval('public.logs_id_seq'::regclass);

-- Sequence values
SELECT pg_catalog.setval('public.ususarios_id_login_seq', 2, true);
SELECT pg_catalog.setval('public.codigos_id_seq', 1, true);
SELECT pg_catalog.setval('public.analises_id_seq', 1, true);
SELECT pg_catalog.setval('public.logs_id_seq', 1, true);

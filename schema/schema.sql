SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = ON;
SET check_function_bodies = FALSE;
SET client_min_messages = WARNING;
SET search_path = PUBLIC, extensions;
SET default_tablespace = '';
SET default_with_oids = FALSE;

-- this extension allow to generate uuid as default field, gen_random_uuid - function from this extension
-- https://stackoverflow.com/questions/11584749/how-to-create-a-new-database-with-the-hstore-extension-already-installed

-- CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS public.user CASCADE;

CREATE TABLE public.user
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , email VARCHAR(255) UNIQUE
  , password TEXT
  , enabled BOOLEAN DEFAULT TRUE NOT NULL
  , is_expired BOOLEAN DEFAULT FALSE NOT NULL
  , is_locked  BOOLEAN DEFAULT FALSE NOT NULL
  , is_password_expired BOOLEAN DEFAULT FALSE NOT NULL
  , created_date timestamptz NOT NULL DEFAULT now()
  , modife_date timestamptz NOT NULL DEFAULT now()
);
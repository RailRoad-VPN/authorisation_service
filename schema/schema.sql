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
DROP TABLE IF EXISTS public.user_device CASCADE;
DROP TABLE IF EXISTS public.user_vpn_server_config CASCADE;

CREATE TABLE public.user
(
    uuid                  UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , email                 VARCHAR(255) UNIQUE
  , password              TEXT
  , enabled               BOOLEAN DEFAULT TRUE                       NOT NULL
  , is_expired            BOOLEAN DEFAULT FALSE                      NOT NULL
  , is_locked             BOOLEAN DEFAULT FALSE                      NOT NULL
  , is_password_expired   BOOLEAN DEFAULT FALSE                      NOT NULL
  , created_date          TIMESTAMP                                  NOT NULL DEFAULT now()
  , modify_date           TIMESTAMP                                  NOT NULL DEFAULT now()
  , modify_reason         TEXT                                       NOT NULL DEFAULT 'init'
  , pin_code              INT
  , pin_code_expire_date  TIMESTAMP
  , is_pin_code_activated BOOLEAN                                             DEFAULT FALSE
);

CREATE TABLE public.user_device
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , user_uuid UUID REFERENCES public.user(uuid) NOT NULL
  , device_token VARCHAR(256) UNIQUE
  , device_id VARCHAR(500)
  , virtual_ip INET
  , device_ip INET
  , platform_id INT NOT NULL
  , vpn_type_id INT NOT NULL
  , location VARCHAR(256)
  , is_active BOOLEAN DEFAULT TRUE NOT NULL
  , connected_since TIMESTAMP
  , modify_date TIMESTAMP NOT NULL DEFAULT now()
  , modify_reason TEXT NOT NULL DEFAULT 'init'
  , created_date TIMESTAMP DEFAULT NOW() NOT NULL
);

CREATE TABLE public.user_vpn_server_config
(
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL
  , user_uuid UUID NOT NULL
  , configuration TEXT NOT NULL
  , version INT DEFAULT 1 NOT NULL
  , vpn_device_platform_id INT NOT NULL
  , vpn_type_id INT NOT NULL
  , created_date TIMESTAMP NOT NULL DEFAULT now()
  , CONSTRAINT uniq_config UNIQUE (user_uuid, vpn_device_platform_id, vpn_type_id)
);
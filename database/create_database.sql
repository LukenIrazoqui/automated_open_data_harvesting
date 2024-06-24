-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 1.0.0-beta1
-- PostgreSQL version: 15.0
-- Project Site: pgmodeler.io
-- Model Author: ---
-- -- object: pg_database_owner | type: ROLE --
-- -- DROP ROLE IF EXISTS pg_database_owner;
-- CREATE ROLE pg_database_owner WITH 
-- 	INHERIT
-- 	 PASSWORD '********';
-- -- ddl-end --
-- 

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: automated_open_data_harvesting | type: DATABASE --
-- DROP DATABASE IF EXISTS automated_open_data_harvesting;
CREATE DATABASE automated_open_data_harvesting
	ENCODING = 'UTF8'
	LC_COLLATE = 'en_IE.UTF-8'
	LC_CTYPE = 'en_IE.UTF-8'
	TABLESPACE = pg_default
	OWNER = postgres;
-- ddl-end --


-- object: data | type: SCHEMA --
-- DROP SCHEMA IF EXISTS data CASCADE;
CREATE SCHEMA data;
-- ddl-end --
ALTER SCHEMA data OWNER TO postgres;
-- ddl-end --

SET search_path TO pg_catalog,public,data;
-- ddl-end --

-- object: public.bvbv_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.bvbv_id_seq CASCADE;
CREATE SEQUENCE public.bvbv_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.bvbv_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.bvbv | type: TABLE --
-- DROP TABLE IF EXISTS public.bvbv CASCADE;
CREATE TABLE public.bvbv (
	id bigint NOT NULL DEFAULT nextval('public.bvbv_id_seq'::regclass),
	name character varying(32) NOT NULL,
	CONSTRAINT bvbv_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.bvbv OWNER TO postgres;
-- ddl-end --

-- object: public.branches_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.branches_id_seq CASCADE;
CREATE SEQUENCE public.branches_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.branches_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.branches | type: TABLE --
-- DROP TABLE IF EXISTS public.branches CASCADE;
CREATE TABLE public.branches (
	id bigint NOT NULL DEFAULT nextval('public.branches_id_seq'::regclass),
	name character varying(64) NOT NULL,
	CONSTRAINT branches_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.branches OWNER TO postgres;
-- ddl-end --

-- object: public.sub_branches_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.sub_branches_id_seq CASCADE;
CREATE SEQUENCE public.sub_branches_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.sub_branches_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.sub_branches | type: TABLE --
-- DROP TABLE IF EXISTS public.sub_branches CASCADE;
CREATE TABLE public.sub_branches (
	id bigint NOT NULL DEFAULT nextval('public.sub_branches_id_seq'::regclass),
	name character varying(64) NOT NULL,
	CONSTRAINT sub_branches_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.sub_branches OWNER TO postgres;
-- ddl-end --

-- object: public.branches_sub_branches_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.branches_sub_branches_id_seq CASCADE;
CREATE SEQUENCE public.branches_sub_branches_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.branches_sub_branches_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.branches_sub_branches | type: TABLE --
-- DROP TABLE IF EXISTS public.branches_sub_branches CASCADE;
CREATE TABLE public.branches_sub_branches (
	id bigint NOT NULL DEFAULT nextval('public.branches_sub_branches_id_seq'::regclass),
	id_sub_branches bigint NOT NULL,
	id_branches bigint NOT NULL,
	CONSTRAINT branches_sub_branches_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.branches_sub_branches OWNER TO postgres;
-- ddl-end --

-- object: public.precision_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.precision_id_seq CASCADE;
CREATE SEQUENCE public.precision_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.precision_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.precision | type: TABLE --
-- DROP TABLE IF EXISTS public.precision CASCADE;
CREATE TABLE public.precision (
	id bigint NOT NULL DEFAULT nextval('public.precision_id_seq'::regclass),
	name character varying(64) NOT NULL,
	CONSTRAINT precision_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.precision OWNER TO postgres;
-- ddl-end --

-- object: public.region_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.region_id_seq CASCADE;
CREATE SEQUENCE public.region_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.region_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.region | type: TABLE --
-- DROP TABLE IF EXISTS public.region CASCADE;
CREATE TABLE public.region (
	id bigint NOT NULL DEFAULT nextval('public.region_id_seq'::regclass),
	name character varying(64) NOT NULL,
	CONSTRAINT region_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.region OWNER TO postgres;
-- ddl-end --

-- object: public.urls_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.urls_id_seq CASCADE;
CREATE SEQUENCE public.urls_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.urls_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.urls | type: TABLE --
-- DROP TABLE IF EXISTS public.urls CASCADE;
CREATE TABLE public.urls (
	id bigint NOT NULL DEFAULT nextval('public.urls_id_seq'::regclass),
	url text NOT NULL,
	CONSTRAINT urls_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.urls OWNER TO postgres;
-- ddl-end --

-- object: public.sources_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.sources_id_seq CASCADE;
CREATE SEQUENCE public.sources_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.sources_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.sources | type: TABLE --
-- DROP TABLE IF EXISTS public.sources CASCADE;
CREATE TABLE public.sources (
	id bigint NOT NULL DEFAULT nextval('public.sources_id_seq'::regclass),
	name character varying(128) NOT NULL,
	CONSTRAINT sources_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.sources OWNER TO postgres;
-- ddl-end --

-- object: public.datasets_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.datasets_id_seq CASCADE;
CREATE SEQUENCE public.datasets_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.datasets_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.datasets | type: TABLE --
-- DROP TABLE IF EXISTS public.datasets CASCADE;
CREATE TABLE public.datasets (
	id bigint NOT NULL DEFAULT nextval('public.datasets_id_seq'::regclass),
	name character varying(256) NOT NULL,
	id_bvbv bigint,
	id_branches bigint,
	id_sub_branches bigint,
	id_precision bigint,
	id_sources bigint,
	id_region bigint,
	id_urls bigint,
	CONSTRAINT datasets_pk PRIMARY KEY (id),
	CONSTRAINT datasets_uq UNIQUE (name,id_bvbv,id_branches,id_sub_branches,id_precision,id_region,id_sources,id_urls)
);
-- ddl-end --
ALTER TABLE public.datasets OWNER TO postgres;
-- ddl-end --

-- object: public.url_table_mapping_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.url_table_mapping_id_seq CASCADE;
CREATE SEQUENCE public.url_table_mapping_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.url_table_mapping_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.url_table_mapping | type: TABLE --
-- DROP TABLE IF EXISTS public.url_table_mapping CASCADE;
CREATE TABLE public.url_table_mapping (
	id bigint NOT NULL DEFAULT nextval('public.url_table_mapping_id_seq'::regclass),
	id_urls bigint,
	id_table_names bigint,
	CONSTRAINT url_table_mapping_pk PRIMARY KEY (id),
	CONSTRAINT url_table_mapping_uq UNIQUE (id_table_names)
);
-- ddl-end --
ALTER TABLE public.url_table_mapping OWNER TO postgres;
-- ddl-end --

-- object: public.table_names_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.table_names_id_seq CASCADE;
CREATE SEQUENCE public.table_names_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.table_names_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.table_names | type: TABLE --
-- DROP TABLE IF EXISTS public.table_names CASCADE;
CREATE TABLE public.table_names (
	id bigint NOT NULL DEFAULT nextval('public.table_names_id_seq'::regclass),
	name text NOT NULL,
	dynamic boolean NOT NULL DEFAULT false,
	CONSTRAINT table_names_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.table_names OWNER TO postgres;
-- ddl-end --

-- object: public.dinamic_table_mapping_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.dinamic_table_mapping_id_seq CASCADE;
CREATE SEQUENCE public.dinamic_table_mapping_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.dinamic_table_mapping_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.dinamic_data_tables_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.dinamic_data_tables_id_seq CASCADE;
CREATE SEQUENCE public.dinamic_data_tables_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.dinamic_data_tables_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.dynamic_data_table_names | type: TABLE --
-- DROP TABLE IF EXISTS public.dynamic_data_table_names CASCADE;
CREATE TABLE public.dynamic_data_table_names (
	id bigint NOT NULL DEFAULT nextval('public.dinamic_data_tables_id_seq'::regclass),
	name text NOT NULL,
	CONSTRAINT dinamic_data_tables_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.dynamic_data_table_names OWNER TO postgres;
-- ddl-end --

-- object: public.static_data_tables_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.static_data_tables_id_seq CASCADE;
CREATE SEQUENCE public.static_data_tables_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.static_data_tables_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.static_data_table_names | type: TABLE --
-- DROP TABLE IF EXISTS public.static_data_table_names CASCADE;
CREATE TABLE public.static_data_table_names (
	id bigint NOT NULL DEFAULT nextval('public.static_data_tables_id_seq'::regclass),
	name text NOT NULL,
	CONSTRAINT static_data_tables_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.static_data_table_names OWNER TO postgres;
-- ddl-end --

-- object: public.view_names_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.view_names_id_seq CASCADE;
CREATE SEQUENCE public.view_names_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.view_names_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.view_names | type: TABLE --
-- DROP TABLE IF EXISTS public.view_names CASCADE;
CREATE TABLE public.view_names (
	id integer NOT NULL DEFAULT nextval('public.view_names_id_seq'::regclass),
	name text NOT NULL,
	CONSTRAINT view_names_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.view_names OWNER TO postgres;
-- ddl-end --

-- object: public.dinamic_table_mapping_id_seq1 | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.dinamic_table_mapping_id_seq1 CASCADE;
CREATE SEQUENCE public.dinamic_table_mapping_id_seq1
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE public.dinamic_table_mapping_id_seq1 OWNER TO postgres;
-- ddl-end --

-- object: public.dynamic_table_mapping | type: TABLE --
-- DROP TABLE IF EXISTS public.dynamic_table_mapping CASCADE;
CREATE TABLE public.dynamic_table_mapping (
	id serial NOT NULL,
	id_table_names bigint,
	id_static_data_table_names bigint,
	id_dynamic_data_table_names bigint,
	id_view_names integer,
	CONSTRAINT dynamic_table_mapping_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.dynamic_table_mapping OWNER TO postgres;
-- ddl-end --

-- object: table_names_fk | type: CONSTRAINT --
-- ALTER TABLE public.dynamic_table_mapping DROP CONSTRAINT IF EXISTS table_names_fk CASCADE;
ALTER TABLE public.dynamic_table_mapping ADD CONSTRAINT table_names_fk FOREIGN KEY (id_table_names)
REFERENCES public.table_names (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: dynamic_table_mapping_uq | type: CONSTRAINT --
-- ALTER TABLE public.dynamic_table_mapping DROP CONSTRAINT IF EXISTS dynamic_table_mapping_uq CASCADE;
ALTER TABLE public.dynamic_table_mapping ADD CONSTRAINT dynamic_table_mapping_uq UNIQUE (id_table_names);
-- ddl-end --

-- object: static_data_table_names_fk | type: CONSTRAINT --
-- ALTER TABLE public.dynamic_table_mapping DROP CONSTRAINT IF EXISTS static_data_table_names_fk CASCADE;
ALTER TABLE public.dynamic_table_mapping ADD CONSTRAINT static_data_table_names_fk FOREIGN KEY (id_static_data_table_names)
REFERENCES public.static_data_table_names (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: dynamic_table_mapping_uq1 | type: CONSTRAINT --
-- ALTER TABLE public.dynamic_table_mapping DROP CONSTRAINT IF EXISTS dynamic_table_mapping_uq1 CASCADE;
ALTER TABLE public.dynamic_table_mapping ADD CONSTRAINT dynamic_table_mapping_uq1 UNIQUE (id_static_data_table_names);
-- ddl-end --

-- object: dynamic_data_table_names_fk | type: CONSTRAINT --
-- ALTER TABLE public.dynamic_table_mapping DROP CONSTRAINT IF EXISTS dynamic_data_table_names_fk CASCADE;
ALTER TABLE public.dynamic_table_mapping ADD CONSTRAINT dynamic_data_table_names_fk FOREIGN KEY (id_dynamic_data_table_names)
REFERENCES public.dynamic_data_table_names (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: dynamic_table_mapping_uq2 | type: CONSTRAINT --
-- ALTER TABLE public.dynamic_table_mapping DROP CONSTRAINT IF EXISTS dynamic_table_mapping_uq2 CASCADE;
ALTER TABLE public.dynamic_table_mapping ADD CONSTRAINT dynamic_table_mapping_uq2 UNIQUE (id_dynamic_data_table_names);
-- ddl-end --

-- object: view_names_fk | type: CONSTRAINT --
-- ALTER TABLE public.dynamic_table_mapping DROP CONSTRAINT IF EXISTS view_names_fk CASCADE;
ALTER TABLE public.dynamic_table_mapping ADD CONSTRAINT view_names_fk FOREIGN KEY (id_view_names)
REFERENCES public.view_names (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: dynamic_table_mapping_uq3 | type: CONSTRAINT --
-- ALTER TABLE public.dynamic_table_mapping DROP CONSTRAINT IF EXISTS dynamic_table_mapping_uq3 CASCADE;
ALTER TABLE public.dynamic_table_mapping ADD CONSTRAINT dynamic_table_mapping_uq3 UNIQUE (id_view_names);
-- ddl-end --

-- object: sub_branches_fk | type: CONSTRAINT --
-- ALTER TABLE public.branches_sub_branches DROP CONSTRAINT IF EXISTS sub_branches_fk CASCADE;
ALTER TABLE public.branches_sub_branches ADD CONSTRAINT sub_branches_fk FOREIGN KEY (id_sub_branches)
REFERENCES public.sub_branches (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: branches_fk | type: CONSTRAINT --
-- ALTER TABLE public.branches_sub_branches DROP CONSTRAINT IF EXISTS branches_fk CASCADE;
ALTER TABLE public.branches_sub_branches ADD CONSTRAINT branches_fk FOREIGN KEY (id_branches)
REFERENCES public.branches (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: bvbv_fk | type: CONSTRAINT --
-- ALTER TABLE public.datasets DROP CONSTRAINT IF EXISTS bvbv_fk CASCADE;
ALTER TABLE public.datasets ADD CONSTRAINT bvbv_fk FOREIGN KEY (id_bvbv)
REFERENCES public.bvbv (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: branches_fk | type: CONSTRAINT --
-- ALTER TABLE public.datasets DROP CONSTRAINT IF EXISTS branches_fk CASCADE;
ALTER TABLE public.datasets ADD CONSTRAINT branches_fk FOREIGN KEY (id_branches)
REFERENCES public.branches (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: sub_branches_fk | type: CONSTRAINT --
-- ALTER TABLE public.datasets DROP CONSTRAINT IF EXISTS sub_branches_fk CASCADE;
ALTER TABLE public.datasets ADD CONSTRAINT sub_branches_fk FOREIGN KEY (id_sub_branches)
REFERENCES public.sub_branches (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: precision_fk | type: CONSTRAINT --
-- ALTER TABLE public.datasets DROP CONSTRAINT IF EXISTS precision_fk CASCADE;
ALTER TABLE public.datasets ADD CONSTRAINT precision_fk FOREIGN KEY (id_precision)
REFERENCES public.precision (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: sources_fk | type: CONSTRAINT --
-- ALTER TABLE public.datasets DROP CONSTRAINT IF EXISTS sources_fk CASCADE;
ALTER TABLE public.datasets ADD CONSTRAINT sources_fk FOREIGN KEY (id_sources)
REFERENCES public.sources (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: urls_fk | type: CONSTRAINT --
-- ALTER TABLE public.datasets DROP CONSTRAINT IF EXISTS urls_fk CASCADE;
ALTER TABLE public.datasets ADD CONSTRAINT urls_fk FOREIGN KEY (id_urls)
REFERENCES public.urls (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: region_fk | type: CONSTRAINT --
-- ALTER TABLE public.datasets DROP CONSTRAINT IF EXISTS region_fk CASCADE;
ALTER TABLE public.datasets ADD CONSTRAINT region_fk FOREIGN KEY (id_region)
REFERENCES public.region (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: table_names_fk | type: CONSTRAINT --
-- ALTER TABLE public.url_table_mapping DROP CONSTRAINT IF EXISTS table_names_fk CASCADE;
ALTER TABLE public.url_table_mapping ADD CONSTRAINT table_names_fk FOREIGN KEY (id_table_names)
REFERENCES public.table_names (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: urls_fk | type: CONSTRAINT --
-- ALTER TABLE public.url_table_mapping DROP CONSTRAINT IF EXISTS urls_fk CASCADE;
ALTER TABLE public.url_table_mapping ADD CONSTRAINT urls_fk FOREIGN KEY (id_urls)
REFERENCES public.urls (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: "grant_CU_26541e8cda" | type: PERMISSION --
GRANT CREATE,USAGE
   ON SCHEMA public
   TO pg_database_owner;
-- ddl-end --

-- object: "grant_U_cd8e46e7b6" | type: PERMISSION --
GRANT USAGE
   ON SCHEMA public
   TO PUBLIC;
-- ddl-end --



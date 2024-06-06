-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 1.0.0-beta1
-- PostgreSQL version: 15.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: new_database | type: DATABASE --
-- DROP DATABASE IF EXISTS new_database;
CREATE DATABASE automated_open_data_harvesting;
-- ddl-end --

\c automated_open_data_harvesting

-- object: data | type: SCHEMA --
-- DROP SCHEMA IF EXISTS data CASCADE;
CREATE SCHEMA data;
-- ddl-end --
ALTER SCHEMA data OWNER TO postgres;
-- ddl-end --

SET search_path TO pg_catalog,public,data;
-- ddl-end --

-- object: public.bvbv | type: TABLE --
-- DROP TABLE IF EXISTS public.bvbv CASCADE;
CREATE TABLE public.bvbv (
	id bigserial NOT NULL,
	name varchar(32) NOT NULL,
	CONSTRAINT bvbv_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.bvbv OWNER TO postgres;
-- ddl-end --

-- object: public.branches | type: TABLE --
-- DROP TABLE IF EXISTS public.branches CASCADE;
CREATE TABLE public.branches (
	id bigserial NOT NULL,
	name varchar(64) NOT NULL,
	CONSTRAINT branches_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.branches OWNER TO postgres;
-- ddl-end --

-- object: public.sub_branches | type: TABLE --
-- DROP TABLE IF EXISTS public.sub_branches CASCADE;
CREATE TABLE public.sub_branches (
	id bigserial NOT NULL,
	name varchar(64) NOT NULL,
	CONSTRAINT sub_branches_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.sub_branches OWNER TO postgres;
-- ddl-end --

-- object: public.branches_sub_branches | type: TABLE --
-- DROP TABLE IF EXISTS public.branches_sub_branches CASCADE;
CREATE TABLE public.branches_sub_branches (
	id bigserial NOT NULL,
	id_sub_branches bigint NOT NULL,
	id_branches bigint NOT NULL,
	CONSTRAINT branches_sub_branches_pk PRIMARY KEY (id)
);
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

-- object: public.precision | type: TABLE --
-- DROP TABLE IF EXISTS public.precision CASCADE;
CREATE TABLE public.precision (
	id bigserial NOT NULL,
	name varchar(64) NOT NULL,
	CONSTRAINT precision_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.precision OWNER TO postgres;
-- ddl-end --

-- object: public.region | type: TABLE --
-- DROP TABLE IF EXISTS public.region CASCADE;
CREATE TABLE public.region (
	id bigserial NOT NULL,
	name varchar(64) NOT NULL,
	CONSTRAINT region_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.region OWNER TO postgres;
-- ddl-end --

-- object: public.urls | type: TABLE --
-- DROP TABLE IF EXISTS public.urls CASCADE;
CREATE TABLE public.urls (
	id bigserial NOT NULL,
	url text NOT NULL,
	CONSTRAINT urls_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.urls OWNER TO postgres;
-- ddl-end --

-- object: public.sources | type: TABLE --
-- DROP TABLE IF EXISTS public.sources CASCADE;
CREATE TABLE public.sources (
	id bigserial NOT NULL,
	name varchar(128) NOT NULL,
	CONSTRAINT sources_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.sources OWNER TO postgres;
-- ddl-end --

-- object: public.datasets | type: TABLE --
-- DROP TABLE IF EXISTS public.datasets CASCADE;
CREATE TABLE public.datasets (
	id bigserial NOT NULL,
	name varchar(256) NOT NULL,
	id_bvbv bigint,
	id_branches bigint,
	id_sub_branches bigint,
	id_precision bigint,
	id_sources bigint,
	id_region bigint,
	id_urls bigint,
	CONSTRAINT datasets_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.datasets OWNER TO postgres;
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

-- object: datasets_uq | type: CONSTRAINT --
-- ALTER TABLE public.datasets DROP CONSTRAINT IF EXISTS datasets_uq CASCADE;
ALTER TABLE public.datasets ADD CONSTRAINT datasets_uq UNIQUE (name, id_bvbv, id_branches, id_sub_branches, id_precision, id_region, id_sources, id_urls);
-- ddl-end --

-- object: region_fk | type: CONSTRAINT --
-- ALTER TABLE public.datasets DROP CONSTRAINT IF EXISTS region_fk CASCADE;
ALTER TABLE public.datasets ADD CONSTRAINT region_fk FOREIGN KEY (id_region)
REFERENCES public.region (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: public.url_table_mapping | type: TABLE --
-- DROP TABLE IF EXISTS public.url_table_mapping CASCADE;
CREATE TABLE public.url_table_mapping (
	id bigserial,
	id_urls bigint,
	table_name text NOT NULL,
	CONSTRAINT url_table_mapping_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.url_table_mapping OWNER TO postgres;
-- ddl-end --

-- object: urls_fk | type: CONSTRAINT --
-- ALTER TABLE public.url_table_mapping DROP CONSTRAINT IF EXISTS urls_fk CASCADE;
ALTER TABLE public.url_table_mapping ADD CONSTRAINT urls_fk FOREIGN KEY (id_urls)
REFERENCES public.urls (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: url_table_unique_maping | type: CONSTRAINT --
-- ALTER TABLE public.url_table_mapping DROP CONSTRAINT IF EXISTS url_table_unique_maping CASCADE;
ALTER TABLE public.url_table_mapping ADD CONSTRAINT url_table_unique_maping UNIQUE (id_urls,table_name);
-- ddl-end --



PGDMP                     	    {            SPK    10.23    10.23 
    �
           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            �
           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            �
           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false            �
           1262    16394    SPK    DATABASE     �   CREATE DATABASE "SPK" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_Indonesia.1252' LC_CTYPE = 'English_Indonesia.1252';
    DROP DATABASE "SPK";
             postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false            �
           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    3                        3079    12924    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false            �
           0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            �            1259    16401    kamera    TABLE       CREATE TABLE public.kamera (
    id_kamera text NOT NULL,
    harga integer NOT NULL,
    resolusi_sensor character varying NOT NULL,
    rentang_iso character varying NOT NULL,
    kecepatan_rana character varying NOT NULL,
    "jumlah_fStop" character varying NOT NULL
);
    DROP TABLE public.kamera;
       public         postgres    false    3            �
          0    16401    kamera 
   TABLE DATA               p   COPY public.kamera (id_kamera, harga, resolusi_sensor, rentang_iso, kecepatan_rana, "jumlah_fStop") FROM stdin;
    public       postgres    false    196   �       �
   �   x�5�A!C��,���N��p��]���2x�>Ё�!:U��]�+��hA���m	60��+�hG�3�K%=�0���.��p�`_n�I�Ѓr.�#�Z7�`��M�f95�t����-�qF�3��W��_�������,�     
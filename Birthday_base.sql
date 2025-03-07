PGDMP          
            }            birthday    17.2    17.2     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    16462    birthday    DATABASE     |   CREATE DATABASE birthday WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE birthday;
                     postgres    false            �            1259    16468 	   birthdays    TABLE     |   CREATE TABLE public.birthdays (
    user_id bigint,
    id bigint NOT NULL,
    name character(50),
    day character(5)
);
    DROP TABLE public.birthdays;
       public         heap r       postgres    false            �            1259    16493    birthdays_id_seq    SEQUENCE     �   ALTER TABLE public.birthdays ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.birthdays_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               postgres    false    218            �            1259    16515    setting    TABLE     h   CREATE TABLE public.setting (
    user_id bigint,
    language character(2),
    interactive boolean
);
    DROP TABLE public.setting;
       public         heap r       postgres    false            �            1259    16463    user    TABLE     K   CREATE TABLE public."user" (
    id bigint NOT NULL,
    chat_id bigint
);
    DROP TABLE public."user";
       public         heap r       postgres    false            �          0    16468 	   birthdays 
   TABLE DATA           ;   COPY public.birthdays (user_id, id, name, day) FROM stdin;
    public               postgres    false    218   B       �          0    16515    setting 
   TABLE DATA           A   COPY public.setting (user_id, language, interactive) FROM stdin;
    public               postgres    false    220   �       �          0    16463    user 
   TABLE DATA           -   COPY public."user" (id, chat_id) FROM stdin;
    public               postgres    false    217   �       �           0    0    birthdays_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.birthdays_id_seq', 24, true);
          public               postgres    false    219            ,           2606    16488    birthdays birthdays_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.birthdays
    ADD CONSTRAINT birthdays_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.birthdays DROP CONSTRAINT birthdays_pkey;
       public                 postgres    false    218            *           2606    16495    user user_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public."user" DROP CONSTRAINT user_pkey;
       public                 postgres    false    217            -           2606    16496     birthdays birthdays_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.birthdays
    ADD CONSTRAINT birthdays_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);
 J   ALTER TABLE ONLY public.birthdays DROP CONSTRAINT birthdays_user_id_fkey;
       public               postgres    false    4650    218    217            .           2606    16523    setting user_id    FK CONSTRAINT     o   ALTER TABLE ONLY public.setting
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public."user"(id);
 9   ALTER TABLE ONLY public.setting DROP CONSTRAINT user_id;
       public               postgres    false    217    4650    220            �   :   x�34�0�44773�42漰^�T�ih�g`�ehjbldajf4Ǆ<s��b���� ��      �   -   x�34516�0537�*�,�24�0�44773�t-�L����� ��O      �   )   x�34�0�44773�4�3�MM��,L�́�p&W� �@�     
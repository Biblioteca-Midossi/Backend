create table if not exists autori
(
    id_autore serial
        primary key,
    nome      varchar(50),
    cognome   varchar(50)
);

create table if not exists istituti
(
    id_istituto   integer    not null
        primary key,
    nome_istituto varchar(3) not null
);

create table if not exists collocazioni
(
    id_collocazione serial
        primary key,
    id_istituto     integer
        references istituti,
    scaffale        varchar(3)
);

create table if not exists libri
(
    id_collocazione integer
        references collocazioni,
    isbn            varchar(64)                                                         not null,
    titolo          varchar(128),
    genere          varchar(256),
    quantita        integer,
    casa_editrice   varchar(128),
    descrizione     varchar(1024),
    thumbnail_path  varchar(256),
    id_libro        bigint default nextval('sql1259724_5.libri_id_libro_seq'::regclass) not null
        primary key
);

create table if not exists test
(
    test varchar(10)
);

create table if not exists utenti
(
    id_utente   bigint default nextval('sql1259724_5.utenti_id_utente_seq'::regclass) not null
        primary key,
    cognome     varchar(64)                                                           not null,
    nome        varchar(64)                                                           not null,
    id_istituto integer
        references istituti,
    ruolo       integer                                                               not null,
    password    varchar(256)                                                          not null,
    username    varchar(64)                                                           not null,
    email       varchar(384)                                                          not null
);

comment on column utenti.ruolo is 'Utente, Moderatore, Admin, ecc..';

create table if not exists prenotazioni
(
    id_prenotazione     bigint default nextval('sql1259724_5.prenotazioni_id_prenotazione_seq'::regclass) not null
        primary key,
    id_utente           bigint                                                                            not null
        references utenti,
    id_libro            bigint                                                                            not null
        references libri,
    inizio_prenotazione date                                                                              not null,
    fine_prenotazione   date                                                                              not null
);

create table if not exists libro_autori
(
    id_libro  integer not null
        constraint autori_libro_id_libro_fkey
            references libri
            on delete cascade,
    id_autore integer not null
        constraint autori_libro_id_autore_fkey
            references autori
            on delete cascade,
    constraint autori_libro_pkey
        primary key (id_libro, id_autore)
);



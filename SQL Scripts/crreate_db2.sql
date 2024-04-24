create table autori
(
    id_autore int auto_increment
        primary key,
    nome      varchar(50) null,
    cognome   varchar(50) null
);

create table collocazioni
(
    id_collocazione int auto_increment
        primary key,
    id_istituto     int        null,
    scaffale        varchar(3) null
);

create index id_istituto
    on collocazioni (id_istituto);

create table istituti
(
    id_istituto   int        not null
        primary key,
    nome_istituto varchar(3) not null
);

create table libri
(
    id_collocazione int           null,
    id_autore       int           null,
    isbn            varchar(64)   not null,
    titolo          varchar(128)  null,
    genere          varchar(256)  null,
    quantita        int           null,
    casa_editrice   varchar(128)  null,
    descrizione     varchar(1024) null,
    thumbnail_path  varchar(256)  null,
    id_libro
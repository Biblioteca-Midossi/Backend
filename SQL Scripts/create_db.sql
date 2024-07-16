-- create schema if not exists Sql1259724_5; -- very dangerous B)
\c postgres;
set search_path to sql1259724_5; -- It's already there, right? :)

-- Tabella test :P
create table if not exists test(
    test varchar(10)
);

-- Tabella istituti
create table if not exists istituti (
    id_istituto int not null primary key, -- Id dell'istituto
    nome_istituto varchar(3) not null -- Nome dell'istituto
);

-- Tabella collocazioni
create table if not exists collocazioni (
    id_collocazione serial not null PRIMARY KEY, -- Id della collocazione
    id_istituto int, -- Id dell'istituto
    scaffale varchar(3), -- Collocazione

    foreign key (id_istituto) references istituti(id_istituto)
);

-- Tabella utenti
create table if not exists utenti (
    id_utente serial not null primary key, -- Id utente
    cognome varchar(50) not null, -- Cognome utente
    nome varchar(50) not null, -- Nome utente
    id_istituto int, -- Id istituto apparentenenza

    foreign key (id_istituto) references istituti(id_istituto)
);

-- Tabella autori (LIMITE UN AUTORE .. magari descrizione con altri autori. (indviduare Principale autore, loro)
create table if not exists autori (
    id_autore serial primary key, -- Id dell'autore
    nome varchar(50), -- Nome autore
    cognome varchar(50) -- Cognome autore
);

-- Tabella libri
create table if not exists libri (
    id_collocazione int, -- Id della collocazione (posizione, istituto)

    id_autore int, -- Id dell'autore

    isbn varchar(64) not null, -- Identificativo del libro (se c'e gia quantita+=1)
    titolo varchar(128),
    genere varchar(256), -- scolastici, scientifici, letterari, gialli, giornalismo
    quantita int, -- quantita'
    casa_editrice varchar(128), -- Nome casa editrice
    descrizione varchar(1024), -- parole chiavi  per la ricerca... TERZO VOLUME,risorse online,autori secondari,...

    thumbnail_path varchar(256), -- percorso della copertina del libro

    id_libro serial primary key,

    foreign key (id_collocazione) references collocazioni(id_collocazione),
    foreign key (id_autore) references autori(id_autore)
);

-- Tabella prenotazioni
create table if not exists prenotazioni (
    id_prenotazione serial not null primary key, -- Id della prenotazione
    id_utente int not null, -- Id dell'utente che ha effettuato la prenozatione
    id_libro int not null, -- Identificativo del libro
    inizio_prenotazione date not null, -- Data inizio prenotazione
    fine_prenotazione date not null, -- Data fine prenotazione

    foreign key (id_utente) references utenti(id_utente),
    foreign key (id_libro) references libri(id_libro)
);

-- can use this if you don't have root acces, just uncomment
-- grant select, insert on biblioteca to 'biblioteca'@'localhost';

-- Queries to populate PK tables
-- biblioteca.istituti
insert into
    istituti(id_istituto, nome_istituto)
VALUES
    (1, 'ITT'),
    (2, 'LAC'),
    (3, 'LAV'),
    (4, 'EXT')
on conflict do nothing;

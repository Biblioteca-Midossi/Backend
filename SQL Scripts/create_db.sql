create schema if not exists biblioteca;

-- Tabella test :P
create table if not exists biblioteca.test(
    test varchar(10)
);

-- Tabella istituti
create table if not exists biblioteca.istituti (
    id_istituto int not null primary key, -- Id dell'istituto
    nome_istituto varchar(3) not null -- Nome dell'istituto
);

-- Tabella collocazioni
create table if not exists biblioteca.collocazioni (
    id_collocazione int auto_increment not null PRIMARY KEY, -- Id della collocazione
    id_istituto int, -- Id dell'istituto
    scaffale varchar(3), -- Collocazione

    foreign key (id_istituto) references biblioteca.istituti(id_istituto)
);

-- Tabella utenti
create table if not exists biblioteca.utenti (
    id_utente int auto_increment not null primary key, -- Id utente
    cognome varchar(50) not null, -- Cognome utente
    nome varchar(50) not null, -- Nome utente
    id_istituto int, -- Id istituto apparentenenza

    foreign key (id_istituto) references biblioteca.istituti(id_istituto)
);

-- Tabella autori (LIMITE UN AUTORE .. magari descrizione con altri autori. (indviduare Principale autore, loro)
create table if not exists biblioteca.autori (
    id_autore int auto_increment primary key, -- Id dell'autore
    nome varchar(50), -- Nome autore
    cognome varchar(50) -- Cognome autore
);

-- Tabella libri (in FK diretta con tutte le altre tabelle)[primary key .automatic?)
create table if not exists biblioteca.libri (
    id_collocazione int, -- Id della collocazione (posizione, istituto)

    id_autore int, -- Id dell'autore

    isbn varchar(17) not null PRIMARY KEY, -- Identificativo del libro (se c'e gia quantita+=1)
    titolo varchar(100),
    genere varchar(255), -- scolastici, scientifici, letterari, gialli, giornalismo
    quantita int, -- quantita'
    casa_editrice varchar(50), -- Nome casa editrice
    descrizione varchar(1024), -- parole chiavi  per la ricerca... TERZO VOLUME,risorse online,autori secondari,...

    thumbnail_path varchar(255), -- percorso della copertina del libro

    foreign key (id_collocazione) references biblioteca.collocazioni(id_collocazione),
    foreign key (id_autore) references biblioteca.autori(id_autore)
);

-- Tabella prenotazioni
create table if not exists biblioteca.prenotazioni (
    id_prenotazione int not null auto_increment primary key, -- Id della prenotazione
    id_utente int not null, -- Id dell'utente che ha effettuato la prenozatione
    isbn_libro int not null, -- Identificativo del libro
    inizio_prenotazione date not null, -- Data inizio prenotazione
    fine_prenotazione date not null, -- Data fine prenotazione

    foreign key (id_utente) references biblioteca.utenti(id_utente),
    foreign key (isbn_libro) references biblioteca.libri(isbn)
);

-- can use this if you don't have root acces, just uncomment
-- grant select, insert on biblioteca to 'biblioteca'@'localhost';

-- Queries to populate PK tables
-- biblioteca.istituti
insert ignore into
    biblioteca.istituti(id_istituto, nome_istituto)
VALUES
    (1, 'ITT'),
    (2, 'LAC'),
    (3, 'LAV'),
    (4, 'EXT');

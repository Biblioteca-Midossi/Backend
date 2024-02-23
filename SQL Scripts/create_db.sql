create schema biblioteca;

-- Tabella test :P
create table biblioteca.test(
    test varchar(10)
);

-- Tabella istituti
create table biblioteca.istituti (
    id_istituto int auto_increment not null primary key, -- Id dell'istituto
    nome_istituto varchar(50) not null -- Nome dell'istituto
);

-- Tabella collocazioni
create table biblioteca.collocazioni (
    id_collocazione int auto_increment not null PRIMARY KEY, -- Id della collocazione
    id_istituto varchar(30), -- Id dell'istituto
    scaffale varchar(3), -- Collocazione

    foreign key (id_istituto) references biblioteca.istituti(id_istituto)
);

-- Tabella utenti
create table biblioteca.utenti (
    id_utente int auto_increment not null primary key, -- Id utente
    cognome varchar(50) not null, -- Cognome utente
    nome varchar(50) not null, -- Nome utente
    id_istituto int, -- Id istituto apparentenenza

    foreign key (id_istituto) references biblioteca.istituti(id_istituto)
);

-- Tabella autori (LIMITE UN AUTORE .. magari descrizione con altri autori. (indviduare Principale autore, loro)
create table biblioteca.autori (
    id_autore int auto_increment primary key, -- Id dell'autore
    nome varchar(50), -- Nome autore
    cognome varchar(50) -- Cognome autore
);

-- Tabella libri (in FK diretta con tutte le altre tabelle)[primary key .automatic?)
create table biblioteca.libri (
    isbn int not null PRIMARY KEY, -- Identificativo del libro
    titolo varchar(80), -- 80
    genere varchar(30), -- scolasticiscientifici, letterari, gialli, giornalismo
    numero_in_inventario int, -- quantita'
    descrizione varchar(200), -- parole chiavi  per la ricerca... TERZO VOLUME,risorse online,autori secondari,...
    -- ?
    id_collocazione int, -- Id della collocazione (posizione, istituto)
    casa_editrice varchar(50), -- Nome casa editrice
    id_autore int, -- Id dell'autore

    foreign key (id_collocazione) references biblioteca.collocazioni(id_collocazione),
    foreign key (id_autore) references biblioteca.autori(id_autore)
);

-- Tabella prenotazioni
create table biblioteca.prenotazioni (
    id_prenotazione int not null auto_increment primary key, -- Id della prenotazione
    id_utente int not null, -- Id dell'utente che ha effettuato la prenozatione
    isbn_libro int not null, -- Identificativo del libro
    inizio_prenotazione date not null, -- Data inizio prenotazione
    fine_prenotazione date not null, -- Data fine prenotazione

    foreign key (id_utente) references biblioteca.utenti(id_utente),
    foreign key (isbn_libro) references biblioteca.libri(isbn)
)

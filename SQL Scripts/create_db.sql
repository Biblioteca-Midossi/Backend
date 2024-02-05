create schema biblioteca;

-- Tabella test :P
create table biblioteca.test(
    test varchar(10)
);

-- Tabella utenti
create table biblioteca.utenti (
    cognome varchar(50) not null primary key,
    nome varchar(50),
    appartenenza varchar(30), -- itt,ac,av,(esterno)
    libri_in_prestito int
 -- libri_in_richiesta (se online)

);

-- Tabella libri (in FK diretta con tutte le altre tabelle)[primary key .automatic?)
create table biblioteca.libri (
    isbn int not null PRIMARY KEY,
    numeri_in_inventario int, -- quantita
    titolo varchar(80), -- 80
    genere varchar(30), -- scolasticiscientifici, letterari, gialli, giornalismo
    descrizione varchar(200), -- parole chiavi  per la ricerca... TERZO VOLUME,risorse online,autori secondari,...
    -- ?
    id_autore int,
    numero_scaffale int,
    foreign key (id_autore) references biblioteca.autori(id_autore),
    foreign key (numero_scaffale) references biblioteca.collocazioni(numero_scaffale)
);

-- Tabella autori (LIMITE UN AUTORE .. magari descrizione con altri autori. (indviduare Principale autore, loro)
create table biblioteca.autori (
    id_autore int auto_increment primary key,
    nome varchar(50),
    cognome varchar(50),
    casa_editrice varchar(50)
);

-- WIP Tabella collocazioni?????
create table biblioteca.collocazioni (
    numero_scaffale int not null PRIMARY KEY
);


-- ricerca parole chiavi per py

select titolo,numeri_in_inventario,genere,isbn
from biblioteca.libri
-- where descrizione in ({chiave})



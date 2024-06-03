alter table sql1259724_5.utenti
    alter column id_utente type BIGINT using id_utente::BIGINT;

alter table sql1259724_5.prenotazioni
    alter column id_prenotazione type bigint using id_prenotazione::bigint,
    alter column id_utente type bigint using id_utente::bigint,
    alter column id_libro type bigint using id_libro::bigint;

alter table sql1259724_5.libri
    alter column id_libro type bigint using id_libro::bigint;



alter table sql1259724_5.utenti
    add column password varchar(256) not null,
    add column username varchar(64) not null,
    add column ruolo int not null default 0;

alter table sql1259724_5.utenti
    alter column nome type varchar(64) using nome::varchar,
    alter column cognome type varchar(64) using nome::varchar;


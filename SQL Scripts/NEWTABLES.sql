-- create table sql1259724_5.libro_autori
-- (
--     id_libro  integer,
--     id_autore integer,
--
--     primary key (id_libro, id_autore),
--     foreign key (id_libro) references libri(id_libro) on delete cascade,
--     foreign key (id_autore) references autori(id_autore) on delete cascade
-- );
--
-- insert into libro_autori(id_libro, id_autore)
-- select id_libro, id_autore from libri
-- where id_autore is not null;
--
-- select * from libro_autori;
--
-- alter table libri drop column id_autore;
--
-- \d libro_autori;
--
-- SELECT * FROM libro_autori;
--
-- SELECT *
-- FROM pg_stat_activity
-- WHERE state = 'idle in transaction';
--
-- SHOW data_directory;
--
-- CREATE TABLE generi (
--     id_genere SERIAL PRIMARY KEY,
--     nome_genere VARCHAR(256) UNIQUE NOT NULL
-- );
--
-- CREATE TABLE libro_generi (
--     id_libro INTEGER NOT NULL,
--     id_genere INTEGER NOT NULL,
--     PRIMARY KEY (id_libro, id_genere),
--     FOREIGN KEY (id_libro) REFERENCES libri(id_libro) ON DELETE CASCADE,
--     FOREIGN KEY (id_genere) REFERENCES generi(id_genere) ON DELETE CASCADE
-- );
--
-- -- Insert unique genres from existing books
-- INSERT INTO generi (nome_genere)
-- SELECT DISTINCT unnest(string_to_array(genere, ', '))
-- FROM libri
-- WHERE genere IS NOT NULL;
--
-- -- Populate libro_generi table
-- INSERT INTO libro_generi (id_libro, id_genere)
-- SELECT
--     l.id_libro,
--     g.id_genere
-- FROM
--     libri l,
--     generi g
-- WHERE
--     g.nome_genere = ANY(string_to_array(l.genere, ', '));
--
-- -- Remove the old genere column from libri table if desired
-- ALTER TABLE libri DROP COLUMN genere;

-- New alter table utenti 11/12/2024
ALTER TABLE utenti
ADD COLUMN profile_picture VARCHAR(255),
ADD COLUMN bio TEXT,
ADD COLUMN last_login TIMESTAMP,
ADD COLUMN preferred_language VARCHAR(10),
ADD COLUMN notification_settings JSONB;
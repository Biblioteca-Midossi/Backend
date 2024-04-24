alter table biblioteca.libri drop primary key;

alter table biblioteca.libri add column id_libro int auto_increment primary key;
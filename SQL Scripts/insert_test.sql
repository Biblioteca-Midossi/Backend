insert into biblioteca.autori (id_autore, nome, cognome)
values  (2, 'Primo', 'Levi'),
        (3, 'Tatsuki', 'Fujimoto');

insert into biblioteca.collocazioni (id_collocazione, id_istituto, scaffale)
values  (2, 1, 'A02'),
        (3, 2, 'Z99');

insert into biblioteca.libri (id_collocazione, id_autore, isbn, titolo, genere, quantita, casa_editrice, descrizione, thumbnail_path)
values  (2, 2, '978-8806219352', 'Se questo è un uomo', 'Letteratura e narrativa', 1, 'Giulio Einaudi Editore', 'Se questo è un uomo di Primo Levi', 'assets/thumbnails/978-8806219352.png'),
        (3, 3, '978-8891296085', 'Chainsaw Man Volume 1', 'Horror, Azione', 55, 'Planet Manga', 'Primo Volume di Chainsaw Man', 'assets/thumbnails/978-8891296085.png');


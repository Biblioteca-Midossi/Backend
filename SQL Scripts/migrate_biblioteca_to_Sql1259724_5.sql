create schema Sql1259724_5;

rename table biblioteca.autori to Sql1259724_5.autori;
rename table biblioteca.collocazioni to Sql1259724_5.collocazioni;
rename table biblioteca.istituti to Sql1259724_5.istituti;
rename table biblioteca.libri to Sql1259724_5.libri;
rename table biblioteca.prenotazioni to Sql1259724_5.prenotazioni;
rename table biblioteca.test to Sql1259724_5.test;
rename table biblioteca.utenti to Sql1259724_5.utenti;

drop schema biblioteca;
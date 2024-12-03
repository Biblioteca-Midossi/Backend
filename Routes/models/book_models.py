from pydantic import BaseModel


class Book(BaseModel):
    id_collocazione: int | None
    id_autore: int | None
    isbn: str
    titolo: str
    genere: str
    quantita: int
    casa_editrice: str
    descrizione: str
    thumbnail_path: str
    id_libro: int
    nome_autore: str
    cognome_autore: str

    def set_id_collocazione(self, id_collocazione: int):
        self.id_collocazione = id_collocazione

    def set_id_autore(self, id_autore: int):
        self.id_autore = id_autore

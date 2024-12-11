--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 17.2 (Ubuntu 17.2-1.pgdg24.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: sql1259724_5; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA sql1259724_5;


ALTER SCHEMA sql1259724_5 OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: autori; Type: TABLE; Schema: sql1259724_5; Owner: postgres
--

CREATE TABLE sql1259724_5.autori (
    id_autore integer NOT NULL,
    nome character varying(50),
    cognome character varying(50)
);


ALTER TABLE sql1259724_5.autori OWNER TO postgres;

--
-- Name: autori_id_autore_seq; Type: SEQUENCE; Schema: sql1259724_5; Owner: postgres
--

CREATE SEQUENCE sql1259724_5.autori_id_autore_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE sql1259724_5.autori_id_autore_seq OWNER TO postgres;

--
-- Name: autori_id_autore_seq; Type: SEQUENCE OWNED BY; Schema: sql1259724_5; Owner: postgres
--

ALTER SEQUENCE sql1259724_5.autori_id_autore_seq OWNED BY sql1259724_5.autori.id_autore;


--
-- Name: collocazioni; Type: TABLE; Schema: sql1259724_5; Owner: postgres
--

CREATE TABLE sql1259724_5.collocazioni (
    id_collocazione integer NOT NULL,
    id_istituto integer,
    scaffale character varying(3)
);


ALTER TABLE sql1259724_5.collocazioni OWNER TO postgres;

--
-- Name: collocazioni_id_collocazione_seq; Type: SEQUENCE; Schema: sql1259724_5; Owner: postgres
--

CREATE SEQUENCE sql1259724_5.collocazioni_id_collocazione_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE sql1259724_5.collocazioni_id_collocazione_seq OWNER TO postgres;

--
-- Name: collocazioni_id_collocazione_seq; Type: SEQUENCE OWNED BY; Schema: sql1259724_5; Owner: postgres
--

ALTER SEQUENCE sql1259724_5.collocazioni_id_collocazione_seq OWNED BY sql1259724_5.collocazioni.id_collocazione;


--
-- Name: generi; Type: TABLE; Schema: sql1259724_5; Owner: postgres
--

CREATE TABLE sql1259724_5.generi (
    id_genere integer NOT NULL,
    nome_genere character varying(256) NOT NULL
);


ALTER TABLE sql1259724_5.generi OWNER TO postgres;

--
-- Name: generi_id_genere_seq; Type: SEQUENCE; Schema: sql1259724_5; Owner: postgres
--

CREATE SEQUENCE sql1259724_5.generi_id_genere_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE sql1259724_5.generi_id_genere_seq OWNER TO postgres;

--
-- Name: generi_id_genere_seq; Type: SEQUENCE OWNED BY; Schema: sql1259724_5; Owner: postgres
--

ALTER SEQUENCE sql1259724_5.generi_id_genere_seq OWNED BY sql1259724_5.generi.id_genere;


--
-- Name: istituti; Type: TABLE; Schema: sql1259724_5; Owner: postgres
--

CREATE TABLE sql1259724_5.istituti (
    id_istituto integer NOT NULL,
    nome_istituto character varying(3) NOT NULL
);


ALTER TABLE sql1259724_5.istituti OWNER TO postgres;

--
-- Name: libri; Type: TABLE; Schema: sql1259724_5; Owner: postgres
--

CREATE TABLE sql1259724_5.libri (
    id_collocazione integer,
    isbn character varying(64) NOT NULL,
    titolo character varying(128),
    quantita integer,
    casa_editrice character varying(128),
    descrizione character varying(1024),
    thumbnail_path character varying(256),
    id_libro bigint NOT NULL
);


ALTER TABLE sql1259724_5.libri OWNER TO postgres;

--
-- Name: libri_id_libro_seq; Type: SEQUENCE; Schema: sql1259724_5; Owner: postgres
--

CREATE SEQUENCE sql1259724_5.libri_id_libro_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE sql1259724_5.libri_id_libro_seq OWNER TO postgres;

--
-- Name: libri_id_libro_seq; Type: SEQUENCE OWNED BY; Schema: sql1259724_5; Owner: postgres
--

ALTER SEQUENCE sql1259724_5.libri_id_libro_seq OWNED BY sql1259724_5.libri.id_libro;


--
-- Name: libro_autori; Type: TABLE; Schema: sql1259724_5; Owner: postgres
--

CREATE TABLE sql1259724_5.libro_autori (
    id_libro integer NOT NULL,
    id_autore integer NOT NULL
);


ALTER TABLE sql1259724_5.libro_autori OWNER TO postgres;

--
-- Name: libro_generi; Type: TABLE; Schema: sql1259724_5; Owner: postgres
--

CREATE TABLE sql1259724_5.libro_generi (
    id_libro integer NOT NULL,
    id_genere integer NOT NULL
);


ALTER TABLE sql1259724_5.libro_generi OWNER TO postgres;

--
-- Name: prenotazioni; Type: TABLE; Schema: sql1259724_5; Owner: postgres
--

CREATE TABLE sql1259724_5.prenotazioni (
    id_prenotazione bigint NOT NULL,
    id_utente bigint NOT NULL,
    id_libro bigint NOT NULL,
    inizio_prenotazione date NOT NULL,
    fine_prenotazione date NOT NULL
);


ALTER TABLE sql1259724_5.prenotazioni OWNER TO postgres;

--
-- Name: prenotazioni_id_prenotazione_seq; Type: SEQUENCE; Schema: sql1259724_5; Owner: postgres
--

CREATE SEQUENCE sql1259724_5.prenotazioni_id_prenotazione_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE sql1259724_5.prenotazioni_id_prenotazione_seq OWNER TO postgres;

--
-- Name: prenotazioni_id_prenotazione_seq; Type: SEQUENCE OWNED BY; Schema: sql1259724_5; Owner: postgres
--

ALTER SEQUENCE sql1259724_5.prenotazioni_id_prenotazione_seq OWNED BY sql1259724_5.prenotazioni.id_prenotazione;


--
-- Name: test; Type: TABLE; Schema: sql1259724_5; Owner: postgres
--

CREATE TABLE sql1259724_5.test (
    test character varying(10)
);


ALTER TABLE sql1259724_5.test OWNER TO postgres;

--
-- Name: utenti; Type: TABLE; Schema: sql1259724_5; Owner: postgres
--

CREATE TABLE sql1259724_5.utenti (
    id_utente bigint NOT NULL,
    cognome character varying(64) NOT NULL,
    nome character varying(64) NOT NULL,
    id_istituto integer,
    ruolo integer NOT NULL,
    password character varying(256) NOT NULL,
    username character varying(64) NOT NULL,
    email character varying(384) NOT NULL
);


ALTER TABLE sql1259724_5.utenti OWNER TO postgres;

--
-- Name: COLUMN utenti.ruolo; Type: COMMENT; Schema: sql1259724_5; Owner: postgres
--

COMMENT ON COLUMN sql1259724_5.utenti.ruolo IS 'Utente, Moderatore, Admin, ecc..';


--
-- Name: utenti_id_utente_seq; Type: SEQUENCE; Schema: sql1259724_5; Owner: postgres
--

CREATE SEQUENCE sql1259724_5.utenti_id_utente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE sql1259724_5.utenti_id_utente_seq OWNER TO postgres;

--
-- Name: utenti_id_utente_seq; Type: SEQUENCE OWNED BY; Schema: sql1259724_5; Owner: postgres
--

ALTER SEQUENCE sql1259724_5.utenti_id_utente_seq OWNED BY sql1259724_5.utenti.id_utente;


--
-- Name: autori id_autore; Type: DEFAULT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.autori ALTER COLUMN id_autore SET DEFAULT nextval('sql1259724_5.autori_id_autore_seq'::regclass);


--
-- Name: collocazioni id_collocazione; Type: DEFAULT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.collocazioni ALTER COLUMN id_collocazione SET DEFAULT nextval('sql1259724_5.collocazioni_id_collocazione_seq'::regclass);


--
-- Name: generi id_genere; Type: DEFAULT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.generi ALTER COLUMN id_genere SET DEFAULT nextval('sql1259724_5.generi_id_genere_seq'::regclass);


--
-- Name: libri id_libro; Type: DEFAULT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.libri ALTER COLUMN id_libro SET DEFAULT nextval('sql1259724_5.libri_id_libro_seq'::regclass);


--
-- Name: prenotazioni id_prenotazione; Type: DEFAULT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.prenotazioni ALTER COLUMN id_prenotazione SET DEFAULT nextval('sql1259724_5.prenotazioni_id_prenotazione_seq'::regclass);


--
-- Name: utenti id_utente; Type: DEFAULT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.utenti ALTER COLUMN id_utente SET DEFAULT nextval('sql1259724_5.utenti_id_utente_seq'::regclass);


--
-- Data for Name: autori; Type: TABLE DATA; Schema: sql1259724_5; Owner: postgres
--

INSERT INTO sql1259724_5.autori VALUES (1, 'Vale', 'Vale');
INSERT INTO sql1259724_5.autori VALUES (2, 'J.K ', 'Rowling');
INSERT INTO sql1259724_5.autori VALUES (3, 'Italo', 'Calvino');
INSERT INTO sql1259724_5.autori VALUES (42, 'Robert L.', 'Stevenson');
INSERT INTO sql1259724_5.autori VALUES (43, 'STENDHAL', 'LA NEWTON');
INSERT INTO sql1259724_5.autori VALUES (34, 'Luigi', 'Santucci');
INSERT INTO sql1259724_5.autori VALUES (35, 'IGNAZIO', 'SEMILIA');
INSERT INTO sql1259724_5.autori VALUES (36, 'Cesare ', 'Pavese');
INSERT INTO sql1259724_5.autori VALUES (37, 'Albert', 'Camus');
INSERT INTO sql1259724_5.autori VALUES (38, 'Agostino', 'Villa');
INSERT INTO sql1259724_5.autori VALUES (4, 'Alessandro ', 'Manzoni');
INSERT INTO sql1259724_5.autori VALUES (5, 'Riccardo', 'Bacchelli');
INSERT INTO sql1259724_5.autori VALUES (6, 'Joseph', 'Conrad');
INSERT INTO sql1259724_5.autori VALUES (41, 'VASCO ', 'PRATOLINI');
INSERT INTO sql1259724_5.autori VALUES (7, 'Fernanda', 'Pivano');
INSERT INTO sql1259724_5.autori VALUES (40, 'Lev ', 'Tolstoj');
INSERT INTO sql1259724_5.autori VALUES (33, 'Fernando ', 'Pessoa');
INSERT INTO sql1259724_5.autori VALUES (39, 'Gianna', 'Schelotto');
INSERT INTO sql1259724_5.autori VALUES (8, 'Stephen', 'King');
INSERT INTO sql1259724_5.autori VALUES (9, 'Poul', 'Anderson');
INSERT INTO sql1259724_5.autori VALUES (10, 'C.S.', 'Lewis');
INSERT INTO sql1259724_5.autori VALUES (11, 'Giuseppe', 'Marotta');
INSERT INTO sql1259724_5.autori VALUES (12, 'Dino', 'Buzzati');
INSERT INTO sql1259724_5.autori VALUES (13, 'Pieter', 'Aspe');
INSERT INTO sql1259724_5.autori VALUES (14, 'Charlotte', 'Brontë');
INSERT INTO sql1259724_5.autori VALUES (44, 'Cesare', 'Segre');
INSERT INTO sql1259724_5.autori VALUES (45, 'GIORGIO', 'BASSANI');
INSERT INTO sql1259724_5.autori VALUES (46, 'MARIE-AUDE', 'MURAIL');
INSERT INTO sql1259724_5.autori VALUES (47, 'Suzanne', 'Collins');
INSERT INTO sql1259724_5.autori VALUES (48, 'QUIRINO', 'GALLI');
INSERT INTO sql1259724_5.autori VALUES (49, 'GIORGIO', 'MONTEFOSCHI');
INSERT INTO sql1259724_5.autori VALUES (50, 'OTTAVIO', 'SABATUCCI');
INSERT INTO sql1259724_5.autori VALUES (51, 'ALDO', 'GABRIELLI');
INSERT INTO sql1259724_5.autori VALUES (52, 'Marie-Henri', 'Beyle');
INSERT INTO sql1259724_5.autori VALUES (53, 'Elena', 'Ferrante');
INSERT INTO sql1259724_5.autori VALUES (54, 'Khaled ', 'Hosseini');
INSERT INTO sql1259724_5.autori VALUES (55, 'GUY', 'DE MAUPASSANT');
INSERT INTO sql1259724_5.autori VALUES (56, 'ELSA', 'MORANTE');
INSERT INTO sql1259724_5.autori VALUES (57, 'Ernest ', 'Hemingway');
INSERT INTO sql1259724_5.autori VALUES (58, 'PROSPER', 'Mérimée');
INSERT INTO sql1259724_5.autori VALUES (59, 'PATRICK', 'MODIANO');
INSERT INTO sql1259724_5.autori VALUES (60, 'Beppe', 'Fenoglio');
INSERT INTO sql1259724_5.autori VALUES (61, 'Ugo', 'Foscolo');
INSERT INTO sql1259724_5.autori VALUES (62, 'Giacomo', 'Noventa');
INSERT INTO sql1259724_5.autori VALUES (63, 'Paolo', 'Giordano');
INSERT INTO sql1259724_5.autori VALUES (64, 'Ernest', ' Hemingway');
INSERT INTO sql1259724_5.autori VALUES (65, 'MARTIN', 'WALKER');
INSERT INTO sql1259724_5.autori VALUES (66, 'Gustave', 'Flaubert');
INSERT INTO sql1259724_5.autori VALUES (67, 'Anne ', 'Frank');
INSERT INTO sql1259724_5.autori VALUES (68, 'BONAVENTURA', 'TECCHI');
INSERT INTO sql1259724_5.autori VALUES (69, 'Francis', 'Scott Fitzgerald');
INSERT INTO sql1259724_5.autori VALUES (70, 'Johann ', 'Goethe');
INSERT INTO sql1259724_5.autori VALUES (71, 'awd', 'awd');
INSERT INTO sql1259724_5.autori VALUES (72, 'dwa', 'dwa');


--
-- Data for Name: collocazioni; Type: TABLE DATA; Schema: sql1259724_5; Owner: postgres
--

INSERT INTO sql1259724_5.collocazioni VALUES (1, 1, 'F57');
INSERT INTO sql1259724_5.collocazioni VALUES (2, 1, 'A03');
INSERT INTO sql1259724_5.collocazioni VALUES (3, 1, 'C02');
INSERT INTO sql1259724_5.collocazioni VALUES (39, 1, 'B3');
INSERT INTO sql1259724_5.collocazioni VALUES (4, 1, 'A01');
INSERT INTO sql1259724_5.collocazioni VALUES (5, 1, 'B01');
INSERT INTO sql1259724_5.collocazioni VALUES (6, 1, 'C01');
INSERT INTO sql1259724_5.collocazioni VALUES (33, 1, 'A1');
INSERT INTO sql1259724_5.collocazioni VALUES (38, 1, 'B03');
INSERT INTO sql1259724_5.collocazioni VALUES (34, 1, 'A88');
INSERT INTO sql1259724_5.collocazioni VALUES (37, 1, 'B2');
INSERT INTO sql1259724_5.collocazioni VALUES (36, 1, 'C2');
INSERT INTO sql1259724_5.collocazioni VALUES (35, 1, 'B02');
INSERT INTO sql1259724_5.collocazioni VALUES (40, 1, 'A56');
INSERT INTO sql1259724_5.collocazioni VALUES (41, NULL, 'A78');
INSERT INTO sql1259724_5.collocazioni VALUES (42, NULL, 'A56');


--
-- Data for Name: generi; Type: TABLE DATA; Schema: sql1259724_5; Owner: postgres
--

INSERT INTO sql1259724_5.generi VALUES (1, 'Fantascienza');
INSERT INTO sql1259724_5.generi VALUES (2, 'Realismo');
INSERT INTO sql1259724_5.generi VALUES (3, 'Narrativo');
INSERT INTO sql1259724_5.generi VALUES (4, 'Romanzo di formazione');
INSERT INTO sql1259724_5.generi VALUES (5, 'fantasy');
INSERT INTO sql1259724_5.generi VALUES (6, '{dwa}');
INSERT INTO sql1259724_5.generi VALUES (7, 'Letteratura ebraica');
INSERT INTO sql1259724_5.generi VALUES (8, 'Narrativa');
INSERT INTO sql1259724_5.generi VALUES (9, 'Autobiografia');
INSERT INTO sql1259724_5.generi VALUES (10, 'Biografia');
INSERT INTO sql1259724_5.generi VALUES (11, 'NARRATIVA');
INSERT INTO sql1259724_5.generi VALUES (12, 'Narrativa psicologica');
INSERT INTO sql1259724_5.generi VALUES (13, '{awd}');
INSERT INTO sql1259724_5.generi VALUES (14, 'Letteratura di guerra');
INSERT INTO sql1259724_5.generi VALUES (15, 'Narrativa ');
INSERT INTO sql1259724_5.generi VALUES (16, 'Romanzo');


--
-- Data for Name: istituti; Type: TABLE DATA; Schema: sql1259724_5; Owner: postgres
--

INSERT INTO sql1259724_5.istituti VALUES (1, 'ITT');
INSERT INTO sql1259724_5.istituti VALUES (2, 'LAC');
INSERT INTO sql1259724_5.istituti VALUES (3, 'LAV');
INSERT INTO sql1259724_5.istituti VALUES (4, 'EXT');


--
-- Data for Name: libri; Type: TABLE DATA; Schema: sql1259724_5; Owner: postgres
--

INSERT INTO sql1259724_5.libri VALUES (3, '9788804598893', 'Il barone rampante', 1, 'Mondadori', '“Il barone rampante” racconta la vita Cosimo Piovasco di Rondò, primogenito del barone di Rondò. Cosimo il 15 giugno 1767, dopo un litigio con il padre causato dalla stanchezza di dover obbedire alle pretese dei genitori e dai maltrattamenti della sorella Battista, decide di rifugiarsi sugli alberi.', 'assets/thumbnails/6.png', 6);
INSERT INTO sql1259724_5.libri VALUES (5, 'privo03', 'Regina Dell''Aria e Della Notte', 1, 'G.C Sansoni', 'Romanzo Breve', 'assets/thumbnails/20.png', 20);
INSERT INTO sql1259724_5.libri VALUES (5, '9788864110776', 'Caos A Bruges', 1, 'Fazi', 'Romanzo', 'assets/thumbnails/24.png', 24);
INSERT INTO sql1259724_5.libri VALUES (6, '9788854172623', 'Jane Eyre', 1, 'Newton Compton Editori', 'ane Eyre è una bambina orfana che viene accolta presso i parenti dopo la morte dei genitori. In questa sua nuova famiglia Jane è resa oggetto di continui maltrattamenti da parte di una fredda zia e anche da parte degli altri bambini della casa, suoi cugini.', 'assets/thumbnails/25.png', 25);
INSERT INTO sql1259724_5.libri VALUES (2, '9788822711717', 'Il libro dell''inquietudine', 1, 'NEWTON COMPTON EDITORI', 'Il Libro dell''inquietudine (in portoghese, Livro do Desassossego) è una delle maggiori opere dello scrittore portoghese Fernando Pessoa. Si tratta di un''opera postuma e incompiuta, oggi costituita da un''ibrida e innumerevole quantità di pagine scritte, «frammenti, tutto frammenti», come rivela Pessoa in una lettera.', 'assets/thumbnails/27.png', 27);
INSERT INTO sql1259724_5.libri VALUES (5, 'privo04', 'Mezzo Miliardo', 1, 'Bietti', 'Romanzo', 'assets/thumbnails/22.png', 22);
INSERT INTO sql1259724_5.libri VALUES (35, 'privo', 'Il velocifero', 1, 'Oscar Mondadori', 'Il "velocifero", la diligenza dei viaggi celeri del secolo scorso, fa da simbolo per la saga di una grossa e pittoresca famiglia, uomini e bestie, galleggiante sulla Milano della Belle époque.', 'assets/thumbnails/28.png', 28);
INSERT INTO sql1259724_5.libri VALUES (36, '9788894308143', 'VOCI', 1, 'EMIA', 'Che cosa succede se il lavoro te lo strappano via? Quali gli improvvisi cambiamenti che sei costretto ad affrontare nella vita? Diciassette racconti brevi ci fanno conoscere e amare persone a cui è stata sottratta la dignità di avere un lavoro o che stanno combattendo per mantenerne uno. Una visione di reale quotidianità che spinge il lettore in un vortice di forti emozioni e di grandi interrogativi su uno dei problemi più urgenti dei nostri giorni. Una lettura che lascia un monito per chi, operando freddamente in ossequio alle sole leggi dei numeri, non vuole rendersi conto delle possibili umane conseguenze e ci costringe a guardare con occhi diversi chi ne diviene, suo malgrado, vittima. 118 pp.', 'assets/thumbnails/29.png', 29);
INSERT INTO sql1259724_5.libri VALUES (2, '9788806221300', 'LA CASA IN COLLINA', 1, 'Giulio Einaudi editore', 'Cesare Pavese pubblica il romanzo La casa in collina nel 1949 insieme con Il carcere nel volume unico Prima che il gallo canti. Se Il carcere risale al periodo tra il 1938 e il 1939 e rievoca l’esperienza del confino dell’autore a Brancaleone Calabro tra il 1935 e il 1936, La casa in collina indaga le conseguenze psicologiche e sociali del secondo conflitto mondiale e della Resistenza, cui Pavese stesso non partecipa, rifugiandosi, come il protagonista, in campagna. In entrambe le opere la narrazione è dunque fortemente intrisa di elementi autobiografici, che fanno trasparire alcune costanti della poetica di Pavese: il legame disarmonico tra l’intellettuale e la realtà, il rapporto complesso con il mondo rurale delle Langhe contrapposto a quello della città, il ruolo della memoria individuale.', 'assets/thumbnails/30.png', 30);
INSERT INTO sql1259724_5.libri VALUES (2, '9788894602609', 'Albert Camus la peste', 2, 'Salone internazionale del libro Torino', 'La peste è un romanzo dello scrittore francese Albert Camus del 1947. Appena pubblicata, l''opera, che rientra nella produzione di Camus definita "Ciclo della rivolta", riscosse grande successo vendendo oltre 160 000 copie nei primi due anni; ottenne tra l''altro il Prix des Critiques.', 'assets/thumbnails/31.png', 31);
INSERT INTO sql1259724_5.libri VALUES (2, 'privo 09', 'I Cosacchi', 1, 'Arnoldo Mondadori', 'Libro di romanzi', 'assets/thumbnails/32.png', 32);
INSERT INTO sql1259724_5.libri VALUES (35, '8804370084', 'Caino Il buono', 1, 'Arnoldo Mondadori Editore', 'Caino il buono è un libro importante, perché affronta il tema relativamente inedito dei sentimenti maschili, e del rapporto fraterno come garanzia di continuità e di solidarietà. Molti lettori vi potranno trovare una chiave d’interpretazione, se non di soluzione, dei propri conflitti familiari.
Ma è anche un libro che si legge con passione. E ci ricorda ancora una volta che la psicologia è una delle vie regie che portano al Romanzo.', 'assets/thumbnails/33.png', 33);
INSERT INTO sql1259724_5.libri VALUES (2, 'privo 10', 'I Quattro Libri di Lettura', 1, 'Nuova Italia', 'L''opera è il rifacimento di un''antologia pedagogica precedente, il Sillabario (o Abbecedario). Comprendente alcune favole di Esopo in versione libera, il rifacimento di leggende russe o indiane, racconti dei fratelli Grimm e storie vere, il testo veniva utilizzato per un apprendimento critico e attivo.[1] Contiene in 4 volumi rispettivamente 58, 65, 51 e 35 tra favole, storie e poesie.

L''opera era destinata, come disse Tolstoj, «a tutti i fanciulli, da quelli della famiglia imperiale a quelli dei contadini, perché ne traggano le loro prime impressioni poetiche»[2].', 'assets/thumbnails/34.png', 34);
INSERT INTO sql1259724_5.libri VALUES (37, '1', 'IL QUARTIERE', 1, 'ARNOLDO MONDADORI EDITORE', 'Ambientato nel periodo che va dal 1932 al 1939, il romanzo narra delle peripezie amorose di un gruppo di ragazzi appartenenti ad un quartiere popolare di Firenze e più precisamente quello di Santa Croce, colti nel passaggio dall''adolescenza alla prima giovinezza: in pratica si coglie lo sviluppo della loro educazione sentimentale e la formazione di una coscienza politica.

Il romanzo è sostenuto da un intreccio continuo di vicende personali ed affettive nelle quali si muovono i vari personaggi, senza che qualcuno emerga o si riconosca particolarmente, neppure nella figura di Valerio, la voce narrante che si identifica con l''autore (questo tipo di romanzo è detto "corale"). Per cui, all''inizio dell''opera, ci viene immediatamente focalizzata questa sensazione dalla frase “Eravamo creature comuni. Ci bastava un gesto per sollevarci collera o amore”.

', 'assets/thumbnails/35.png', 35);
INSERT INTO sql1259724_5.libri VALUES (2, '9788804658245', 'Hunger Games. La trilogia', 1, 'Oscar mondadori', 'Hunger Games è una serie di romanzi di fantascienza distopica per ragazzi scritta da Suzanne Collins', 'assets/thumbnails/40.png', 40);
INSERT INTO sql1259724_5.libri VALUES (4, 'PRIVO9', 'LA COMMEDIA NOSTRA', 3, 'Gruppo Teatrale Popolare Caprarola', 'Il gruppo teatrale popolare di caprarola ha voluto realizzare questo libro per raccogliere insieme le 5 commedie rappresentate con appassionata disinteressata partecipazione.', 'assets/thumbnails/42.png', 42);
INSERT INTO sql1259724_5.libri VALUES (2, '9788854172432', 'Il rosso e il nero', 1, 'NEWTON COMPTON EDITORI', 'Il rosso e il nero. Cronaca del 1830 è un romanzo storico dello scrittore francese Stendhal. Il protagonista, Julien Sorel, è un giovane uomo della provincia francese di modesta educazione, il quale tenta di salire la scala sociale attraverso una combinazione di talento, duro lavoro, inganno e ipocrisia. ', 'assets/thumbnails/44.png', 44);
INSERT INTO sql1259724_5.libri VALUES (38, '9788866320326', 'L''AMICA GENIALE:Infanzia, adolescenza', 1, 'Edizioni e/o', 'L''amica geniale è un romanzo italiano di Elena Ferrante, pubblicato nel 2011. È il primo volume della serie letteraria omonima, che proseguirà con altri tre romanzi: Storia del nuovo cognome, Storia di chi fugge e di chi resta, Storia della bambina perduta.', 'assets/thumbnails/45.png', 45);
INSERT INTO sql1259724_5.libri VALUES (39, '9788868367305', 'Il Cacciatore di Aquiloni ', 1, 'pickwick', 'Il cacciatore di aquiloni è il primo romanzo dello scrittore afghano-americano Khaled Hosseini, pubblicato nel 2003.', 'assets/thumbnails/46.png', 46);
INSERT INTO sql1259724_5.libri VALUES (4, '88-04-32055-9', 'IL GIARDINO DEI FINZI-CONTINI', 1, 'ARNALDO MONDADORI EDITORE', 'Il giardino dei Finzi-Contini racconta l''amore, l''amicizia, i progetti di vita e le partite a tennis di alcuni ragazzi ebrei di Ferrara perfettamente integrati nella vita della città, durante gli anni dell''università, mentre l''Italia si allea con la Germania ed entra in guerra.', 'assets/thumbnails/38.png', 38);
INSERT INTO sql1259724_5.libri VALUES (4, '978-88-09-75724-0', 'MISS CHARITY', 1, 'GIUNTI', 'Descrizione. Charity è una bambina piena di curiosità, assetata di contatti umani, di parole e di scambi. Vuole partecipare alla vita del mondo. Purtroppo, però, una ragazzina della buona società inglese dell''800 deve tacere, non mostrarsi troppo, salvo che in chiesa.', 'assets/thumbnails/39.png', 39);
INSERT INTO sql1259724_5.libri VALUES (38, '9788866321811', 'Storia del nuovo cognome', 1, 'Edizioni e/o', 'Storia del nuovo cognome è un romanzo del 2012 scritto da Elena Ferrante e pubblicato in Italia da E/O. È il secondo romanzo della serie L''amica geniale, preceduto da L''amica geniale del 2011 e seguito da Storia di chi fugge e di chi resta del 2013 e Storia della bambina perduta del 2014.', 'assets/thumbnails/48.png', 48);
INSERT INTO sql1259724_5.libri VALUES (4, '8804301430', 'morante opere', 1, 'mondadori', 'Elsa Morante è stata una scrittrice, saggista, poetessa e traduttrice italiana di grande rilievo, particolarmente nota per le sue opere narrative del secondo dopoguerra. Tra le sue opere più importanti troviamo', 'assets/thumbnails/49.png', 49);
INSERT INTO sql1259724_5.libri VALUES (38, '9788804701187', 'Il Vecchio E il Mare', 1, 'Mondadori', 'Un uomo può essere distrutto, ma non sconfitto.» Il vecchio e il mare è un breve romanzo dello scrittore americano Ernest Hemingway: scritto nel 1951, fu pubblicato sulla rivista Life nel 1952', 'assets/thumbnails/50.png', 50);
INSERT INTO sql1259724_5.libri VALUES (4, '00000000000', 'RACCONTI E NOVELLE', 1, 'SANSONI EDITORE FIRENZE', 'Firenze, Sansoni, 1966, 16mo brossura con copertina illustrata a colori, pp. 569 (I capolavori, 30).', 'assets/thumbnails/51.png', 51);
INSERT INTO sql1259724_5.libri VALUES (4, '000000000000000000000000000000000000000000000', 'I VIALI DI CIRCONVALLAZIONE', 1, 'RUSCONI EDITORE', 'I viali di circonvallazione (Les Boulevards de ceinture, 1972) è il terzo romanzo dello scrittore francese Patrick Modiano pubblicato in prima edizione il 6 ottobre del 1972 e tradotto in italiano l''anno successivo; nel ''72 vinse il premio Grand prix du roman de l''Académie française.', 'assets/thumbnails/53.png', 53);
INSERT INTO sql1259724_5.libri VALUES (38, '9788804644989', 'Ultime Lettere di Jacopo Ortis', 1, 'Oscarmondadori', 'Le Ultime lettere di Jacopo Ortis è un romanzo epistolare, composto dalle lettere che il Foscolo immagina scritte da un giovane suicida negli ultimi tempi della sua vita a un amico, Lorenzo Alderani. Questi le pubblica, aggiungendo alcuni collegamenti narrativi e descrive, alla fine, la tragica morte del protagonista.', 'assets/thumbnails/55.png', 55);
INSERT INTO sql1259724_5.libri VALUES (38, '9788804666639', 'La Solitudine dei Numeri Primi', 1, 'Oscar Absolute', 'La solitudine dei numeri primi è il primo romanzo di Paolo Giordano. Romanzo di formazione, narra le vite parallele di Alice e Mattia attraverso le vicende spesso dolorose che ne segnano l''infanzia, l''adolescenza e l''età adulta', 'assets/thumbnails/57.png', 57);
INSERT INTO sql1259724_5.libri VALUES (4, '978-88-06-22264-2', 'L''ISOLA DI ARTURO', 1, 'EINAUDI', 'L''isola di Arturo è un romanzo di Elsa Morante (Roma 1912-1985) edito da Einaudi e pubblicato nel 1957. Ha valso alla sua autrice il Premio Strega e si colloca nel filone del neorealismo.', 'assets/thumbnails/58.png', 58);
INSERT INTO sql1259724_5.libri VALUES (38, '978880466324119', 'storia di chi fugge e di chi resta', 1, 'e/o', 'Storia di chi fugge e di chi resta è un romanzo del 2013 della scrittrice italiana Elena Ferrante e pubblicato in Italia da E/O. È il terzo romanzo della serie L''amica geniale, preceduto da Storia del nuovo cognome del 2012 e seguito da Storia della bambina perduta del 2014', 'assets/thumbnails/59.png', 59);
INSERT INTO sql1259724_5.libri VALUES (38, '9788804665021', 'ADDIO ALLE ARMI', 1, 'Oscar mondadori', 'Addio alle armi è una storia di amore e di guerra tra Frederic Henry, un giovane americano ricco, e Catherine Barkley. Ernest Hemingway ha sempre sognato una storia d''amore come questa e la descriveva ispirandosi alle sue esperienze sul fronte di guerra nel 1918 in Italia.', 'assets/thumbnails/60.png', 60);
INSERT INTO sql1259724_5.libri VALUES (4, '978-88-200-4740-5', 'BRUNò IL COMMISSARIO FRANCESE', 1, 'SPERLING & KUPFER', 'Nella cittadina di St. Denis, nel Périgord, la vita scorre tranquilla per Bruno, il capo della polizia locale. Il foie gras è superbo, il vino e i formaggi eccellenti... E in paese non capita mai nulla di grave. Finché un giorno viene scoperto il cadavere sventrato di un uomo, con una svastica incisa sul petto. Da qui cominciano i problemi per il pacioso poliziotto, che tuttavia, proprio grazie ai suoi metodi poco ortodossi, risolverà il caso portando alla luce una verità che affonda le radici nel periodo tormentato della Seconda guerra mondiale. Originale e ben congegnata, la prima indagine dell''investigatore che la critica ha salutato come il "Maigret" del Périgord.', 'assets/thumbnails/61.png', 61);
INSERT INTO sql1259724_5.libri VALUES (38, '9788807900983', 'Madame Bovary', 1, 'Feltrinelli', 'Madame Bovary. Mœurs de province, abbreviato normalmente in Madame Bovary, è uno dei romanzi più importanti di Gustave Flaubert, pubblicato dapprima a puntate sul giornale «La Revue de Paris» tra il 1 ottobre e il 15 dicembre 1856.', 'assets/thumbnails/62.png', 62);
INSERT INTO sql1259724_5.libri VALUES (38, '9788806230142', 'Diario, Anne Frank', 1, 'Einaudi', 'Nel suo diario Anna Frank parla delle angosce, delle illusioni, dei sogni, della speranza, della distribuzione del cibo, dei turni in bagno, del cibo che non arriva, delle malattie temute e dello svolgimento della guerra.', 'assets/thumbnails/63.png', 63);
INSERT INTO sql1259724_5.libri VALUES (3, '978-88-04-66789-6', 'Il visconte dimezzato', 1, 'Mondadori', '"Il visconte dimezzato" di Italo Calvino racconta la storia di Visconte Medardo dimezzato da un cannone: metà gentile, metà crudele. Esplora identità e dualità in un''atmosfera fantastica e sognante.', 'assets/thumbnails/2.png', 2);
INSERT INTO sql1259724_5.libri VALUES (2, '9788804586074', 'Le Cronache di Narnia', 1, 'MONDADORI', 'Le storie delle Cronache di Narnia cominciano proprio da una serie di immagini nella testa del loro autore.

“All’inizio non c’era nessun racconto” scrisse Lewis alcuni anni dopo “solo delle forme”.

Il primo libro della serie, Il leone, la strega e l’armadio, nacque dal “quadro mentale” di un bosco innevato attraverso il quale trotterella frettolosamente un piccolo fauno dalle zampe caprine, che regge un ombrello con una mano e una pila di pacchetti con l’altra.

Il fauno immaginato da Lewis è Mr. Tumnus, la guida di Lucy Pevensie a Narnia, terra incantata di animali parlanti ed eroiche battaglie.', 'assets/thumbnails/21.png', 21);
INSERT INTO sql1259724_5.libri VALUES (2, '9788861752535', 'Lo strano caso del Dr Jekyll e Mr Hyde', 1, 'JoyBooK', 'Lo strano caso del dottor Jekyll e del signor Hyde è un racconto gotico dello scrittore Robert Louis Stevenson. Tratta la storia di un avvocato londinese, Gabriel John Utterson, il quale investiga i singolari episodi tra il suo vecchio amico, il dottor Jekyll, e il malvagio signor Hyde.', 'assets/thumbnails/36.png', 36);
INSERT INTO sql1259724_5.libri VALUES (4, 'PRIVO8', 'LA CANGIARA', 2, 'AGNESOTTI', '“La Congiura dei Lampugnani” è un’opera d’arte di Francesco Hayez che rappresenta un episodio storico avvenuto il 26 dicembre 1476 a Milano. Il dipinto narra il complotto ordito da Giovanni Andrea Lampugnani, Girolamo Olgiati e Carlo Visconti contro il duca Galeazzo Maria Sforza. L’opera è esposta presso la Pinacoteca di Brera a Milano e risale al periodo tra gli anni 1826 e 18291.

Nel dipinto, i tre giovani si apprestano a compiere il loro gesto e salutano il loro protettore, Cola Montano, sotto la statua di Sant’Ambrogio, patrono di Milano. Il duca invece entra nella chiesa sul fondo a sinistra. Hayez ha creato una scenografia medievale, raffigurando l’interno della chiesa in stile Romanico-Gotico, nonostante all’epoca fosse in realtà in stile barocco1.', 'assets/thumbnails/41.png', 41);
INSERT INTO sql1259724_5.libri VALUES (4, '0', 'LA CASA TELLIER', 1, 'SANSONI EDITORE FIRENZE', 'Madame Tellier è una dignitosa vedova senza figli che dirige, senza provare alcun sentimento di vergogna, una casa di tolleranza in Normandia («aveva abbracciato quella professione proprio come avrebbe fatto la modista o la ricamatrice»[1]). La casa è frequentata da composti e abitudinari borghesi della cittadina (l''ex sindaco, l''armatore, il banchiere, ecc.). Madame Tellier si reca con le cinque ragazze della casa in un paesetto per la prima comunione del figlio del fratello. In chiesa, durante la funzione religiosa, le prostitute sentono nostalgia dell''antica purezza, e la loro commossa pietà diventa motivo di edificazione per i fedeli e per il celebrante («Con la vostra fede palese e la vostra pietà così viva, siete state per tutti un salutare esempio»). Terminata la cerimonia, ritornano tutte alla loro vita abituale e, dopo la breve assenza, i clienti le ritrovano più allegre e sensuali.', 'assets/thumbnails/47.png', 47);
INSERT INTO sql1259724_5.libri VALUES (38, '9788866325512', 'Storia della bambina perduta', 1, 'Edizioni e/o', 'Storia della bambina perduta è un romanzo del 2014 della scrittrice Elena Ferrante e pubblicato in Italia da E/O, precisamente il 29 ottobre 2014. È il quarto e ultimo romanzo della tetralogia de L''amica geniale, preceduto da Storia di chi fugge e di chi resta, pubblicato nel 2013.', 'assets/thumbnails/52.png', 52);
INSERT INTO sql1259724_5.libri VALUES (4, '880629363X', 'Il partigiano Johnny', 1, 'Einaudi', 'Il partigiano Johnny è un romanzo autobiografico incompiuto di Beppe Fenoglio pubblicato postumo nel 1968. È considerato uno dei più importanti romanzi sulla Resistenza oltre che del Novecento italiano.', 'assets/thumbnails/54.png', 54);
INSERT INTO sql1259724_5.libri VALUES (38, 'privo104', 'Storia di un eresia', 1, 'Rusconi Editore', 'Questa raccolta di scritti postumi, curata da Franca Noventa e introdotta da un lungo saggio di Rodolfo Quadrelli, è un invito ai lettori affinché riprendano in mano i libri di questo maestro «pericoloso» per gli attuali potenti della cultura italiana. Nella seconda parte del libro si pubblica l’ultima opera di Nd venta, rimasta incompiuta e che doveva comprendere trecento lettere aperte ad amici e a letterati italiani del suo tempo, da Fortini a Debenedetti, da Vittorini a Pampaloni, da Bassani a Sereni, per citarne alcuni. Ne sono giunte a noi soltanto settanta: ma sono un’alta lezione di acutezza critica, di intuizione profetica e di humour.', 'assets/thumbnails/56.png', 56);
INSERT INTO sql1259724_5.libri VALUES (4, '0000000', 'GLI ONESTI', 1, 'BOMPIANI', '(Bagnoregio, Viterbo, 1896 - Roma 1968) narratore e saggista italiano. Germanista, tenne la cattedra di letteratura tedesca nell’ateneo romano. Esordì nella narrativa con Il nome sulla sabbia (1924), pubblicando poi una serie di romanzi, racconti e prose varie che hanno al centro sottili problemi morali e psicologici, indagati secondo un’ottica cristiana e affidati a uno stile d’impronta classica. Fra i suoi libri più riusciti, soprattutto nel disegno di caratteri femminili, si ricordano: Il vento tra le case (1928), Tre storie d’amore (1931), I Villatauri (1935), Ernestina (1936), Valentina Velier (1950), Storie di bestie (1957), Gli egoisti (1959). Numerosi i volumi di saggi: Wackenroder (1927), Carossa (1947), L’arte di Thomas Mann (1956), Svevia, terra di poeti (1964), Goethe scrittore di fiabe (1966), Il senso degli altri (1968).', 'assets/thumbnails/64.png', 64);
INSERT INTO sql1259724_5.libri VALUES (38, '9788822706119', 'Il Grande Gatsby', 1, 'Edizione Integrale', 'Il grande Gatsby è un romanzo di Francis Scott Fitzgerald pubblicato per la prima volta a New York il 10 aprile 1925 e definito da T.S. Eliot «il primo passo in avanti fatto dalla narrativa americana dopo Henry James', 'assets/thumbnails/65.png', 65);
INSERT INTO sql1259724_5.libri VALUES (38, '97888079007863', 'I Dolori del Giovane Werther', 1, 'Demetra', ' dolori del giovane Werther è un romanzo epistolare di Johann Wolfgang Goethe pubblicato nel 1774. Il Werther appartiene all''età giovanile di Goethe ed è considerato opera simbolo del movimento dello Sturm und Drang, anticipando molti temi che saranno propri del romanticismo tedesco', 'assets/thumbnails/66.png', 66);
INSERT INTO sql1259724_5.libri VALUES (6, '9788804668046', 'Il deserto dei Tartari', 1, 'Mondadori', 'Giovanni Drogo, un sottotenente, viene mandato in una lontana fortezza. A nord della fortezza c''è il deserto da cui si attende un''invasione dei tartari. Ma l''invasione, sempre annunciata, non avviene e l''addestramento, i turni di guardia, l''organizzazione militare, appaiono cerimoniali senza senso. Quando Drogo torna in città per una promozione, si accorge di aver perso ogni contatto con il mondo e che ormai la sua unica ragione di vita è l''inutile attesa del nemico. Tornato alla fortezza, si ammala e proprio allora accade l''evento tanto aspettato: i tartari avanzano dal deserto. Nell''emozione e nella confusione del momento, senza che lui possa prendere parte ai preparativi di difesa, Drogo muore, dimenticato da tutti.', 'assets/thumbnails/23.png', 23);
INSERT INTO sql1259724_5.libri VALUES (2, '9788806219352', 'Primo Levi: Se Questo é Un Uomo', 1, 'Einaudi', 'Se questo è un uomo è un''opera memorialistica di Primo Levi scritta tra il dicembre 1945 e il gennaio 1947. Rappresenta la coinvolgente ma meditata testimonianza di quanto vissuto dall''autore nel campo di concentramento di Auschwitz', 'assets/thumbnails/37.png', 37);
INSERT INTO sql1259724_5.libri VALUES (4, '000000000000000000000', 'SI DICE O NON SI DICE', 1, 'MONDADORI', 'Si dice o non si dice? di Aldo Gabrielli, nato dall’attività giornalistica e divulgativa del grande linguista, è una guida pratica ed efficace per tutti coloro che vogliono parlare e scrivere un italiano corretto ma adeguato alle necessità di comunicazione della società attuale. Parte da casi concreti e offre risposte immediate a migliaia di dubbi e domande generati dall’uso quotidiano della lingua. In questa seconda edizione ampliata e aggiornata trovano spazio i dubbi più recenti di grammatica e ortografia che derivano dalla continua evoluzione della lingua viva. Le voci, presentate in ordine alfabetico, sono facilmente reperibili. Per ognuna viene fornita una risposta immediata e chiara, seguita da un approfondimento linguistico per chi voglia saperne di più. Un libro utilissimo per imparare, ma anche piacevole da leggere, per lo stile agile e accattivante e per la ricchezza di notizie curiose, spesso risalenti ai tempi remoti in cui hanno avuto origine la nostra lingua e la nostra cultura.', 'assets/thumbnails/43.png', 43);
INSERT INTO sql1259724_5.libri VALUES (41, 'awd', 'awd', 1, 'awd', 'awd', 'assets/thumbnails/68.png', 68);
INSERT INTO sql1259724_5.libri VALUES (42, 'dwa', 'dwa', 1, 'dwa', 'dwa', 'assets/thumbnails/69.png', 69);


--
-- Data for Name: libro_autori; Type: TABLE DATA; Schema: sql1259724_5; Owner: postgres
--

INSERT INTO sql1259724_5.libro_autori VALUES (6, 3);
INSERT INTO sql1259724_5.libro_autori VALUES (20, 9);
INSERT INTO sql1259724_5.libro_autori VALUES (24, 13);
INSERT INTO sql1259724_5.libro_autori VALUES (25, 14);
INSERT INTO sql1259724_5.libro_autori VALUES (27, 33);
INSERT INTO sql1259724_5.libro_autori VALUES (22, 11);
INSERT INTO sql1259724_5.libro_autori VALUES (28, 34);
INSERT INTO sql1259724_5.libro_autori VALUES (29, 35);
INSERT INTO sql1259724_5.libro_autori VALUES (30, 36);
INSERT INTO sql1259724_5.libro_autori VALUES (31, 37);
INSERT INTO sql1259724_5.libro_autori VALUES (32, 38);
INSERT INTO sql1259724_5.libro_autori VALUES (33, 39);
INSERT INTO sql1259724_5.libro_autori VALUES (34, 40);
INSERT INTO sql1259724_5.libro_autori VALUES (35, 41);
INSERT INTO sql1259724_5.libro_autori VALUES (40, 47);
INSERT INTO sql1259724_5.libro_autori VALUES (42, 50);
INSERT INTO sql1259724_5.libro_autori VALUES (44, 52);
INSERT INTO sql1259724_5.libro_autori VALUES (45, 53);
INSERT INTO sql1259724_5.libro_autori VALUES (46, 54);
INSERT INTO sql1259724_5.libro_autori VALUES (38, 45);
INSERT INTO sql1259724_5.libro_autori VALUES (39, 46);
INSERT INTO sql1259724_5.libro_autori VALUES (48, 53);
INSERT INTO sql1259724_5.libro_autori VALUES (49, 56);
INSERT INTO sql1259724_5.libro_autori VALUES (50, 57);
INSERT INTO sql1259724_5.libro_autori VALUES (51, 58);
INSERT INTO sql1259724_5.libro_autori VALUES (53, 59);
INSERT INTO sql1259724_5.libro_autori VALUES (55, 61);
INSERT INTO sql1259724_5.libro_autori VALUES (57, 63);
INSERT INTO sql1259724_5.libro_autori VALUES (58, 56);
INSERT INTO sql1259724_5.libro_autori VALUES (59, 53);
INSERT INTO sql1259724_5.libro_autori VALUES (60, 64);
INSERT INTO sql1259724_5.libro_autori VALUES (61, 65);
INSERT INTO sql1259724_5.libro_autori VALUES (62, 66);
INSERT INTO sql1259724_5.libro_autori VALUES (63, 67);
INSERT INTO sql1259724_5.libro_autori VALUES (2, 3);
INSERT INTO sql1259724_5.libro_autori VALUES (21, 10);
INSERT INTO sql1259724_5.libro_autori VALUES (36, 42);
INSERT INTO sql1259724_5.libro_autori VALUES (41, 48);
INSERT INTO sql1259724_5.libro_autori VALUES (47, 55);
INSERT INTO sql1259724_5.libro_autori VALUES (52, 53);
INSERT INTO sql1259724_5.libro_autori VALUES (54, 60);
INSERT INTO sql1259724_5.libro_autori VALUES (56, 62);
INSERT INTO sql1259724_5.libro_autori VALUES (64, 68);
INSERT INTO sql1259724_5.libro_autori VALUES (65, 69);
INSERT INTO sql1259724_5.libro_autori VALUES (66, 70);
INSERT INTO sql1259724_5.libro_autori VALUES (23, 12);
INSERT INTO sql1259724_5.libro_autori VALUES (37, 44);
INSERT INTO sql1259724_5.libro_autori VALUES (43, 51);
INSERT INTO sql1259724_5.libro_autori VALUES (68, 71);
INSERT INTO sql1259724_5.libro_autori VALUES (69, 71);
INSERT INTO sql1259724_5.libro_autori VALUES (69, 72);


--
-- Data for Name: libro_generi; Type: TABLE DATA; Schema: sql1259724_5; Owner: postgres
--

INSERT INTO sql1259724_5.libro_generi VALUES (6, 8);
INSERT INTO sql1259724_5.libro_generi VALUES (20, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (24, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (25, 8);
INSERT INTO sql1259724_5.libro_generi VALUES (27, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (22, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (28, 8);
INSERT INTO sql1259724_5.libro_generi VALUES (29, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (30, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (31, 3);
INSERT INTO sql1259724_5.libro_generi VALUES (32, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (33, 8);
INSERT INTO sql1259724_5.libro_generi VALUES (34, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (35, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (40, 1);
INSERT INTO sql1259724_5.libro_generi VALUES (40, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (42, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (44, 12);
INSERT INTO sql1259724_5.libro_generi VALUES (44, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (44, 4);
INSERT INTO sql1259724_5.libro_generi VALUES (45, 8);
INSERT INTO sql1259724_5.libro_generi VALUES (45, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (46, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (38, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (39, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (48, 8);
INSERT INTO sql1259724_5.libro_generi VALUES (49, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (50, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (51, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (53, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (55, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (57, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (58, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (59, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (60, 14);
INSERT INTO sql1259724_5.libro_generi VALUES (60, 8);
INSERT INTO sql1259724_5.libro_generi VALUES (60, 2);
INSERT INTO sql1259724_5.libro_generi VALUES (60, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (61, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (62, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (63, 9);
INSERT INTO sql1259724_5.libro_generi VALUES (63, 10);
INSERT INTO sql1259724_5.libro_generi VALUES (63, 7);
INSERT INTO sql1259724_5.libro_generi VALUES (2, 8);
INSERT INTO sql1259724_5.libro_generi VALUES (21, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (36, 8);
INSERT INTO sql1259724_5.libro_generi VALUES (41, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (47, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (52, 8);
INSERT INTO sql1259724_5.libro_generi VALUES (52, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (54, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (56, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (64, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (65, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (66, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (23, 8);
INSERT INTO sql1259724_5.libro_generi VALUES (37, 16);
INSERT INTO sql1259724_5.libro_generi VALUES (43, 11);
INSERT INTO sql1259724_5.libro_generi VALUES (68, 13);
INSERT INTO sql1259724_5.libro_generi VALUES (69, 6);


--
-- Data for Name: prenotazioni; Type: TABLE DATA; Schema: sql1259724_5; Owner: postgres
--



--
-- Data for Name: test; Type: TABLE DATA; Schema: sql1259724_5; Owner: postgres
--



--
-- Data for Name: utenti; Type: TABLE DATA; Schema: sql1259724_5; Owner: postgres
--

INSERT INTO sql1259724_5.utenti VALUES (1, 'Zito', 'Alessandro', 1, 4, '$2b$12$lV74QV0I3BiKT0b6tDsf7O7.2Fzz2aaGe32F3d8SfAP1gTm.re9x2', 'Ignorance', 'erenblaze32@gmail.com');
INSERT INTO sql1259724_5.utenti VALUES (2, 'Picci', 'Paolo', 3, 3, '$2b$12$LHEfMZZ7.02Ykj9FGaVrR.3JL2AbAIatAouhdmN5wP2/GEkX1Qbta', 'paopicci', 'paopicci@gmail.com');
INSERT INTO sql1259724_5.utenti VALUES (5, 'Ponzio', 'Carlo', 3, 3, '$2b$12$K0fDU2b2M/vmXKR1fY/2k.gZm.x6AufDC/tywqbdVkx/902Jo3lX2', 'ponziocar', 'ponziocar@gmail.com');
INSERT INTO sql1259724_5.utenti VALUES (9, 'awdawd', 'awdawd', 2, 0, '$2b$12$o8373sN2HN.Q1aPyakmug.xkJ6Nk8iEo8mGvxEZ2fMlSxcZkEU3qG', 'awd', 'awdawd@gmail.com');


--
-- Name: autori_id_autore_seq; Type: SEQUENCE SET; Schema: sql1259724_5; Owner: postgres
--

SELECT pg_catalog.setval('sql1259724_5.autori_id_autore_seq', 72, true);


--
-- Name: collocazioni_id_collocazione_seq; Type: SEQUENCE SET; Schema: sql1259724_5; Owner: postgres
--

SELECT pg_catalog.setval('sql1259724_5.collocazioni_id_collocazione_seq', 42, true);


--
-- Name: generi_id_genere_seq; Type: SEQUENCE SET; Schema: sql1259724_5; Owner: postgres
--

SELECT pg_catalog.setval('sql1259724_5.generi_id_genere_seq', 16, true);


--
-- Name: libri_id_libro_seq; Type: SEQUENCE SET; Schema: sql1259724_5; Owner: postgres
--

SELECT pg_catalog.setval('sql1259724_5.libri_id_libro_seq', 69, true);


--
-- Name: prenotazioni_id_prenotazione_seq; Type: SEQUENCE SET; Schema: sql1259724_5; Owner: postgres
--

SELECT pg_catalog.setval('sql1259724_5.prenotazioni_id_prenotazione_seq', 1, false);


--
-- Name: utenti_id_utente_seq; Type: SEQUENCE SET; Schema: sql1259724_5; Owner: postgres
--

SELECT pg_catalog.setval('sql1259724_5.utenti_id_utente_seq', 9, true);


--
-- Name: libro_autori autori_libro_pkey; Type: CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.libro_autori
    ADD CONSTRAINT autori_libro_pkey PRIMARY KEY (id_libro, id_autore);


--
-- Name: autori autori_pkey; Type: CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.autori
    ADD CONSTRAINT autori_pkey PRIMARY KEY (id_autore);


--
-- Name: collocazioni collocazioni_pkey; Type: CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.collocazioni
    ADD CONSTRAINT collocazioni_pkey PRIMARY KEY (id_collocazione);


--
-- Name: generi generi_nome_genere_key; Type: CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.generi
    ADD CONSTRAINT generi_nome_genere_key UNIQUE (nome_genere);


--
-- Name: generi generi_pkey; Type: CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.generi
    ADD CONSTRAINT generi_pkey PRIMARY KEY (id_genere);


--
-- Name: istituti istituti_pkey; Type: CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.istituti
    ADD CONSTRAINT istituti_pkey PRIMARY KEY (id_istituto);


--
-- Name: libri libri_pkey; Type: CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.libri
    ADD CONSTRAINT libri_pkey PRIMARY KEY (id_libro);


--
-- Name: libro_generi libro_generi_pkey; Type: CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.libro_generi
    ADD CONSTRAINT libro_generi_pkey PRIMARY KEY (id_libro, id_genere);


--
-- Name: prenotazioni prenotazioni_pkey; Type: CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.prenotazioni
    ADD CONSTRAINT prenotazioni_pkey PRIMARY KEY (id_prenotazione);


--
-- Name: utenti utenti_pkey; Type: CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.utenti
    ADD CONSTRAINT utenti_pkey PRIMARY KEY (id_utente);


--
-- Name: libro_autori autori_libro_id_autore_fkey; Type: FK CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.libro_autori
    ADD CONSTRAINT autori_libro_id_autore_fkey FOREIGN KEY (id_autore) REFERENCES sql1259724_5.autori(id_autore) ON DELETE CASCADE;


--
-- Name: libro_autori autori_libro_id_libro_fkey; Type: FK CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.libro_autori
    ADD CONSTRAINT autori_libro_id_libro_fkey FOREIGN KEY (id_libro) REFERENCES sql1259724_5.libri(id_libro) ON DELETE CASCADE;


--
-- Name: collocazioni collocazioni_id_istituto_fkey; Type: FK CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.collocazioni
    ADD CONSTRAINT collocazioni_id_istituto_fkey FOREIGN KEY (id_istituto) REFERENCES sql1259724_5.istituti(id_istituto);


--
-- Name: libri libri_id_collocazione_fkey; Type: FK CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.libri
    ADD CONSTRAINT libri_id_collocazione_fkey FOREIGN KEY (id_collocazione) REFERENCES sql1259724_5.collocazioni(id_collocazione);


--
-- Name: libro_generi libro_generi_id_genere_fkey; Type: FK CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.libro_generi
    ADD CONSTRAINT libro_generi_id_genere_fkey FOREIGN KEY (id_genere) REFERENCES sql1259724_5.generi(id_genere) ON DELETE CASCADE;


--
-- Name: libro_generi libro_generi_id_libro_fkey; Type: FK CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.libro_generi
    ADD CONSTRAINT libro_generi_id_libro_fkey FOREIGN KEY (id_libro) REFERENCES sql1259724_5.libri(id_libro) ON DELETE CASCADE;


--
-- Name: prenotazioni prenotazioni_id_libro_fkey; Type: FK CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.prenotazioni
    ADD CONSTRAINT prenotazioni_id_libro_fkey FOREIGN KEY (id_libro) REFERENCES sql1259724_5.libri(id_libro);


--
-- Name: prenotazioni prenotazioni_id_utente_fkey; Type: FK CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.prenotazioni
    ADD CONSTRAINT prenotazioni_id_utente_fkey FOREIGN KEY (id_utente) REFERENCES sql1259724_5.utenti(id_utente);


--
-- Name: utenti utenti_id_istituto_fkey; Type: FK CONSTRAINT; Schema: sql1259724_5; Owner: postgres
--

ALTER TABLE ONLY sql1259724_5.utenti
    ADD CONSTRAINT utenti_id_istituto_fkey FOREIGN KEY (id_istituto) REFERENCES sql1259724_5.istituti(id_istituto);


--
-- PostgreSQL database dump complete
--


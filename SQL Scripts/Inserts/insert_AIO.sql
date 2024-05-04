insert into Sql1259724_5.autori (id_autore, nome, cognome)
values  (1, 'Vale', 'Vale'),
        (2, 'J.K ', 'Rowling'),
        (3, 'Italo', 'Calvino'),
        (42, 'Robert L.', 'Stevenson'),
        (43, 'STENDHAL', 'LA NEWTON'),
        (34, 'Luigi', 'Santucci'),
        (35, 'IGNAZIO', 'SEMILIA'),
        (36, 'Cesare ', 'Pavese'),
        (37, 'Albert', 'Camus'),
        (38, 'Agostino', 'Villa'),
        (4, 'Alessandro ', 'Manzoni'),
        (5, 'Riccardo', 'Bacchelli'),
        (6, 'Joseph', 'Conrad'),
        (41, 'VASCO ', 'PRATOLINI'),
        (7, 'Fernanda', 'Pivano'),
        (40, 'Lev ', 'Tolstoj'),
        (33, 'Fernando ', 'Pessoa'),
        (39, 'Gianna', 'Schelotto'),
        (8, 'Stephen', 'King'),
        (9, 'Poul', 'Anderson'),
        (10, 'C.S.', 'Lewis'),
        (11, 'Giuseppe', 'Marotta'),
        (12, 'Dino', 'Buzzati'),
        (13, 'Pieter', 'Aspe'),
        (14, 'Charlotte', 'Brontë'),
        (44, 'Cesare', 'Segre');

insert into Sql1259724_5.istituti (id_istituto, nome_istituto)
values  (1, 'ITT'),
        (2, 'LAC'),
        (3, 'LAV'),
        (4, 'EXT');

insert into Sql1259724_5.collocazioni (id_collocazione, id_istituto, scaffale)
values  (1, 1, 'F57'),
        (2, 1, 'A03'),
        (3, 1, 'C02'),
        (4, 1, 'A01'),
        (5, 1, 'B01'),
        (6, 1, 'C01'),
        (33, 1, 'A1'),
        (34, 1, 'A88'),
        (37, 1, 'B2'),
        (36, 1, 'C2'),
        (35, 1, 'B02');

insert into Sql1259724_5.libri (id_collocazione, id_autore, isbn, titolo, genere, quantita, casa_editrice, descrizione, thumbnail_path, id_libro)
values  (1, 1, 'Vale', 'Vale', 'Vale', 7, 'Vale', 'Vale', 'assets/thumbnails/VALE.png', 1),
        (3, 3, '978-88-04-66789-6', 'Il visconte dimezzato', 'Narrativa', 1, 'Mondadori', '"Il visconte dimezzato" di Italo Calvino racconta la storia di Visconte Medardo dimezzato da un cannone: metà gentile, metà crudele. Esplora identità e dualità in un''atmosfera fantastica e sognante.', 'assets/thumbnails/978-88-04-66789-6.png', 2),
        (3, 3, '978-88-04-66795-7', 'Il cavaliere inesistente', 'Narrativa', 1, 'Mondadori', '"Il cavaliere inesistente" di Italo Calvino segue le gesta di Agilulfo, un cavaliere che non esiste fisicamente ma incarna l''ideale cavalleresco. La storia esplora temi di onore, identità e realtà in un contesto fantastico-medievale.', 'assets/thumbnails/978-88-04-66795-7.png', 3),
        (3, 3, '978-88-04-63713-4', 'Il sentiero dei nidi di ragno', 'Narrativa', 1, 'Mondadori', '"Il sentiero dei nidi di ragno" di Italo Calvino segue la crescita di Pin, un ragazzo durante la Seconda Guerra Mondiale. Ambientato in Liguria, il romanzo esplora l''infanzia, la guerra e la ricerca di significato in un mondo in tumulto.', 'assets/thumbnails/978-88-04-63713-4.png', 4),
        (2, 2, '9788893817035', 'Harry Potter e la camera dei segreti', 'Narrativa', 1, 'SALANI EDITORE', 'Harry Potter e la camera dei segreti (titolo originale in inglese: Harry Potter and the Chamber of Secrets) è il secondo romanzo della saga high fantasy Harry Potter, scritta da J. K. Rowling ', 'assets/thumbnails/9788893817035.png', 5),
        (3, 3, '9788804598893', 'Il barone rampante', 'Narrativa', 1, 'Mondadori', '“Il barone rampante” racconta la vita Cosimo Piovasco di Rondò, primogenito del barone di Rondò. Cosimo il 15 giugno 1767, dopo un litigio con il padre causato dalla stanchezza di dover obbedire alle pretese dei genitori e dai maltrattamenti della sorella Battista, decide di rifugiarsi sugli alberi.', 'assets/thumbnails/9788804598893.png', 6),
        (2, 2, '9788893817066', 'Harry Potter e l''Ordine della Fenice', 'fantasy', 1, 'salani', 'harry potter', 'assets/thumbnails/9788893817066.png', 7),
        (4, 4, '9788826816586', 'I Promessi Sposi', 'Narrativa ', 1, 'Atlas', 'I Promessi sposi sono un romanzo storico ambientato nella Lombardia del 1628-1630, che ha per protagonisti i giovani Renzo Tramaglino e Lucia Mondella il cui matrimonio viene impedito dal signorotto del loro paese, don Rodrigo, a causa di una futile scommessa col cugino Attilio.', 'assets/thumbnails/9788826816586.png', 8),
        (5, 5, 'privo01', 'Il Mulino Di Po', 'Romanzo', 1, 'Arnoldo Mondatori', 'Romanzo Storico', 'assets/thumbnails/privo01.png', 9),
        (6, 6, '9788818018950', 'Cuore di tenebra', 'Narrativa', 1, 'Rusconi libri', 'Marlow, la voce narrante di questo romanzo racconta la storia di Kurtz, misterioso personaggio che vive tra i nativi del Congo,guidandoli nelle loro scorribande per razziare avorio. A loro volta gli indigeni lo venerano come un dio in rituali dall''inaudita crudeltà. Marlow parte alla ricerca di Kurtz in quello che più che un viaggio verso una meta si rivela l''esplorazione dell'' "orrore" di una conoscenza che significa riconoscere fino in fondo il brutto di se stesso e della propria civiltà.', 'assets/thumbnails/9788818018950.png', 10),
        (2, 2, '9788893817059', 'Harry Potter e il calice di fuoco', 'NARRATIVA', 1, 'SALANI EDITORE', 'un momento cruciale nella vita di Harry Potter: ormai è un mago adolescente, vuole andarsene dalla casa dei pestiferi Dursley, vuole sognare la cercatrice del Corvonero per cui ha una cotta tremenda... E poi vuole scoprire quali sono i grandiosi avvenimenti che si terranno a Hogwarts e che riguarderanno altre due scuole di magia e una grande competizione che non si svolge da cento anni. Harry Potter vuole davvero essere un normale mago di quattordici anni. Ma sfortunatamente, Harry non è un mago normale. E stavolta la differenza può essergli fatale. Età di lettura: da 8 anni.', 'assets/thumbnails/9788893817059.png', 11),
        (5, 7, '8804116382', 'Ernest Hemingway', 'Romanzo', 1, 'Arnoldo Mondatori', 'Romanzi e Racconti', 'assets/thumbnails/8804116382.png', 12),
        (2, 2, '9788893817028', 'Harry Potter e la pietra filosofale', 'NARRATIVA', 1, 'SALANI EDITORE', 'Harry Potter e la Pietra Filosofale della scrittrice inglese Joanne Rowling esce nel 1997 ed è il primo episodio della saga di Harry Potter. In questo libro il giovane Harry, dopo aver scoperto di essere un mago, vive le sue prime avventure nella scuola di magia di Hogwarts. Il romanzo ha ottenuto un grande successo, consacrando la saga di Harry Potter come la serie di romanzi fantasy più popolare degli ultimi decenni.     ', 'assets/thumbnails/9788893817028.png', 13),
        (2, 2, '978-88-9381-704-2', 'Harry Potter e il prigioniero di azkaban', 'Narrativa', 1, 'Salani editore ', '"Harry Potter e il prigioniero di Azkaban" vede Harry tornare a Hogwarts per il terzo anno. Affronta il fuggitivo Sirius Black mentre scopre segreti oscuri legati al suo passato.', 'assets/thumbnails/978-88-9381-704-2.png', 14),
        (5, 5, 'privo02', 'Il Mulino Di Po Volume 2', 'Romanzo', 1, 'Arnoldo Mondatori', 'Romanzo Storico', 'assets/thumbnails/privo02.png', 15),
        (2, 2, '9788893817073', 'Harry Potter e il principe mezzosangue', 'NARRATIVA', 1, 'SALANI EDITORE', 'Il sesto anno della saga di Harry Potter inizia con le dimissioni del Ministro della Magia, Cornelius Caramell, che non aveva creduto al ritorno di Voldemort. Caramell viene sostituito dall''ex capo degli Auror, Rufus Scrimgeour. Nel frattempo Severus Piton riceve la visita di Narcissa Malfoy, madre di Draco, accompagnata dalla sorella Bellatrix. Narcissa chiede a Piton di proteggere e aiutare il figlio Draco, che è stato incaricato da Voldemort di uccidere Silente. Piton stringe con Narcissa il Voto Infrangibile, promettendo che aiuterà Draco in questa missione. Silente va a prendere Harry Potter a casa degli zii, per portarlo dai Weasley, ma prima gli chiede di accompagnarlo in una missione: deve convincere il Professore Lumacorno ad accettare l''incarico di insegnante di pozioni.', 'assets/thumbnails/9788893817073.png', 16),
        (2, 2, '978-88-9381-708-0', 'Harry Potter e i doni della morte', 'Narrativa', 1, 'Salani editore ', '"Harry Potter e i Doni della Morte" è il culmine epico della serie, dove Harry, Ron e Hermione affrontano il loro destino, cercando gli Horcrux di Voldemort per sconfiggerlo definitivamente. Con azione avvincente e momenti toccanti, questa conclusione emozionante tiene i lettori incollati fino all''ultima pagina.', 'assets/thumbnails/978-88-9381-708-0.png', 17),
        (6, 6, '881801627X', 'La linea d''ombra', 'Narrativa', 1, 'Rusconi libri', 'Il romanzo narra la storia di un giovane, chiamato a comandare una nave perché il suo capitano è morto. Egli deve condurre la nave in un porto dell''oceano Indiano ma la traversata nasconderà molte insidie e pericoli . Il viaggio diventa l''allegoria del percorso interiore del giovane capitano : tutte le sue insicurezze , i sensi di colpa e paure vengono superate con il coraggio e la volontà di non arrendersi alla propria morte e a quella degli altri.', 'assets/thumbnails/881801627X.png', 18),
        (2, 8, '9788868364649', 'IT', 'NARRATIVA', 1, 'PICKWICK', 'Il romanzo è la storia di sette amici provenienti dalla fittizia città di Derry, Maine, ed è raccontata alternando due diversi periodi temporali. Dal libro sono stati tratti un''omonima miniserie televisiva nel 1990 e una trasposizione cinematografica divisa in due parti: It (2017) e It - Capitolo due (2019).', 'assets/thumbnails/9788868364649.png', 19),
        (5, 9, 'privo03', 'Regina Dell''Aria e Della Notte', 'Romanzo', 1, 'G.C Sansoni', 'Romanzo Breve', 'assets/thumbnails/privo03.png', 20),
        (2, 10, '9788804586074', 'Le Cronache di Narnia', 'NARRATIVA', 1, 'MONDADORI', 'Le storie delle Cronache di Narnia cominciano proprio da una serie di immagini nella testa del loro autore.

“All’inizio non c’era nessun racconto” scrisse Lewis alcuni anni dopo “solo delle forme”.

Il primo libro della serie, Il leone, la strega e l’armadio, nacque dal “quadro mentale” di un bosco innevato attraverso il quale trotterella frettolosamente un piccolo fauno dalle zampe caprine, che regge un ombrello con una mano e una pila di pacchetti con l’altra.

Il fauno immaginato da Lewis è Mr. Tumnus, la guida di Lucy Pevensie a Narnia, terra incantata di animali parlanti ed eroiche battaglie.', 'assets/thumbnails/9788804586074.png', 21),
        (5, 11, 'privo04', 'Mezzo Miliardo', 'Romanzo', 1, 'Bietti', 'Romanzo', 'assets/thumbnails/privo04.png', 22),
        (6, 12, '9788804668046', 'Il deserto dei Tartari', 'Narrativa', 1, 'Mondadori', 'Giovanni Drogo, un sottotenente, viene mandato in una lontana fortezza. A nord della fortezza c''è il deserto da cui si attende un''invasione dei tartari. Ma l''invasione, sempre annunciata, non avviene e l''addestramento, i turni di guardia, l''organizzazione militare, appaiono cerimoniali senza senso. Quando Drogo torna in città per una promozione, si accorge di aver perso ogni contatto con il mondo e che ormai la sua unica ragione di vita è l''inutile attesa del nemico. Tornato alla fortezza, si ammala e proprio allora accade l''evento tanto aspettato: i tartari avanzano dal deserto. Nell''emozione e nella confusione del momento, senza che lui possa prendere parte ai preparativi di difesa, Drogo muore, dimenticato da tutti.', 'assets/thumbnails/9788804668046.png', 23),
        (5, 13, '9788864110776', 'Caos A Bruges', 'Romanzo', 1, 'Fazi', 'Romanzo', 'assets/thumbnails/9788864110776.png', 24),
        (6, 14, '9788854172623', 'Jane Eyre', 'Narrativa', 1, 'Newton Compton Editori', 'ane Eyre è una bambina orfana che viene accolta presso i parenti dopo la morte dei genitori. In questa sua nuova famiglia Jane è resa oggetto di continui maltrattamenti da parte di una fredda zia e anche da parte degli altri bambini della casa, suoi cugini.', 'assets/thumbnails/9788854172623.png', 25),
        (34, 1, 'VALE1', 'VALE', 'VALE', 76, 'VALE', 'VALE', 'assets/thumbnails/VALE1.png', 26),
        (2, 33, '9788822711717', 'Il libro dell''inquietudine', 'Romanzo', 1, 'NEWTON COMPTON EDITORI', 'Il Libro dell''inquietudine (in portoghese, Livro do Desassossego) è una delle maggiori opere dello scrittore portoghese Fernando Pessoa. Si tratta di un''opera postuma e incompiuta, oggi costituita da un''ibrida e innumerevole quantità di pagine scritte, «frammenti, tutto frammenti», come rivela Pessoa in una lettera.', 'assets/thumbnails/9788822711717.png', 27),
        (35, 34, 'privo', 'Il velocifero', 'Narrativa', 1, 'Oscar Mondadori', 'Il "velocifero", la diligenza dei viaggi celeri del secolo scorso, fa da simbolo per la saga di una grossa e pittoresca famiglia, uomini e bestie, galleggiante sulla Milano della Belle époque.', 'assets/thumbnails/privo.png', 28),
        (36, 35, '9788894308143', 'VOCI', 'NARRATIVA', 1, 'EMIA', 'Che cosa succede se il lavoro te lo strappano via? Quali gli improvvisi cambiamenti che sei costretto ad affrontare nella vita? Diciassette racconti brevi ci fanno conoscere e amare persone a cui è stata sottratta la dignità di avere un lavoro o che stanno combattendo per mantenerne uno. Una visione di reale quotidianità che spinge il lettore in un vortice di forti emozioni e di grandi interrogativi su uno dei problemi più urgenti dei nostri giorni. Una lettura che lascia un monito per chi, operando freddamente in ossequio alle sole leggi dei numeri, non vuole rendersi conto delle possibili umane conseguenze e ci costringe a guardare con occhi diversi chi ne diviene, suo malgrado, vittima. 118 pp.', 'assets/thumbnails/9788894308143.png', 29),
        (2, 36, '9788806221300', 'LA CASA IN COLLINA', 'Romanzo', 1, 'Giulio Einaudi editore', 'Cesare Pavese pubblica il romanzo La casa in collina nel 1949 insieme con Il carcere nel volume unico Prima che il gallo canti. Se Il carcere risale al periodo tra il 1938 e il 1939 e rievoca l’esperienza del confino dell’autore a Brancaleone Calabro tra il 1935 e il 1936, La casa in collina indaga le conseguenze psicologiche e sociali del secondo conflitto mondiale e della Resistenza, cui Pavese stesso non partecipa, rifugiandosi, come il protagonista, in campagna. In entrambe le opere la narrazione è dunque fortemente intrisa di elementi autobiografici, che fanno trasparire alcune costanti della poetica di Pavese: il legame disarmonico tra l’intellettuale e la realtà, il rapporto complesso con il mondo rurale delle Langhe contrapposto a quello della città, il ruolo della memoria individuale.', 'assets/thumbnails/9788806221300.png', 30),
        (2, 37, '9788894602609', 'Albert Camus la peste', 'Narrativo', 2, 'Salone internazionale del libro Torino', 'La peste è un romanzo dello scrittore francese Albert Camus del 1947. Appena pubblicata, l''opera, che rientra nella produzione di Camus definita "Ciclo della rivolta", riscosse grande successo vendendo oltre 160 000 copie nei primi due anni; ottenne tra l''altro il Prix des Critiques.', 'assets/thumbnails/9788894602609.png', 31),
        (2, 38, 'privo 09', 'I Cosacchi', 'Romanzo', 1, 'Arnoldo Mondadori', 'Libro di romanzi', 'assets/thumbnails/privo 09.png', 32),
        (35, 39, '8804370084', 'Caino Il buono', 'Narrativa', 1, 'Arnoldo Mondadori Editore', 'Caino il buono è un libro importante, perché affronta il tema relativamente inedito dei sentimenti maschili, e del rapporto fraterno come garanzia di continuità e di solidarietà. Molti lettori vi potranno trovare una chiave d’interpretazione, se non di soluzione, dei propri conflitti familiari.
Ma è anche un libro che si legge con passione. E ci ricorda ancora una volta che la psicologia è una delle vie regie che portano al Romanzo.', 'assets/thumbnails/8804370084.png', 33),
        (2, 40, 'privo 10', 'I Quattro Libri di Lettura', 'Romanzo', 1, 'Nuova Italia', 'L''opera è il rifacimento di un''antologia pedagogica precedente, il Sillabario (o Abbecedario). Comprendente alcune favole di Esopo in versione libera, il rifacimento di leggende russe o indiane, racconti dei fratelli Grimm e storie vere, il testo veniva utilizzato per un apprendimento critico e attivo.[1] Contiene in 4 volumi rispettivamente 58, 65, 51 e 35 tra favole, storie e poesie.

L''opera era destinata, come disse Tolstoj, «a tutti i fanciulli, da quelli della famiglia imperiale a quelli dei contadini, perché ne traggano le loro prime impressioni poetiche»[2].', 'assets/thumbnails/privo 10.png', 34),
        (37, 41, '1', 'IL QUARTIERE', 'NARRATIVA', 1, 'ARNOLDO MONDADORI EDITORE', 'Ambientato nel periodo che va dal 1932 al 1939, il romanzo narra delle peripezie amorose di un gruppo di ragazzi appartenenti ad un quartiere popolare di Firenze e più precisamente quello di Santa Croce, colti nel passaggio dall''adolescenza alla prima giovinezza: in pratica si coglie lo sviluppo della loro educazione sentimentale e la formazione di una coscienza politica.

Il romanzo è sostenuto da un intreccio continuo di vicende personali ed affettive nelle quali si muovono i vari personaggi, senza che qualcuno emerga o si riconosca particolarmente, neppure nella figura di Valerio, la voce narrante che si identifica con l''autore (questo tipo di romanzo è detto "corale"). Per cui, all''inizio dell''opera, ci viene immediatamente focalizzata questa sensazione dalla frase “Eravamo creature comuni. Ci bastava un gesto per sollevarci collera o amore”.

', 'assets/thumbnails/1.png', 35),
        (2, 42, '9788861752535', 'Lo strano caso del Dr Jekyll e Mr Hyde', 'Narrativa', 1, 'JoyBooK', 'Lo strano caso del dottor Jekyll e del signor Hyde è un racconto gotico dello scrittore Robert Louis Stevenson. Tratta la storia di un avvocato londinese, Gabriel John Utterson, il quale investiga i singolari episodi tra il suo vecchio amico, il dottor Jekyll, e il malvagio signor Hyde.', 'assets/thumbnails/9788861752535.png', 36),
        (2, 44, '9788806219352', 'Primo Levi: Se Questo é Un Uomo', 'Romanzo', 1, 'Einaudi', 'Se questo è un uomo è un''opera memorialistica di Primo Levi scritta tra il dicembre 1945 e il gennaio 1947. Rappresenta la coinvolgente ma meditata testimonianza di quanto vissuto dall''autore nel campo di concentramento di Auschwitz', 'assets/thumbnails/9788806219352.png', 37);
EstraiDatiStazioniTOS.py: Procedura per creare file csv con coordinate GB delle stazioni del Servizio Idrografico Regionale (codice TOS) con cumulata dei valori di precipitazione validi o prevalidati disponibili e non nullo per un periodo arbitrario definito
dall'utente partendo dai file di Output delle precipitazioni giornaliere disponibili
alla pagina web http://www.sir.toscana.it/ricerca-dati.

Campi file output 'sum' della procedura EstraiDatiStazioniTOS.py

codice (COD);
nome stazione (stazione);
comune (comune);
coordinate gb (X_GB; Y_GB);
primo giorno dell'intervallo indicatoi dall'utente (start_day);
ultimo giorno dell'intervallo indicatoi dall'utente (end_day);
giorni totali intervallo start_day - end_day (tot_days);
giorni totali con dati misurati validati o prevalidati e non nulli(mis_days);
sommatoria dei dati di pioggia dei giorni validati, prevalidati o non nulli (cumul)

EstraiDatiStazioniTOS_Stat.py: come sopra ma con campi aggiuntivi con statistiche di base per l'intervallo dato.

Campi file output 'stat' della procedura EstraiDatiStazioniTOS_stat.py

codice (COD);
nome stazione (stazione);
comune (comune);
coordinate gb (X_GB; Y_GB);
primo giorno dell'intervallo indicatoi dall'utente (start_day);
ultimo giorno dell'intervallo indicatoi dall'utente (end_day);
giorni totali intervallo start_day - end_day (tot_days);
giorni totali con dati misurati validati o prevalidati e non nulli(mis_days);
giorni totali senza pioggia (<= a soglia definita dall'utente) presenti in mis_days (norain_days); 
giorni totali di pioggia (> a soglia definita dall'utente) presenti in mis_days (rain_days); 
sommatoria dei dati di pioggia dei giorni validati, prevalidati o non nulli (cumul);
valore massimo di pioggia giornaliera nell'intervallo start_day - end_day (max)
valore minimo di pioggia giornaliera nell'intervallo start_day - end_day (min)
valore medio nell'intervallo mis_days (media)


In entrambii casi per le statistiche sulle singole stazioni viene creato anche un file 'master' unico con tutti i dati giornalieri di tutte le stazioni con dati validati prevalidati e non nulli presenti nell'intervallo di tempo dato. 

Nei file TOS sono presenti dei refusi con attributo "validato" e valore di precipitazione nullo, questi sono scartati automaticamente.

BatchDownloadStazioniTOS.py: procedura per scaricare automaticamente tutti i dati disponibili nell'elenco 'list_file.txt'

CreaShapeStazioniTOS_Vita.py: procedura per creare file di tutte le stazioni con dati validi, prevalidati e non nulli per cui è disponibile un file TOS. Gli attributi riportano: 

codice (COD);
nome stazione (stazione);
comune (comune);
coordinate gb (X_GB; Y_GB);
primo giorno di registrazione dati prevalidati o validati (start_day);
ultimo giorno di registrazione dati validati o prevalidati (end_day);
giorni totali intervallo start_day - end_day (tot_days);
giorni totali con dati misurati validati o prevalidati e non nulli(mis_days);
giorni totali con dati misurati validati e non nulli (val);
giorni totali con dati misurati prevalidati e non nulli(preval).

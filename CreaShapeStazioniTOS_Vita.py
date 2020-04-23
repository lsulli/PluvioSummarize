import os
import datetime

# Procedura per creare file csv con coordinate GB delle stazioni del Servizio Idrografico Regionale (codice TOS)
# partendo dai file di Output disponibili alla pagina
# web http://www.appenninosettentrionale.it/dati/lista_stazioni_sir_meno.php.
# o alla pagina web http://www.sir.toscana.it/ricerca-dati
# Dati estratti:
# codice (COD)
# nome stazione (stazione)
# comune (comune)
# coordinate gb (X_GB; Y_GB)
# primo giorno di registrazione dati prevalidati o validati (start_day),
# ultimo giorno di registrazione dati validati o prevalidati (end_day),
# giorni totali intervallo start_day - end_day (tot_days),
# giorni totali con dati misurati validati o prevalidati (mis_days),
# giorni totali con dati misurati validati (val),
# giorni totali con dati misurati prevalidati (preval).
# ----------------------------------------------------------------------------------------
# traccio il tempo di elaborazione
t1 = datetime.datetime.now()

# Variabile che indica la directory in cui sono archiviati i file .csv dei dati giornalieri delle stazioni
# SIR con codice TOS per scaricare in batch i file aggiornati dalla pagina web utilizzare lo script
# python BatchDownload.py
# ATTENZIONE: usate sempre \\ come separatore di directory!!

file_dir = 'C:\\2_LSulli\\15_Pluviometria\\Origine'

# crea una lista con tutti i file nella directory
lis = os.listdir(file_dir)

# variabili che indicano i file di output da creare:

# file ascii con le coordinate delle stazioni
xy_file = 'C:\\2_LSulli\\15_Pluviometria\\Origine\\xy_output.csv'

# Inizializzo le varibili e assegno le costanti
d = ''
cod = 'nd'
stazione = 'nd'
comune = 'nd'
w3 = open(xy_file, 'a+')
#scrivo l'intestazione con il nome dei campi
w3.write('COD; stazione; comune; X_GB; Y_GB; start_day; end_day; tot_days; mis_days; val; preval' + '\n')

# loop nei file di input per recuperare i dati dei file di output
for line1 in lis:
    try:
        # inizializzo ad ogni loop il contatore delle stringhe valide
        ct = 0
        val = 0
        preval = 0
        # apro e leggo i file che sono presenti nella directory di input
        f_dir = file_dir + '\\' + line1
        # open files in read mode
        in_file = open(f_dir, 'r+')

        # le righe di ogni file sono assegnate ad una variabile
        d = in_file.readlines()
        # recupero i dati della stazione sapendo che occupano sempre
        # il solito posto e conosco le stringhe di riferimento
        try:  # Il codice ha lunghezza e posizione fissa
            cod = d[1][10:21]
        except:
            pass
        try:  # il nome della stazione deve essere depurato dalle virgolette e ha lunghezza variabile quindi faccio
            # riferimento alla posizione di inizio e al carattere prima dell'ultima virgoletta

            stazione = d[0][12:(d[0].find('"', 12))]
        except:
            pass
        try:   # il nome del comune deve essere depurato dalle virgolette e ha lunghezza variabile quindi faccio
            # riferimento alla posizione di inizio e al carattere prima dell'ultima virgoletta
            comune = d[2][10:(d[2].find('"', 10))]
        except:
            pass
        try:  # le coordinate hanno lunghezza e posizione fissa
            x_gb = d[4][13:20]
            y_gb = d[4][25:32]
        except:
            pass
        # eseguo un ciclo completo dall'inzio dei dati registrati per trovare la prima data con valori validi o prevalidati
        # appena trovo la prima data utile esco dal ciclo
        try:
            for line2 in d[19:]:
                if (line2[-2:-1] == 'V' or line2[-2:-1] == 'P')and len(line2[11:(line2.find(';', 11))])> 0:
                    start_day = datetime.datetime.strptime(line2[:10], '%d/%m/%Y')
                    start_day_str = line2[:10]
                    break
            print (cod, 'primo giorno con dati validi:', start_day_str)
        except:
            pass
        # eseguo un ciclo completo dalla fine dei dati registrati per trovare l'ultima data con valori validi o prevalidati
        # appena trovo la prima data utile esco dal ciclo
        try:
            for line2 in d[::-1]:
                if (line2[-2:-1] == 'V' or line2[-2:-1] == 'P') and len(line2[11:(line2.find(';', 11))])> 0:
                    end_day = datetime.datetime.strptime(line2[:10], '%d/%m/%Y')
                    end_day_str = line2[:10]
                    break
            print (cod, ' ultimo giorno con dati validi:', end_day_str)
        except:
            pass
        # calcolo la differenza in giorni tra prima e ultima data valida. Tengo conto che
        # trattandosi di una differenza tra date l'intervallo in giorni ha un giorno in più

        tot_days = (end_day - start_day)
        tot_days_str = str(tot_days.days + 1)

        # conteggio il record con dati validati o prevalidati per registrarlo e confrontarlo
        # con i giorni dell'intervallo esaminato
        try:
            for line2 in d[19:]:
                #print (d[19:])
                if datetime.datetime.strptime(line2[:10], '%d/%m/%Y') >= start_day \
                        and datetime.datetime.strptime(line2[:10], '%d/%m/%Y') <= end_day \
                        and (line2[-2:-1] == 'V') and len(line2[11:(line2.find(';', 11))])> 0:
                    val = val + 1
                if datetime.datetime.strptime(line2[:10], '%d/%m/%Y') >= start_day \
                        and datetime.datetime.strptime(line2[:10], '%d/%m/%Y') <= end_day \
                        and (line2[-2:-1] == 'P')and len(line2[11:(line2.find(';', 11))])> 0:
                    preval = preval + 1
        except:
            pass
        ct = val+preval

        # scrivo nel file sum.csv solo se sono stati trovati valori validi o prevalidati
        if ct > 0:
            w3.write(cod + ';' + stazione + ';' + comune +';' + x_gb + ';' + y_gb + ';' + start_day_str + ';' + end_day_str + ';'
                     + str(tot_days.days) + ';' + str(ct) + ';' + str(val) + ';' + str(preval) + ';' +'\n')

        # comunico alla shell che elaborazione è stata eseguita e informo quanti giorni hanno dati validi o prevalidati
        print('stazione: ', cod, ' elaborata. Presenti dati validi o prevalidati per ', ct, ' giorni su un intervallo di ',
              tot_days_str)
    except:
        print('******* ATTENZIONE stazione ', cod, 'non è stata processata per problemi nel file di input')

w3.close()
t2 = datetime.datetime.now()
print (t2 - t1)

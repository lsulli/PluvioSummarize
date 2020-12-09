import os
import datetime
import statistics

# Procedura per creare file csv con coordinate GB delle stazioni del Servizio Idrografico Regionale (codice TOS)
# con cumulata dei valori di precipitazione validi o prevalidati e not null disponibili per un periodo arbitrario definito
# dall'utente partendo dai file di Output delle precipitazioni giornaliere disponibili
# alla pagina web http://www.sir.toscana.it/ricerca-dati

# ----------------------------------------------------------------------------------------

# Variabile che indica la directory in cui sono archiviati i file .csv dei dati giornalieri delle stazioni
# SIR con codice TOS per scaricare in batch i file aggiornati dalla pagina web utilizzare lo script
# python BatchDownload.py
# ATTENZIONE: usate sempre \\ come separatore di directory!!

file_dir = '.\\Temp'

# Directory di destinazione dei file di Output:

output_dir = '.'

# crea una lista con tutti i file nella directory
lis = os.listdir(file_dir)

# Inizializzo le varibili e assegno le costanti
d = ''
name = 'nd'
comune = 'nd'
zero_aprox_value = 0 #valore di pioggia assunto come limite di giorno con pioggia

# per default l'output dei valori di precipitazione ha come separatore di decimali il punto

my_comma = 0 # = 1 per impostare la virgola come separatore di decimale

# data inizio periodo - stringa: cambiare a piacimento rispettando il formato dd/mm/aaaa!
start_string = '01/12/2020'
startstr = start_string.replace('/', '')# stringa da inserire nel nome del file di output
# data fine periodo - stringa: cambiare a piacimento rispettando il formato
end_string = '05/12/2020'
endstr = end_string.replace('/', '')# stringa da inserire nel nome del file di output

# variabili che indicano i file di output da creare:

# file master con tutti i dati giornalieri per ogni stazione per l'intervallo dato. Nome file 'parlante'
out_file = output_dir + '\\master_' + startstr + '_' + endstr + '.csv'

# file raggruppato per stazione con coordinate GB e valore della cumulata  per l'intervallo dato.
# Direttamente leggibile dal GIS. Ricordatevi che i valori di precipitazione vengono letti di default come stringa!
out_sum = output_dir + '\\stat_' + startstr + '_' + endstr + '.csv'

# conversione da stringa a formato data
start = datetime.datetime.strptime(start_string, '%d/%m/%Y')
end = datetime.datetime.strptime(end_string, '%d/%m/%Y')
# calcolo dei giorni nell'intervallo richiesto: attenzione l'intervallo è dato dal primo all'ultimo giorno compresi, non è una sottrazione matematica. 
tot_days = end - start

# si creano i file e si scrive i nomi di colonna
w = open(out_file, 'a+')
w.write('cod; date; pluvio; validaz' + '\n')

w2 = open(out_sum, 'a+')
w2.write('cod; Stazione;  X_GB; Y_GB; start_day; end_day; tot_days; mis_days; norain_days; rain_days; sum; max; min; mean; median; stdev' + '\n')

# loop nei file di input per recuperare i dati dei file di output
for line1 in lis:
    try:
        # inizializzo ad ogni loop l'insieme dei dati pluviometrici e il contatore delle stringhe valide
        list_cumulata = []
        count_validvalue = 0
        count_zerovalue = 0
        # apro e leggo i file che sono presenti nella directory di input
        f_dir = file_dir + '\\' + line1
        # open files in read mode
        in_file = open(f_dir, 'r+')

        # le righe di ogni file sono assegnate ad una variabile
        d = in_file.readlines()
        # recupero il valore del codice della stazione e delle coordinate sapendo che occupa sempre
        # il solito posto ed è sempre lungo uguale
        try:  # provo e salto la riga se vi sono errori
            cod = d[1][10:21]
        except:
            pass
        try: # provo e salto la riga se vi sono errori
            name = d[0][12:(d[0].find('"', 12))]
        except:
           pass
        try:  # provo e salto la riga se vi sono errori
            x_gb = d[4][13:20]
            y_gb = d[4][25:32]
        except:
            pass
        # a partire dalla prima linea dei valori registrati verifico la data e se i dati sono validati o meno
        for line2 in d[19:]:
            # recupero il valore di precipitazione come stringa 
            my_p_str_value = (line2[11:(line2.find(';', 11))])
            try:
                # impongo i criteri di selezione dell'intervallo voluto e dei dati validi, prevalidati e not null (stringa non vuota)
                if datetime.datetime.strptime(line2[:10], '%d/%m/%Y') >= start \
                        and datetime.datetime.strptime(line2[:10], '%d/%m/%Y') <= end \
                        and (line2[-2:-1] == 'V' or line2[-2:-1] == 'P') and len(my_p_str_value)>0:
                    # conteggio il record con dati validati o prevalidati e not null per registrarlo e confrontarlo
                    # con i giorni dell'intervallo esaminato
                    count_validvalue = count_validvalue + 1
                    # scrivo tutta la linea nel file master.csv
                    my_line = line2.replace(',','.')
                    w.write(cod + ';' + my_line)
                    # recupero il valore di precipitazione come stringa
                    # riga da eliminare ?: my_p_str_value = (line2[11:(line2.find(';', 11))])
                    # converto my_p_str_value in floating per la successiva sommatoria rispettando la convenzione di python per i decimali
                    my_p_float_value = float(my_p_str_value.replace(',', '.'))
                    # aggiungo il valore nella lista
                    list_cumulata.append(my_p_float_value)
                    if my_p_float_value <= zero_aprox_value:
                        count_zerovalue=count_zerovalue+1
            except:
                pass
        # sommo i valori di precipitazione giornaliera registrati nella lista e converto il valore in stringa
        # e quindi applico il separatore di decimale come virgola
        list_cumulata.sort()
        my_sum = str(round(sum(list_cumulata), 1))
        my_max = str(round(max(list_cumulata), 1))
        my_min = str(round(min(list_cumulata), 1))
        my_mean = str(round((statistics.mean(list_cumulata)), 1))
        my_median = str(round((statistics.median(list_cumulata)), 1))
        my_stdev = str(round((statistics.stdev(list_cumulata)), 1))
        print ('media:', my_mean)
        if my_comma == 1:
            my_sum_str_comma = my_sum.replace('.', ',')
            my_max_str_comma = my_max.replace('.', ',')
            my_min_str_comma = my_min.replace('.', ',')
            my_mean_str_comma = my_mean.replace('.', ',')
            my_median_str_comma = my_median.replace('.', ',')
            my_stdev_str_comma = my_stdev.replace('.', ',')
        elif my_comma== 0:
            my_sum_str_comma = my_sum
            my_max_str_comma = my_max
            my_min_str_comma = my_min
            my_mean_str_comma = my_mean
            my_median_str_comma = my_median
            my_stdev_str_comma = my_stdev
        # scrivo nel file sum.csv solo se sono stati trovati valori validi o prevalidati e not null
        if count_validvalue > 0:
            w2.write(cod + ';' + name + ';'+ x_gb + ';' + y_gb + ';' + start_string + ';' + end_string + ';' + str((tot_days.days) + 1)
            + ';' + str(count_validvalue) + ';' + str(count_zerovalue) + ';' + str(count_validvalue-count_zerovalue) + ';' + my_sum_str_comma 
            + ';' + my_max_str_comma + ';' + my_min_str_comma + ';' + my_mean_str_comma + ';' + my_median_str_comma + ';' + my_stdev_str_comma +'\n')

        # comunico alla shell che elaborazione è stata eseguita e informo quanti giorni hanno dati validi o prevalidati
        print('stazione: ', cod, ' elaborata. Presenti dati validi o prevalidati per ', count_validvalue, ' giorni su un intervallo di ',
               str((tot_days.days) + 1))
    except:
        pass
w.close()
w2.close()

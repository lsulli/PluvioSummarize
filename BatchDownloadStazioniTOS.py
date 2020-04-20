#need to install requests module. With pip in prompt dos write: 'pip install requests' 

import requests

root_url = 'http://www.sir.toscana.it/archivio/download.php?IDST=pluvio&IDS='

#Elenco dei file da scaricare.
#il file list_file.txt deve risiedere nella stessa directory e avere un semplice elenco 
#dei nomi delle stazioni senza alcuna estensione (l'estensione '.csv' viene gestita in seguito)
#esempio:
#TOS10000710
#TOS11000114
#TOS11000115
#TOS07000001


in_file = open('list_file.txt', 'r+')

d = in_file.readlines()# insieme delle righe nel file
len(d)#conta il numero di stazioni nel file (pari al numero di righe)

counter = 0

#i file verranno scaricati nella directory corrente
for file_url in d:
	counter = counter+1
	print('file n.', counter, ' di ', len(d))
	try:
		r = requests.get(root_url+file_url[:-1], stream = True)

		with open(file_url[-12:-1]+'.csv',"wb") as csv:
			for chunk in r.iter_content(chunk_size=1024):
				# writing one chunk at a time to pdf file
				if chunk:
					csv.write(chunk)

		print('file della stazione ', file_url[:-1], ' copiato')
		csv.close()

	except:
		print('Errore in fase di copiatura per il file', file_url[:-1], ' passo al successivo ' )
		pass
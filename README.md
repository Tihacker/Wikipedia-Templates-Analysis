# Wikipedia-Templates-Analysis
Questo codice è frutto del progetto di tesi Wikipedia Templates Analysis, sviluppato da Mattia Lago sotto la supervisione del prof. Alberto Montresor e il dott. Cristian Consonni.

Il codice ha bisogno di un refactoring.

In ogni caso ogni script utilizza docopt per la lettura da console, quindi utilizzando la flag '-h' è possibile ottenere una lista di tutte le opzioni possibili per ogni script.

La versione di Python utilizzata è la 3, non è stata testata quindi nessuna compatibilità con Python 2.

Librerie necessarie per il corretto funzionamento:
- Mediawiki Utilities
- docopt
- Matplotlib

Ordine di esecuzione:

| Ordine | Nome File | Input | Output |
|:-------------:|:-------------:|:-------------:|:-------------:|
| 1 | analizedump.py | .bz2 dump | output.csv |
| 2 | redirect.py | .bz2 dump | redirect.csv |
| 3 | post-processing.py | output.csv | output-post.csv |
| 3.1 | rimuovicommenti.py | output-post.csv | output-nocomment.csv |
| 3.2 | aggiungiredirect.py (facoltativo) | output-nocomment.csv, redirect.csv | output-redirects.csv |
| 4.1 | graficop1.py | output-nocomment.csv | alldict.csv [tmp file] |
| 4.2 | graficop2.py | alldict.csv | .csv coordinate files |
| 5 | stampagraficisingle.py | .csv coordinate file | graph's .png |
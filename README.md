# Requestarr

Progetto finale del corso di Tecnologie Web, anno di corso 2023/2024, studente Lorenzo Taccini.

## Estratto

Il progetto ha lo scopo di realizzare un servizio di **media request and discovery** per un utilizzo *in-house*, ad esempio nel deploy di un home server.

Creato sulla falsa riga di servizi più blasonati come [Overseerr](https://overseerr.dev/), per facilitare la fruizione di contenuti multimediali, in particolare per il **processo di richiesta di nuovi contenuti**.

## Features Principali

- Visualizzazione di un **catalogo di film aggiornato e aggiornabile**, con dettagli su ogni titolo, ottenuti direttamente da [TMDB](https://www.themoviedb.org/)
- **Richiesta di titoli** ai moderatori da parte di utenti registrati
- **Dashboard personale** per la personalizzazione del profilo utente
- **Watchlist** privata per-user
- Dashboard per visualizzare lo **stato** delle proprie richieste
- **Recommendation System** basato su generi simili: Un titolo ti interessa? Scopri istantaneamente gli altri titoli più affini!
- **Strumento di ricerca flessibile**: trova i tuoi titoli preferiti nel catalogo senza preoccuparti di commettere qualche errore di ortografia!


## Installazione e start-up

Assicurati di lavorare in un ambiente con pipenv configurato.

Installa i requisiti contenuti nel file `requirements.txt` lanciando (dalla ROOT di progetto):
``` shell
pip install -r requirements.txt
```

Popola poi il catalogo di titoli con lo script `TMDB_scraper.py` contenuto nella diretory `utils`:
```shell
python -m utils.TMDB_scraper
```
Lo script, attraverso le API di TMDB popola il database con film randomici ottenuti dalla piattaforma.

Se necessario, si può creare un `superuser` con:
```shell
python manage.py createsuperuser
```
e inserendo le proprie informazioni.

Ora puoi **avviare il server** in modalità *development* con:
```shell
python manage.py runserver
```

## Testing 

Per utilizzare le funzionalità di **unit testing** basta eseguire, dalla ROOT:
```shell
python manage.py test movieapp.tests
```
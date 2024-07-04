import requests
import random
import json

API_KEY = '5dbf33ab1210565bba9d880c176bf3d8'


def get_random_movies(num_movies=20):
    base_url = 'https://api.themoviedb.org/3'
    endpoint = '/discover/movie'
    params = {
        'api_key': API_KEY,
        'sort_by': 'popularity.desc',
        'include_adult': 'false',
        'include_video': 'false',
        'page': 1,
    }

    # Effettua la richiesta GET all'API di TMDB
    response = requests.get(base_url + endpoint, params=params)
    if response.status_code == 200:
        movies = response.json()['results']
        # Estrai casualmente 'num_movies' film
        random_movies = random.sample(movies, num_movies)
        return random_movies
    else:
        print(f"Errore nella richiesta API: {response.status_code}")
        return None


def extract_movie_info(movie):
    # Estrai le informazioni desiderate
    movie_info = {
        'model': 'movieapp.movie',  # Specifica il modello di Django
        'pk': movie['id'],  # PK come l'ID di TMDB
        'fields': {
            'title': movie['title'],
            'year': movie['release_date'][:4],  # Estrapola solo l'anno dalla data di uscita
            'tmdb_id': movie['id'],
            'description': movie['overview'],
            'genre': [],  # Inizializza una lista vuota per i nomi dei generi
        }
    }

    base_url = 'https://api.themoviedb.org/3'
    endpoint = '/genre/movie/list'
    params = {
        'api_key': API_KEY,
        'language': 'en-US',  # Specifica la lingua dei generi
    }

    # Effettua la richiesta GET all'API di TMDB per ottenere i nomi dei generi
    response = requests.get(base_url + endpoint, params=params)
    if response.status_code == 200:
        genre_dict = {genre['id']: genre['name'] for genre in response.json()['genres']}
        movie_info['fields']['genre'] = [genre_dict[genre_id] for genre_id in movie['genre_ids']]
        movie_info['fields']['genre'] = json.dumps(movie_info['fields']['genre'])
    else:
        print(f"Errore nella richiesta API per ottenere i generi: {response.status_code}")

    return movie_info


def create_json_file(movies):
    movies_info = []
    for movie in movies:
        movie_info = extract_movie_info(movie)
        movies_info.append(movie_info)

    # Scrivi le informazioni nel file JSON
    with open('../movieapp/fixtures/random_movies.json', 'w', encoding='utf-8') as f:
        json.dump(movies_info, f, ensure_ascii=False, indent=4)

    print("File JSON 'random_movies.json' creato con successo.")


if __name__ == "__main__":
    random_movies = get_random_movies(num_movies=20)
    print(random_movies)
    '''if random_movies:
        create_json_file(random_movies)'''

import json

import requests


def get_movie_details(movie_id, api_key) -> dict | None:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        'api_key': api_key,
        'language': 'en-US'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        movie_data = response.json()
        title = movie_data.get('title')
        year = movie_data.get('release_date', '')[:4]  # Ottiene l'anno dalla data di rilascio
        description = movie_data.get('overview')
        genre_dict = {genre['id']: genre['name'] for genre in movie_data['genres']}
        genre_list = json.dumps(list(genre_dict.values()))
        return {
            'title': title,
            'year': year,
            'description': description,
            'genre': genre_list
        }
    else:
        print(f"Errore nella richiesta: {response.status_code}")
        return None

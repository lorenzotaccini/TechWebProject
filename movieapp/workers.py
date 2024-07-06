import difflib

from movieapp.models import Movie


def title_recommendation(movie: Movie):
    def count_common_genres(list1, list2):
        return len(set(list1) & set(list2))

    genres = movie.get_genre_as_list()
    allmovies_genre_list = [(m, m.get_genre_as_list()) for m in
                            Movie.objects.all().exclude(tmdb_id=movie.tmdb_id)]

    common_genres_list = [[elem[0], count_common_genres(genres, elem[1])] for elem in allmovies_genre_list]
    common_genres_list = sorted(common_genres_list, key=lambda x: x[1], reverse=True)

    recommended_titles = [elem[0] for elem in common_genres_list if elem[1]][:5]

    if len(recommended_titles) > 0:
        return recommended_titles
    else:
        return None


def find_similar_movies(movie_titles: list, query):
    tolerance = 0.6
    similar_movies = []
    for s in movie_titles:
        s_ratio = difflib.SequenceMatcher(None, query, s).ratio()
        if s_ratio >= tolerance:
            similar_movies.append(s)
    return similar_movies

# Esempio di dati di input
my_genres = ['Thriller', 'Sci-Fi', 'Action']
qwerty = [
    ['Thriller', 'Sci-Fi', 'Drama'],
    ['Sci-Fi', 'Action', 'Comedy'],
    ['Action', 'Drama', 'Horror'],
    ['Thriller', 'Sci-Fi'],
    ['Action', 'Drama'],
    ['Sci-Fi', 'Romance'],
    ['Thriller', 'Drama'],
    ['Action', 'Comedy'],
    ['Thriller', 'Sci-Fi', 'Horror'],
    ['Thriller', 'Sci-Fi', 'Action']
]

# Funzione per calcolare il numero di stringhe in comune tra due liste di stringhe
def num_common_elements(list1, list2):
    return len(set(list1) & set(list2))

# Calcola il numero di stringhe in comune tra my_genres e ogni elemento di qwerty
common_counts = [[elem, num_common_elements(my_genres, elem)] for elem in qwerty]
print(common_counts)
# Ordina gli elementi di qwerty in base al numero di stringhe in comune (in ordine decrescente)
sorted_qwerty = sorted(common_counts, key=lambda x: x[1], reverse=True)

# Seleziona i primi 5 elementi dalla lista ordinata
top_5_elements = sorted_qwerty[:5]
print(top_5_elements)

# Stampa i risultati
print("I 5 elementi di qwerty con più stringhe in comune con my_genres sono:")
for elem, count in top_5_elements:
    print(elem, "- numero di stringhe in comune:", count)

import difflib

def trova_simili(stringa, lista_stringhe, soglia=0.6):
    """
    Trova le stringhe simili alla stringa data in una lista di stringhe.

    Args:
    - stringa (str): La stringa con l'errore.
    - lista_stringhe (list of str): La lista di stringhe da confrontare.
    - soglia (float): La soglia di similarità. Default è 0.6.

    Returns:
    - list of str: Le stringhe simili trovate.
    """
    simili = []
    for s in lista_stringhe:
        similarita = difflib.SequenceMatcher(None, stringa, s).ratio()
        if similarita >= soglia:
            simili.append(s)
    return simili

# Esempio di utilizzo
stringa_errore = "de last kutime"
lista_stringhe = ["The Last Kumite", "Inside Out", "Inside Out 2", "IF", "banana"]

print(trova_simili(stringa_errore, lista_stringhe))
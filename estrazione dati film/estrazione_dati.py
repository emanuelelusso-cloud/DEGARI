# Questo programma serve per estrarre dati dal sito TMDb, il quale contiene informazioni riguardanti film.
# Per poterlo utilizzare è necessario iscriversi alla piattaforma "https://www.themoviedb.org/" e generare una propria API key
# Dato che le descrizioni prese da TMDb risultano esigue, esse vengono integrate con le informazioni presenti su wikipedia

import json

import requests
import pandas as pd
import wikipedia
wikipedia.set_lang("it")

# Integrazione delle descrizioni con quelle prese da wikipedia in modo tale da avere più dati
def get_wikipedia_description(title):
    try:
        page = wikipedia.page(f"{title} (film)")

        # Se esiste la sezione della trama allora prende solo quella
        possible_sections = ["trama", "sinossi", "riassunto", "soggetto"]
        for section in page.sections:
            if any(p in section.lower() for p in possible_sections):
                return page.section(section)

        # Altrimenti ritorna tutte le voci, compreso di produttore, anno, etc
        return page.content       # Per dati più puliti mettere return None
    except:
        return None
#################################################
API_KEY = "" # <- inserisci qui la tua chiave api
#################################################

BASE_URL = "https://api.themoviedb.org/3"


params = {
    "api_key": API_KEY,
    "with_watch_providers": 8,         # Piattaforma: 35 RaiPlay, 8 netflix, 119 amazon prime, 337 disney+
    "watch_region": "IT",
    "language": "it-IT",
    "sort_by": "popularity.desc",      # Prende i film più popolari
    "page": 1
}

# Prendo la lista dei generi presenti
genre_response = requests.get(
    f"{BASE_URL}/genre/movie/list",
    params={"api_key": API_KEY, "language": "it-IT"}
)
genres_data = genre_response.json()["genres"]
# Associo a ogni id del genere il nome
genre_map = {g["id"]: g["name"] for g in genres_data}

all_results = []

for page in range(1, 10):  # Prende dalla prima pagina fino alla N-esima pagina
    params["page"] = page
    response = requests.get(f"{BASE_URL}/discover/movie", params=params)
    data = response.json()
    all_results.extend(data["results"])

custom_movies = []

# Tengo solo i campi che mi interessano
for movie in all_results:
    title = movie["title"]

    wiki_text = get_wikipedia_description(title)

    custom_movies.append({
        "name": title,
        "generi": [genre_map[g] for g in movie["genre_ids"]],
        "description": movie["overview"],
        "descrProgramma": wiki_text
    })

# Creo il file json
with open("film.json", "w", encoding="utf-8") as f:
    json.dump(custom_movies, f, ensure_ascii=False, indent=2)

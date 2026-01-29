# Questo programma legge le descrizioni delle opere d'arte da analizzare da un file JSON
#       e scrive per ogni artwork il suo prototipo.
#
# Per ogni artwork (es. quadro/video/serie tv) vengono analizzate tutte le istanze (es. episodi di una serie)
#       (es. il dipinto della Gioconda è l'unica istanza dell'artwork "La Gioconda")

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import treetaggerwrapper
import json
import os
from lib.json_field import *


#####################################################
#####################################################
#       FUNZIONI                                    #
#####################################################
#####################################################
def getLemma(word):
    tags = treetaggerwrapper.make_tags(tagger.tag_text(word))
    return tags[0].__getattribute__("lemma").split(":")[0]


def getTypeOfWord(word):
    tags = treetaggerwrapper.make_tags(tagger.tag_text(word))
    return tags[0].__getattribute__("pos").split(":")[0]


def isNumber(word):
    return getTypeOfWord(word) == "NUM"


def isVerb(word):
    return getTypeOfWord(word) == "VER"


def isAdjective(word):
    return getTypeOfWord(word) == "ADJ"


def isAdverb(word):
    return getTypeOfWord(word) == "ADV"


def insertArtworkInDict(instance, dict, identify, instDescr):
    arttwork = instance[identify]

    # Rimuovo caratteri non ammessi nella creazione di un file dal nome dell'artwork
    if isinstance(arttwork, list):
        for i in range(len(arttwork)):
            for char in chars_not_allowed_in_filename:
                arttwork[i] = arttwork[i].replace(char, "")
    else:
        for char in chars_not_allowed_in_filename:
            arttwork = arttwork.replace(char, "")

    description = ""
    for d in instDescr:
        description += " " + str(instance[d])
    word_tokens = word_tokenize(description)
    verbo = None

    # Inserisco le parole in dict
    for word in word_tokens:


        if "'" in word:  # se la parola e' ad esempio "d'autore", prendo solo "autore"
            word = word.split("'")[1]

        word = word.lower()

        if (len(word) > 1) and (word not in remove_words) and (not isNumber(word)) and (not isAdverb(word)):

            if isVerb(word):
                verbo = getLemma(word)
            else:
                word = getLemma(word)

                # Inserisco la parola in dict e/o aggiorno il conteggio della frequenza
                if isinstance(arttwork, list):
                    for i in range(len(arttwork)):
                        if arttwork[i] not in dict:
                            dict[arttwork[i]] = {}

                        if word not in dict[arttwork[i]]:
                            dict[arttwork[i]][word] = 0

                        dict[arttwork[i]][word] += 1
                        if verbo is not None:
                            if verbo not in dict[arttwork[i]]:
                                dict[arttwork[i]][verbo] = 0

                            dict[arttwork[i]][verbo] += 1
                            verbo = None

                else:
                    if arttwork not in dict:
                        dict[arttwork] = {}

                    if word not in dict[arttwork]:
                        dict[arttwork][word] = 0

                    dict[arttwork][word] += 1
                    if verbo is not None:
                        if verbo not in dict[arttwork]:
                            dict[arttwork][verbo] = 0

                        dict[arttwork][verbo] += 1
                        verbo = None


def compute_word_weights(data, artworks_output, top_n = 14):
    for artwork in data:
        top_words = dict(
            sorted(data[artwork].items(), key=lambda kv: kv[1], reverse=True)[:top_n]
        )
        # conto le parole totali dell'artwork
        totWords = sum(top_words.values())

        # Calcolo min e max delle medie
        minFreq = 1
        maxFreq = 0
        for count in top_words.values():
            freq = count / totWords
            minFreq = min(minFreq, freq)
            maxFreq = max(maxFreq, freq)


        rangeFreq = maxFreq - minFreq
        rangeScore = MAX_SCORE - MIN_SCORE
        lines = {}

        for word, count in top_words.items():
            freq = count / totWords

            score = MAX_SCORE
            if rangeFreq > 0:
                score = MIN_SCORE + (rangeScore * (freq - minFreq) / rangeFreq)

            lines[word] = score

        artworks_output[artwork] = lines

def writeInFile(file_name, instance):

    typical_path = os.path.join("typical", file_name)
    rigid_path = os.path.join("rigid", file_name)

    record = {"id": file_name}

    with open(typical_path, "w", encoding="utf-8")as file, open(rigid_path, "w", encoding="utf-8"), open(os.path.join(OUTPUT_DIR, '01_prototipi_resume.jsonl'), "a", encoding="utf-8") as resume:
        for word, value in instance.items():
            spaces = 20 - len(word) + 1
            stri = word + ":"
            for idx in range(spaces):
                stri = stri + " "

            stri = stri + str(value)
            file.write(stri + "\n")

            record[word] = value

        resume.write(json.dumps(record, ensure_ascii=False) + "\n")



def load_file(filename, dict, config):
    # carica tutte le istanze
    with open(filename, "r", encoding="utf-8") as file:
        instances = json.loads(file.read())

    # lista delle chiavi dei record
    keys = list(instances[0].keys())

    descriptions, config["identify"]  = acquire_json_fild(keys)

    # per ogni record salvo le parole e il numero di volte che si ripete
    for instance in instances:
        insertArtworkInDict(instance, dict, config["identify"], descriptions)

#####################################################
#####################################################
#       VAR GLOBALI                                 #
#####################################################
#####################################################
language = "it"

prepositions = ["di", "a", "da", "in", "su",
                "il", "del", "al", "dal", "nel", "sul",
                "lo", "dello", "allo", "dallo", "nello", "sullo",
                "la", "della", "alla", "dalla", "nella", "sulla",
                "l’", "dell’", "all’", "dall’", "nell’", "sull’",
                "i", "dei", "ai", "dai", "nei", "sui",
                "gli", "degli", "agli", "dagli", "negli", "sugli",
                "le", "delle", "alle", "dalle", "nelle", "sulle"]
articles = ["il", "lo", "la", "i", "gli", "le", "un", "un'", "uno", "una"]
congiuntions = ["a", "a meno che", "acciocché", "adunque", "affinché", "allora",
                "allorché", "allorquando", "altrimenti", "anche", "anco", "ancorché",
                "anzi", "anziché", "appena", "avvegna che", "avvegnaché", "avvegnadioché",
                "avvengaché", "avvengadioché", "benché", "bensi", "bensì", "che", "ché",
                "ciononostante", "comunque", "conciossiaché", "conciossiacosaché", "cosicché",
                "difatti", "donde", "dove", "dunque", "e", "ebbene", "ed", "embè", "eppure",
                "essendoché", "eziando", "fin", "finché", "frattanto", "giacché", "giafossecosaché",
                "imperocché", "infatti", "infine", "intanto", "invece", "laonde", "ma", "magari",
                "malgrado", "mentre", "neanche", "neppure", "no", "nonché", "nonostante", "né", "o",
                "ogniqualvolta", "onde", "oppure", "ora", "orbene", "ossia", "ove", "ovunque",
                "ovvero", "perché", "perciò", "pero", "perocché", "pertanto", "però", "poiché",
                "poscia", "purché", "pure", "qualora", "quando", "quindi", "se", "sebbene",
                "semmai", "senza", "seppure", "sia", "siccome", "solamente", "soltanto",
                "sì", "talché", "tuttavia"]
punctuation = list(string.punctuation) + ["...", "``"]
stop_words = stopwords.words('italian')  # le stop_words sono prese dalla libreria nltk (sono parole da non considerare)
remove_words = prepositions + articles + congiuntions + punctuation + stop_words  # tutte le parole da evitare
chars_not_allowed_in_filename = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

tagger = treetaggerwrapper.TreeTagger(TAGLANG=language)

encoding = "utf-8"
MIN_SCORE = 0.6
MAX_SCORE = 0.9

BASE_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(BASE_DIR, 'typical')

os.makedirs(OUTPUT_DIR, exist_ok=True)
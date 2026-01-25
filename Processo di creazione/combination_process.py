import glob
import os.path
import sys
from typing import Any, Dict

from prototyper import *
from clear import *
from Recommender import *

def run_prototyper():
    clear_properties()

    files = glob.glob('file_json/*.json')

    if len(files) == 1:
        # se è presente un solo file valido lo carica
        load_file(files[0], dict, config)
        compute_word_weights(dict, artworks_output)

    elif len(files) > 1:
        # in caso di più file, ti fa scegliere un file
        for i, f in enumerate(files):
            print(f"{i}: {f}")

        try:
            scelta = int(input('\nscegli il numero del file\n'))

            if 0 <= scelta < len(files):
                load_file(files[scelta], dict, config)
                compute_word_weights(dict, artworks_output)
                for i, key in enumerate(artworks_output):
                    if i == 10:
                        break
                    print(f"{key}: {artworks_output[key]}")

            else:
                print("Numero fuori range!")
                sys.exit(0)

        except ValueError:
            print("Devi inserire un numero valido")
            sys.exit(0)

    else:
        print("non sono presenti file .json nella cartella file_json")
        sys.exit(0)

    for artwork in artworks_output:
        writeInFile(artwork, artworks_output[artwork])


def run_recommender():
    if not artworks_output:
        files = glob.glob('typical/*')
        resume = os.path.join('typical', '01_prototipi_resume.jsonl')

        if resume in files:
            with open(resume, "r", encoding="utf-8") as file:
                for line in file:
                    data = json.loads(line)
                    artwork_id = data.pop("id")
                    artworks_output[artwork_id] = data

        elif len(files) > 0:
            for f in files:
                try:
                    lines = {}
                    record: Dict[str, Any] = {"id": os.path.basename(f)}

                    with open(f, "r", encoding="utf-8") as file, open(resume, "a", encoding="utf-8") as resume_file:
                        for line in file:
                            if ":" not in line:
                                continue

                            word, value = line.split(":", 1)
                            lines[word.strip()] = float(value.strip())
                            record[word.strip()] = float(value.strip())

                        artworks_output[os.path.basename(f)] = lines
                        resume_file.write(json.dumps(record, ensure_ascii=False) + "\n")

                except ValueError as e:
                    print(e)
        else:
            print("non sono presenti file nella cartella typical")


    category = None
    files = glob.glob('prototipi/*')

    if len(files) > 0:
        for i, f in enumerate(files[:10]):
            print(f"{i}: {f}")

        print("\nScegli una delle seguenti opzioni:")
        print("a) Inserisci un numero tra le opzioni consigliate")
        print("b) Inserisci un nome di un file presente in 'prototipi'")
        print("c) Inserisci una o più parole per la ricerca separandole con virgola")
    else:
        print("Inserisci una o più parole per la ricerca separandole con virgola")

    scelta = input("")

    valori = [v.strip() for v in scelta.split(",") if v.strip()]

    if len(valori) == 1 and all(v.isdigit() for v in valori):
        op = int(valori[0])

        if op < len(files):
            category = files[op].split("\\")[-1]
            print("hai scelto: ", category)
        else:
            print("opzione non valida")
            return

    elif len(valori) == 1 and os.path.isfile(os.path.join("prototipi", valori[0])):
        category = valori[0]

        print("hai scelto il file: ", category)



    else:
        print("hai scelto le parole: ", [v for v in valori])
        prop_list = []
        for word in valori:
            prop_list.append(tuple([word, '1']))

        elaboraGraduatoria(prop_list, artworks_output)
        return

    f = ReadAttributes(os.path.join("prototipi", category))
    r = [str(s) for s in f.result.split(',')]

    prop_list = []
    not_prop_list = []
    for p in f.attrs:
        if str(p).find('-') == -1:
            prop_list.append(p)
        else:
            not_prop_list.append(p[0].replace("-", "").strip())

    i = 0
    for p in f.tipical_attrs:
        if r[i].strip() == "'1'":
            prop_list.append(p)
        i += 1
    print(prop_list)
    print(not_prop_list)

    elaboraGraduatoria(prop_list, artworks_output, not_prop_list, category)


config = {
    "identify": None
}
dict = {}
artworks_output = {}

if __name__ == '__main__':
    print('\n0: exit\n1: creazione dei prototipi\n2: sistema di raccomandazione\n3: combinazione di concetti')
    scelta = int(input("\nscegli il numero relativo all'opzione\n"))

    while True:
        match scelta:
            case 0:
                sys.exit(0)
            case 1:
                run_prototyper()
                print('\n0: exit\n1: creazione dei prototipi\n2: sistema di raccomandazione\n3: combinazione di concetti')
                scelta = int(input("\ncontinuare con quale opzione\n"))

            case 2:
                run_recommender()
                print('\n0: exit\n1: creazione dei prototipi\n2: sistema di raccomandazione\n3: combinazione di concetti')
                scelta = int(input("\ncontinuare con quale opzione\n"))

            case _:
                print("\nscelta non valida\n")
                sys.exit(0)


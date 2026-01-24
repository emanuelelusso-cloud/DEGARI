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

    keys_list = list(artworks_output.keys())

    for i, key in enumerate(keys_list[:10]):
        print(f"{i}:  {key}: {artworks_output[key]}")

    print("\nScegli una delle seguenti opzioni:")
    print("a) Inserisci due numeri separati da virgola delle opzioni consigliate (es: 1,2)")
    print("b) Inserisci due nomi di file .txt presenti in 'typical' separati da virgola")
    print("c) Inserisci una o più parole per la ricerca separandole con virgola")

    scelta = input("")

    valori = [v.strip() for v in scelta.split(",") if v.strip()]

    if len(valori) == 2 and all(v.isdigit() for v in valori):
        op1 = int(valori[0])
        op2 = int(valori[1])

        if op1 < len(keys_list) and op2 < len(keys_list):

            print("hai scelto: ")
            print(f"{op1}: {keys_list[op1]}: {artworks_output[keys_list[op1]]}")
            print(f"{op2}: {keys_list[op2]}: {artworks_output[keys_list[op2]]}")



    elif len(valori) == 2 and all(os.path.isfile(os.path.join("typical", v)) for v in valori):
        file1, file2 = valori

        print("hai scelto i file: ", file1, file2)

    else:
        print("hai scelto le parole: ", [v for v in valori])
        prop_list = []
        for word in valori:
            prop_list.append(tuple([word, '1']))

        # Calcolo graduatoria nuova categoria
        elaboraGraduatoria(prop_list, artworks_output)






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
                print('\n0: exit\n2: sistema di raccomandazione\n3: combinazione di concetti')
                scelta = int(input("\ncontinuare con quale opzione\n"))
                if scelta == 1:
                    scelta = 4
            case 2:
                run_recommender()
                print('\n0: exit\n1: creazione dei prototipi\n3: combinazione di concetti')
                scelta = int(input("\ncontinuare con quale opzione\n"))
                if scelta == 2:
                    scelta = 4
            case _:
                print("\nscelta non valida\n")
                sys.exit(0)


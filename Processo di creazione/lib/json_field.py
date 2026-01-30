import glob
import json
import os
import sys
from typing import Dict, Any


def acquire_json_fild(keys):

    descriptions = None
    key_id = None
    # selezione della chiave da utilizzare come valore univoco di ogni record
    for i, f in enumerate(keys):
        print(f"{i}: {f}")

    try:
        scelta = int(input('\nscegli il numero del valore che identifica ogni record\n'))

        if 0 <= scelta < len(keys):
            key_id = keys[scelta]
        else:
            print("Numero fuori range!")
            sys.exit(0)

    except ValueError:
        print("Devi inserire un numero valido")
        sys.exit(0)

    # selezione delle chiavi che identificano le parole da parserizzare
    for i, f in enumerate(keys):
        print(f"{i}: {f}")

    try:
        scelta = input('\nscegli il/i numero/i del valore che identifica la descrizione dei record separati da ","\n')
        indici = [int(x.strip()) for x in scelta.split(",") if x.isdigit()]

        if any(i < 0 or i >= len(keys) for i in indici):
            print("Uno o più numeri fuori range!")
            sys.exit(0)

        descriptions = [keys[i] for i in indici]

    except ValueError:
        print("Devi inserire un numero valido")
        sys.exit(0)

    return descriptions, key_id


def create_artworks(artworks, path = "typical"):
    files = glob.glob(f'{path}/*')
    resume = os.path.join(path, '01_prototipi_resume.jsonl')

    if resume in files:
        with open(resume, "r", encoding="utf-8") as file:
            for line in file:
                data = json.loads(line)
                artwork_id = data.pop("id")
                artworks[artwork_id] = data

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

                    artworks[os.path.basename(f)] = lines
                    resume_file.write(json.dumps(record, ensure_ascii=False) + "\n")

            except ValueError as e:
                print(e)
    else:
        print("non sono presenti file nella cartella", path)
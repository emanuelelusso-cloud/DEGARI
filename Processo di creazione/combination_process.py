import glob
import sys

from prototyper import *

def load_file(filename):
    # carica tutte le istanze
    with open(filename, "r", encoding="utf-8") as file:
        instances = json.loads(file.read())

    # lista delle chiavi dei record
    keys = list(instances[0].keys())

    # selezione della chiave da utilizzare come valore univoco di ogni record
    for i, f in enumerate(keys):
        print(f"{i}: {f}")

    try:
        scelta = int(input('\nscegli il numero del valore che identifica ogni record\n'))

        if 0 <= scelta < len(keys):
            config["identify"] = keys[scelta]
        else:
            print("Numero fuori range!")
            return

    except ValueError:
        print("Devi inserire un numero valido")
        return

    # selezione delle chiavi che identificano le parole da parserizzare
    for i, f in enumerate(keys):
        print(f"{i}: {f}")

    try:
        scelta = input('\nscegli il/i numero/i del valore che identifica la descrizione dei record separati da ","\n')
        indici = [int(x.strip()) for x in scelta.split(",") if x.isdigit()]

        if any(i < 0 or i >= len(keys) for i in indici):
            print("Uno o più numeri fuori range!")
            return

        descriptions = [keys[i] for i in indici]

    except ValueError:
        print("Devi inserire un numero valido")
        return

    # per ogni record salvo le parole e il numero di volte che si ripete
    for instance in instances:
        insertArtworkInDict(instance, dict, config["identify"], descriptions)

config = {
    "identify": None
}
dict = {}
artworks_output = {}

if __name__ == '__main__':
    files = glob.glob('prototipi/*.json')

    if len(files) == 1:
        # se è presente un solo file valido lo carica
        load_file(files[0])
        compute_word_weights(dict, artworks_output)

    elif len(files) > 1:
        # in caso di più file, ti fa scegliere un file
        for i, f in enumerate(files):
            print(f"{i}: {f}")

        try:
            scelta = int(input('\nscegli il numero del file\n'))

            if 0 <= scelta < len(files):
                load_file(files[scelta])
                compute_word_weights(dict, artworks_output)
                for i, key in enumerate(artworks_output):
                    if i == 10:
                        break
                    print(f"{key}: {artworks_output[key]}")

                for artwork in artworks_output:
                    writeInFile(artwork, artworks_output[artwork])
            else:
                print("Numero fuori range!")
                sys.exit(0)

        except ValueError:
            print("Devi inserire un numero valido")
            sys.exit(0)

    else:
        print("non sono presenti file .json")
        sys.exit(0)


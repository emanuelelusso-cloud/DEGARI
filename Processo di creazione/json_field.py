import json
import sys


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

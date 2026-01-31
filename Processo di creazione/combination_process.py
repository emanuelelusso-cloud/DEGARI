import ast
import os.path

from lib.DataFromInput import *
from prototyper import *
from clear import *
from Recommender import *
from cocos import *
from cocos_preprocessing import *

def run_prototyper(folder = "typical"):

    if folder != config["old_folder"]:
        config["old_folder"] = folder

    dict.clear()
    artworks_output.clear()

    if folder != "typical":
        os.makedirs(folder, exist_ok=True)
        os.makedirs(folder + "_rigid", exist_ok=True)
    else:
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

        scelta = input('\nscegli il numero del file\n')

        if scelta.isdigit():
            op = int(scelta)

            if 0 <= op < len(files):
                load_file(files[op], dict, config)
                compute_word_weights(dict, artworks_output)

            else:
                print("Numero fuori range!")
                sys.exit(0)

        else:
            print("Devi inserire un numero valido")
            sys.exit(0)

    else:
        print("non sono presenti file .json nella cartella file_json")
        sys.exit(0)

    for artwork in artworks_output:
        writeInFile(artwork, artworks_output[artwork], folder)

    print("\nFile creati in: \n" + folder)


def run_recommender(folder = "typical"):

    if folder != config["old_folder"] or not artworks_output:
        artworks_output.clear()
        config["old_folder"] = folder
        create_artworks(artworks_output, folder)


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

    if len(valori) == 1 and valori[0].isdigit():
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
    r = ast.literal_eval(f.result)

    prop_list = []
    not_prop_list = []
    for p in f.attrs:
        if str(p).find('-') == -1:
            prop_list.append(p)
        else:
            not_prop_list.append(p[0].replace("-", "").strip())

    i = 0
    for p in f.tipical_attrs:
        if r[i] == 1:
            prop_list.append(p)
        i += 1
    print(prop_list)
    print(not_prop_list)

    elaboraGraduatoria(prop_list, artworks_output, not_prop_list, category)


def run_cocos(folder = "typical"):

    if config["old_folder"] != folder or not artworks_output:
        artworks_output.clear()
        config["old_folder"] = folder
        create_artworks(artworks_output, folder)

    files_prot = glob.glob('prototipi/*')

    if len(artworks_output) > 0 and len(files_prot) > 0:

        keys_list = list(artworks_output.keys())

        for i, key in enumerate(keys_list[:10]):
            print(f"{i}: {key}: {artworks_output[key]}")

        print("\na) scegli il numero corrispondente a due opzioni elencate da combinare, separate da virgola")
        print("b) scrivi il nome di due file presenti in typical, separati da virgola")
        print("c) scrivi il nome di un file presente in prototipi")
        print("d) scrivi 'combine_all' per combinare tutti i file presenti in typical")
        scelta = input("si può inserire il numero di attributi massimo che si vogliono tenere, separato da una virgola (es: file_di_prova,7)(es: file1,file2,7)\n")

        valori = [v.strip() for v in scelta.split(",") if v.strip()]

        run_cocos_preprocessing(valori, keys_list, folder)

    elif len(artworks_output) > 0:
        keys_list = list(artworks_output.keys())

        for i, key in enumerate(keys_list[:10]):
            print(f"{i}: {key}: {artworks_output[key]}")

        print("\na) scegli il numero corrispondente a due opzioni elencate da combinare, separate da virgola")
        print("b) scrivi il nome di due file presenti in typical, separati da virgola")
        print("c) scrivi 'combine_all' per combinare tutti i file presenti in typical")
        scelta = input("si può inserire il numero di attributi massimo che si vogliono tenere, separato da una virgola (es: file1,file2,7)\n")

        valori = [v.strip() for v in scelta.split(",") if v.strip()]

        run_cocos_preprocessing(valori, keys_list, folder)

    elif len(files_prot) > 0:

        for i, f in enumerate(files_prot[:10]):
            print(f"{i}: {f}")

        print("a) Scegli un numero relativo ai file elencati")
        print("b) Scrivi il nome di un file presente in prototipi")
        scelta = input("si può inserire il numero di attributi massimo che si vogliono tenere, separato da una virgola (es: file_di_prova,3)\n")

        valori = scelta.split(",")
        max_attrs = math.inf

        if valori[0].isdigit():
            if len(valori) == 2 and valori[1].isdigit():
                max_attrs = int(valori[1])

            op = int(scelta)
            cocos(files_prot[op], max_attrs)
        elif os.path.isfile(os.path.join("prototipi", scelta)):
            if len(valori) == 2 and valori[1].isdigit():
                max_attrs = int(valori[1])

            op = scelta
            cocos(op, max_attrs)
        else:
            print("Scelta non valida")
            return
    else:
        print("non sono presenti concetti da combinare\n")


def run_cocos_preprocessing(valori, keys_list, folder):
    max_attrs = math.inf
    if valori[0] == "combine_all":
        if len(valori) >= 2 and valori[1].isdigit():
            max_attrs = int(valori[1])

        for op1 in artworks_output.keys():
            for op2 in artworks_output.keys():
                if op1 != op2:
                    write_cocos_file(op1, artworks_output[op1], op2, artworks_output[op2], folder)
                    cocos(os.path.join("prototipi", f'{op1}_{op2}.txt'), max_attrs)

    elif len(valori) >= 2 and all(v.isdigit() for v in valori):
        op1 = int(valori[0])
        op2 = int(valori[1])

        if op1 < len(artworks_output) and op2 < len(artworks_output):
            if len(valori) >= 3 and valori[2].isdigit():
                max_attrs = int(valori[2])

            print("hai scelto i file: ", keys_list[op1], "and", keys_list[op2])

            write_cocos_file(keys_list[op1], artworks_output[keys_list[op1]], keys_list[op2], artworks_output[keys_list[op2]], folder)
            cocos(os.path.join("prototipi", f'{keys_list[op1]}_{keys_list[op2]}.txt'), max_attrs)
        else:
            print("Opzione non valida")
            return

    elif len(valori) >= 2 and all(val in artworks_output for val in valori):
        op1, op2 = valori

        print("hai scelto il file: ", op1, "and", op2)
        if len(valori) >= 3 and valori[2].isdigit():
            max_attrs = int(valori[2])

        write_cocos_file(op1, artworks_output[op1], op2, artworks_output[op2], folder)
        cocos(os.path.join("prototipi", f'{op1}_{op2}.txt'), max_attrs)


    elif os.path.isfile(os.path.join("prototipi", valori[0])):
        print("hai scelto il file: ", valori[0])
        if len(valori) >= 2 and valori[1].isdigit():
            max_attrs = int(valori[1])
        op = valori[0]
        cocos(os.path.join("prototipi", op), max_attrs)
    else:
        print("Scelta non valida\n")
        return



config = {
    "identify": None,
    "old_folder": "typical"
}
dict = {}
artworks_output = {}

if __name__ == '__main__':
    print('\n0: exit\n1: creazione dei prototipi\n2: sistema di raccomandazione\n3: combinazione di concetti\n(si può scegliere un folder separando le opzioni con ",". default typical)')
    scelta = input("scegli il numero relativo all'opzione\n")

    valori = scelta.split(",")
    if valori[0].isdigit():
        op = int(valori[0])
    else:
        print("Scelta non valida\n")
        sys.exit(0)

    while True:
        match op:
            case 0:
                sys.exit(0)
            case 1:
                if len(valori) >= 2:
                    run_prototyper(valori[1])
                else:
                    run_prototyper()
                print('\n0: exit\n1: creazione dei prototipi\n2: sistema di raccomandazione\n3: combinazione di concetti\n(si può scegliere un folder separando le opzioni con ",". default typical)')
                scelta = input("continuare con quale opzione?\n")
                valori = scelta.split(",")
                if valori[0].isdigit():
                    op = int(valori[0])
                else:
                    print("Scelta non valida\n")
                    sys.exit(0)

            case 2:
                if len(valori) >= 2:
                    if os.path.isdir(valori[1]):
                        run_recommender(valori[1])
                    else:
                        print("directory non esistente:", valori[1])
                else:
                    run_recommender()

                print('\n0: exit\n1: creazione dei prototipi\n2: sistema di raccomandazione\n3: combinazione di concetti\n(si può scegliere un folder separando le opzioni con ",". default typical)')
                scelta = input("continuare con quale opzione?\n")
                valori = scelta.split(",")
                if valori[0].isdigit():
                    op = int(valori[0])
                else:
                    print("Scelta non valida\n")
                    sys.exit(0)

            case 3:
                if len(valori) >= 2:
                    if os.path.isdir(valori[1]):
                        run_cocos(valori[1])
                    else:
                        print("directory non esistente:", valori[1])
                else:
                    run_cocos()

                print('\n0: exit\n1: creazione dei prototipi\n2: sistema di raccomandazione\n3: combinazione di concetti\n(si può scegliere un folder separando le opzioni con ",". default typical)')
                scelta = input("continuare con quale opzione?\n")
                valori = scelta.split(",")
                if valori[0].isdigit():
                    op = int(valori[0])
                else:
                    print("Scelta non valida\n")
                    sys.exit(0)

            case _:
                print("\nscelta non valida\n")
                sys.exit(0)


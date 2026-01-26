# Classificatore che restituisce tutte le istanze ordinate in base ad una graduatoria calcolata
# che rientrano nel nuovo genere fornito in input
import glob
import sys
import os
import json
from json_field import *
from DataFromInput import *


# Controlla se una parola(w) e' contenuta in una stringa(s)
def contains_word(s, w):
    return ((' ' + str(w) + ' ') in (' ' + str(s) + ' ')) or ((' ' + str(w) + ',') in (' ' + str(s) + ' '))


def contains_value(lista, w):
    for p in lista:
        if str(p[0]) == w:
            return True
    return False


# Calcola la graduatoria e riclassifica tutte le istanze offrendo la raccomandazione
def elaboraGraduatoria(prop_list, resume_properties, not_prop_list=[], category = None):
    print("\nRecommended artworks:\n\n")

    graduatoria = {}
    lista_istanze = []
    chars_not_allowed_in_filename = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

    sum = 0

    # Apertura json contenente le descrizioni delle opere
    # Calcolo graduatoria
    for instance_id, instance in resume_properties.items():
        sum = sum + 1
        for char in chars_not_allowed_in_filename:
            instance_id = instance_id.replace(char, "")
        instance_id = instance_id.replace("'", "_")
        if instance_id not in graduatoria:
            graduatoria[instance_id] = 0

            for prop in prop_list:
                prop_name = str(prop[0])

                if prop_name in instance:
                    graduatoria[instance_id] += 0.1

                    score = round(float(instance[prop_name]), 2)
                    graduatoria[instance_id] += score

    # Scorrimento istanze
    for instance_id, instance in resume_properties.items():

        # interseco per trovare quali parole sono presenti in prop_list e nell'istanza
        instance_keys = set(instance.keys())
        prop_keys = {str(p[0]) for p in prop_list}

        matches = list(instance_keys & prop_keys)

        # Se nell'istanza compare una proprietà negata, l'istanza viene scartata
        for prop in not_prop_list:
            if str(prop) in instance:
                matches = []
                graduatoria[instance_id] = 0
                break

        # Un'istanza è considerata se contiene almeno il 30% delle proprietà della lista
        if int(len(matches)) >= int(len(prop_list) * 30 / 100):
            lista_istanze.append([instance_id,
                                      "\n\t\\-> matches: " + str(matches)])
        else:
            graduatoria[instance_id] = 0

    # Graduatoria risultato
    i = 0
    # Scorrimento graduatoria ordinata per il punteggio degli artwork in modo decrescente
    for artwork, score in sorted(graduatoria.items(), key=lambda kv: kv[1], reverse=True):
        if score == 0:
            break
        print(artwork + "-" + str(score))

        for istanza in lista_istanze:
            if istanza[0] == artwork:
                i += 1
                print("\t" + istanza[0] + istanza[1] + "\n")

                f = open("recommendations.tsv", "a", encoding="utf-8", errors="replace")
                if category is not None:
                    f.write(istanza[0].replace("\t", " ") + "\t" + category + "\n")
                f.close()
    if i == 0:
        print("No recommendable contents for this category.")
    else:
        perc = (100 * i) / sum
        print("Classified " + str(i) + " of " + str(sum) + " contents (" + str(perc) + "%)")
        f = open("resume.tsv", "a", encoding="utf-8", errors="replace")
        if category is not None:
            f.write(category.replace("\t", " ") + "\t" + str(i) + "\n")
        f.close()

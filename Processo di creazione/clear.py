import os
import glob

prototipi = "prototipi"
typical = "typical"
rigid = "rigid"

def  clear_prototipi():
    for f in glob.glob(os.path.join(prototipi, "*")):
        if f.split("\\")[1] != "file_di_prova" and f.split("\\")[1] != "prova28attr.txt":
            os.remove(f)

def clear_properties():
    for t in glob.glob(os.path.join(typical, "*")):
        os.remove(t)

    for r in glob.glob(os.path.join(rigid, "*")):
        os.remove(r)

if __name__ == "__main__":
    scelta = int(input("\n0: pulizia prototipi + rigid + typical \n1: pulizia prototipi \n2: pulizia rigid + typical\n"))

    match scelta:
        case 0:
            clear_prototipi()
            clear_properties()

        case 1:
            clear_prototipi()

        case 2:
            clear_properties()
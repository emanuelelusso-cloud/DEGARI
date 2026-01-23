import os
import glob

prototipi = "prototipi"
typical = "typical"

def  clear_prototipi():
    for f in glob.glob(os.path.join(prototipi, "*")):
        os.remove(f)

def clear_properties():
    for f in glob.glob(os.path.join(typical, "*")):
        os.remove(f)

if __name__ == "__main__":
    clear_prototipi()
    clear_properties()
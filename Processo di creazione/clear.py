import os
import glob

folder = "output"

for f in glob.glob(os.path.join(folder, "*")):
    os.remove(f)
import os
import subprocess

for file in os.listdir('.'):
    if file.endswith(".xml.log"):
        subprocess.call(['./atclab-logtocsv.py', file])

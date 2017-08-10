import csv
import re

sample = """<hpc_elapsed_time>5259.91</hpc_elapsed_time><elapsed_time>5289</elapsed_time><view>experiment</view><event>mouse_move</event><x>23.6389</x><y>32.5</y></info>"""

def xycoords(logline):
    match = re.search("<x>(.*?)</x><y>(.*?)</y>", logline)
    return [match.group(1), match.group(2)]

def elapsed_time(logline):
    match = re.search("<elapsed_time>(.*?)</elapsed_time>", logline).group(1)
    return match

csvopen = open("coords.csv", "w+")
csvout = csv.writer(csvopen)

with open("Bullpup_3.xml.log", 'r+') as o:
    for line in o:
        if "mouse_move" in line:
            
            tmplist = xycoords(line)
            tmplist.append(elapsed_time(line))
            print(tmplist)
            csvout.writerow(tmplist)

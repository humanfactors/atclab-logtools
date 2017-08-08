import re
import csv
import click

partdatafile = open("participant1-grep.xml",'r')
partoutfile = open("participant1-out.csv", 'w+')
partoutcsv = csv.writer(partoutfile)


logregexdict = dict(trial = r"<atc:trial>(.+?)<\/atc:trial>",
                    button = r"<PushButton::LogEvent>([a-zA-Z]+)([0-9]{1,2})<\/PushButton::LogEvent>",
                    mstime = r"<hp_timer>(.+?)<\/hp_timer>",
                    timestamp = r"<time>(.+?)<\/time>",
                    taskid = r"<task_id>(.+?)</task_id>")

def parse_trialname(trialname):
    trialinfo = trialname.split("-")
    trialnumber = trialinfo[0]
    difficulty = re.search("(easy|hard)([\d]{1,2})",trialinfo[1]).group(1)
    npairs = re.search("(easy|hard)([\d]{1,2})",trialinfo[1]).group(2)
    return [trialname, trialnumber, difficulty, npairs]

def extract_values(line):
    trial = re.search(logregexdict['trial'],line).group(1)
    trialinfo = trial.split("-")
    trialnumber = trialinfo[0]
    difficulty = re.search("(easy|hard)([\d]{1,2})",trialinfo[1]).group(1)
    npairs = re.search("(easy|hard)([\d]{1,2})",trialinfo[1]).group(2)
    buttontype = re.search(logregexdict['button'],line).group(1)
    buttonpressed = re.search(logregexdict['button'],line).group(2)
    conflictlocation = re.search(r"([0-9]{1,2})",trialinfo[2]).group(1)
    mstime = re.search(logregexdict['mstime'],line).group(1)
    timestamp = re.search(logregexdict['timestamp'],line).group(1)
            'conflictlocation' : conflictlocation,
    return {'trial' : trial,
            'trialnumber' : trialnumber,
            'difficulty' : difficulty,
            'npairs' : npairs,
            'buttontype' : buttontype,
            'buttonpressed' : buttonpressed,
            'mstime' : mstime,
            'timestamp' : timestamp}

def extract_taskid(line):
    if "task_id" in line:
        return re.search(logregexdict['taskid'],line).group(1)

loaded_trials = []
responded_trials = []
responded_set = []
responded_set = set(responded_set)

for line in partdatafile:
    if "task_id" in line and "-C" in line:
        loaded_trials.append(extract_taskid(line))
    if "PushButton" in line:
        line_dict = extract_values(line)
        responded_trials.append([line_dict['trial'], line_dict['trialnumber'],
                         line_dict['difficulty'], line_dict['npairs'],
                         line_dict['buttontype'], line_dict['buttonpressed'],
                         line_dict['conflictlocation'], line_dict['timestamp'], line_dict['mstime']])
    if ">pb" in line:
        responded_set.append(line_dict['trial'])

partoutfile.seek(0)


partoutcsv.writerows(responded_trials)

for taskid in loaded_trials:
    if taskid not in responded_set:
        print(taskid)
        partoutcsv.writerow(parse_trialname(taskid))

partoutfile.close()
partdatafile.close()

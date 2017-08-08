#!/usr/bin/python3
import re
import os
import io
import csv
import subprocess
import click


loaded_trials = []
responded_trials = []
responded_set = []


@click.command()
@click.argument('input', type=click.Path(exists=True))
def main(input):
    global participantid
    participantid = re.search(r'(\d+)',click.format_filename(input)).group(1)
    print("Extracting participant %s" % (participantid))
    cleanedlogfile = grep_rawlog(click.format_filename(input))
    print("Grepping Done for participant %s" % (participantid))
    parse_logfile(cleanedlogfile)
    print("writing output")
    write_output(loaded_trials, responded_trials, participantid)
    print("Completed participant %s" % (participantid))

relogtags = dict(trial = r"<atc:trial>(.+?)<\/atc:trial>",
                    button = r"<PushButton::LogEvent>([a-zA-Z]+)([0-9]{1,2})<\/PushButton::LogEvent>",
                    mstime = r"<hp_timer>(.+?)<\/hp_timer>",
                    timestamp = r"<time>(.+?)<\/time>",
                    taskid = r"<task_id>(.+?)</task_id>")

def parse_trialname(trialname):
    trialinfo = trialname.split("-")
    trialnumber = trialinfo[0]
    difficulty = re.search("(easy|hard)([\d]{1,2})",trialinfo[1]).group(1)
    npairs = re.search("(easy|hard)([\d]{1,2})",trialinfo[1]).group(2)
    return [participantid, trialname, trialnumber, difficulty, npairs,"NA","NA","NA","NA","NA"]

# TODO: One reason this might be going so slow is for every single line it is
# creating these regular expression searches. Try and isolate these, ensure
# they are typed as strings... But there's something else slowing this down..

def extract_values(line):
    trial = re.search(relogtags['trial'],line).group(1)
    trialinfo = trial.split("-")
    trialnumber = trialinfo[0]
    return {'trial' : trial,
            'trialnumber' : trialnumber,
            'difficulty' : re.search("(easy|hard)([\d]{1,2})",trialinfo[1]).group(1),
            'npairs' : re.search("(easy|hard)([\d]{1,2})",trialinfo[1]).group(2),
            'conflictlocation' : re.search(r"([0-9]{1,2})",trialinfo[2]).group(1),
            'buttontype' : re.search(relogtags['button'],line).group(1),
            'buttonpressed' : re.search(relogtags['button'],line).group(2),
            'mstime' : re.search(relogtags['mstime'],line).group(1),
            'timestamp' : re.search(relogtags['timestamp'],line).group(1)}

def extract_taskid(line):
    if "task_id" in line:
        return re.search(relogtags['taskid'],line).group(1)

def grep_rawlog(rawlogfile):
    p = subprocess.Popen(['grep', "-e", "PushButton", '-e', 'task_id',  rawlogfile], stdout=subprocess.PIPE)
    return io.TextIOWrapper(p.stdout)

def parse_logfile(logfile):
    for line in logfile:
        if "task_id" in line and "-C" in line:
            loaded_trials.append(extract_taskid(line))
            continue
        if "PushButton" in line:
            line_dict = extract_values(line)
            responded_trials.append([participantid,
                                     line_dict['trial'],
                                     line_dict['trialnumber'],
                                     line_dict['difficulty'],
                                     line_dict['npairs'],
                                     line_dict['buttontype'],
                                     line_dict['buttonpressed'],
                                     line_dict['conflictlocation'],
                                     line_dict['timestamp'],
                                     line_dict['mstime']])
            if ">pb" in line:
                responded_set.append(line_dict['trial'])

def write_output(loaded_trials, responded_trials, participantid):
    with open("pid-%s.csv" % (participantid), 'w+') as partout:
        partoutcsv = csv.writer(partout)
        partoutcsv.writerows(responded_trials)
        for taskid in loaded_trials:
            if taskid not in responded_set:
                partoutcsv.writerow(parse_trialname(taskid))

if __name__ == __name__:
    main()

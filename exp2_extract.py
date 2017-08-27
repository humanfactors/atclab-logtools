#!/usr/bin/python3

#import csv
import re
import subprocess
import io
import click

# Variables
# Use returntimes to index truetiming output
returntimes_s = {"test1" : 147,
                   "test2" : 169,
                   "test3" : 122, 
                   "test4" : 123, 
                   "test5" : 175, 
                   "test6" : 123, 
                   "test7" : 150, 
                   "test8" : 118, 
                   "test9" : 160, 
                   "test10" : 150, 
                   "test11" : 171, 
                   "test12" : 147, 
                   "test13" : 133, 
                   "test14" : 138, 
                   "test15" : 171}

@click.command()
@click.argument('input', type=click.Path(exists=True))
def main(input):
    participantid = re.search(r'(Participant\d+)',click.format_filename(input)).group(1)
    cleanedlogfile = grep_conflicts(click.format_filename(input))
    truetimes = true_timing(cleanedlogfile)
    print(returntimes_ms(returntimes_s, truetimes))
    print(cleanedlogfile)

def grep_conflicts(rawlogfile):
    p = subprocess.Popen(['grep', 
                        "-e", "Interruption",
                        '-e', '<task_id>test',
                        '-e', 'level_variation',
                        "-e", "tick",
                        rawlogfile], stdout=subprocess.PIPE)
    return io.TextIOWrapper(p.stdout)

# def grep_timing(cleanedlog):
#     p = subprocess.Popen(['grep', "-e", "tick", '-e', '<task_id>test', cleanedlog], stdout=subprocess.PIPE)
#     return io.TextIOWrapper(p.stdout)
def returntimes_ms(returntimes_s, truetimes):
    ms_dict = dict()
    for key, value in returntimes_s.items():
        ms_dict[key] = truetimes[key][value]
    return ms_dict

def true_timing(logio):
    timingdict = dict()
    for line in logio:
        if "task_id>test" in line:
            test = re.search(r"<task_id>(test[0-9]{1,2})</task_id>", line).group(1)
            timingdict[test] = [0]
        if "tick" in line:
            time = re.search(r'<hpc_elapsed_time>(.+?)</hpc_elapsed_time>', line).group(1)
            timingdict[test].append(time)
    return timingdict

if __name__ == __name__:
    main()

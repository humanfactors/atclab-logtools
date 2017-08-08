import re
import timeit

test = """<time>Fri 4. Aug 09:14:25 2017</time><info><atc:trial>0-hard3-CA8-NA12-NB4</atc:trial><hp_timer>19560.9</hp_timer><PushButton::LogEvent>mpb3</PushButton::LogEvent><PushButton::Text>Reveal Aircraft Pair</PushButton::Text><PushButton::x>375</PushButton::x><PushButton::y>600</PushButton::y></info>"""

relogtags = dict(trial = r"<atc:trial>(.+?)<\/atc:trial>",
                    button = r"<PushButton::LogEvent>([a-zA-Z]+)([0-9]{1,2})<\/PushButton::LogEvent>",
                    mstime = r"<hp_timer>(.+?)<\/hp_timer>",
                    timestamp = r"<time>(.+?)<\/time>",
                    taskid = r"<task_id>(.+?)</task_id>")


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

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

wrapped = wrapper(extract_values, test)
print(timeit.timeit(wrapped, number = 1000))

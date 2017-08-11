import os
import io
import csv
import re
import click

class ATCXMLcsv(object):
    """Default class for ATC CSV. Requires a CSV on output"""
    def __init__(self, csvfile, measuretype):
        self.csvfile = csvfile
        self.validateMeasureType(measuretype)
        self.measuretype = measuretype

    def validateArgs(self, measuretype):
        if measuretype in ["accept", "handoff", "conflict", "pm"]:
            pass
        else:
            raise InvalidMeasure("Requested measure must be 'Accept' or 'Handoff")

    def grepHandAccept(self, csvfile, measuretype):
        p = subprocess.Popen(['grep', "-e", str(measuretype), csvfile], stdout=subprocess.PIPE)
        return io.TextIOWrapper(p.stdout)
    
    # Yanks a handoff or accept
    def yankHandAccept(self, csvfile):
        output = io.StringIO()
        with open(csvfile) as f:
            for line in f:
                if self.measuretype in line:
                    output.write(line)
                else:
                    continue
        return output.getvalue()
        
    def _measuretypematch(self,measuretype,line):
        if measuretype in line:
            return True

class InvalidMeasure(Exception):
    """Raise when measure type is not 'accept' or 'handoff'"""
    pass

# I should get this to do some magic to remove PM or nuisance aircraft
# PM could be defined as a regex?

@click.command()
@click.option('--measure', '-m', type = str)
@click.argument('csvfile' , type=click.Path(exists=True))
def main(csvfile, measure):
    filename = str(click.format_filename(csvfile))
    if not filename.endswith("csv"):
        raise IOError("Only accepts csv files")
    print("Parsing %s" % filename)
    ATCextraction = ATCXMLcsv(csvfile, measure)
    print(ATCextraction.yankMeasure(csvfile))

if __name__ == "__main__":
    main()
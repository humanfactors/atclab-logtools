import csv
import os
import unittest

class TestACList(unittest.TestCase):

    def testextractHandoffs(self):
        pass

    def testextractAccepts(self):
        pass
    
    def grepcsvFile(self, csvfile, dataobject):
        output = io.StringIO()
        with open(csvfile) as f:
            for line in f:
                if dataobjectmatch(line):
                    output.write(line)
                else:
                    continue

    def validateExtractType(self, requestedmeasure):
        if requestedmeasure in ["Accept", "Handoff", "Conflict"]:
            pass
        else:
            raise InvalidMeasure("Requested measure must be 'Accept' or 'Handoff")
    

class InvalidMeasure(Exception):
    """Raise when measure type is not 'Accept' or 'Handoff'"""
    pass
        
    def dataobject.match

        p = subprocess.Popen(['grep', "-e", str(dataobject), csvfile], stdout=subprocess.PIPE)
        return io.TextIOWrapper(p.stdout)


    def test_ac_list_unique(self):
        ac = ac_list.ACList()
        aclist = ac.get_ac_idx_list()
        uniq = list(set(aclist))
        self.assertEqual(len(uniq), len(aclist))

    def test_ac_list_error(self):
        ac = ac_list.ACList()
        for i in range(len(ac.get_ac_idx_list())):
            ac.pop_ac_idx()
        with self.assertRaises(ac_list.AircraftNameUnavailable):
            ac.pop_ac_idx()

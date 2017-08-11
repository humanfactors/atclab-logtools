#!/usr/bin/python3

import re
import unittest

if __name__ == '__main__':
    print("hello world")


class Conflict(object):
    """Performance data associated with an ATC conflict specified for complete dynamic scenarios."""
    def __init__(self):
        self.value = "hello"
        self.other_value = "bonjour"
        self.constant_value = 42

    def conflictPair(aircraft1, aircraft2):
        pass

    def seperationViolation(pair):
        pass

class InvalidConflict(Exception):
    """Custom error class when the specified conflict is invalid"""
    pass

class DeferredHandoff(object):
    """A deferred handoff object"""
    def __init__(self):
        pass

   def gather_pm_values(self, pminput):
        '''Gathers the PM info specified in PM csv as two lists, for short and long retrieve conditions.'''
        with open(self.pminput, 'r+') as o:
            # Some kind of dict object
            pmdetails = pd.read_csv(o)
            self.pmdetailslong = pmdetails[0:16]
            self.pmdetailsshort = pmdetails[16:32]
        return None

    def _DeferredHandoffAircraft(self, callsign, trial, pmkey, condition):
        return dict("callsign" = callsign, "trial" = trial, "pmkey" = pmkey, "condition" = condition)


class InvalidHandoff(Exception):
    """Custom error class when the specified conflict is invalid"""
    print("Invalid Handoff. Please consult the specification or email Michael")
    pass

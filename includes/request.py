"""
    Python included Classes that helps to work with django requests object
"""
import re
from re import match
from typing import Dict

class POST(dict):
    """
        POST request object that extends the python's native list object
    """
    def getlist(self,var:str) ->list:
        """
            Get list of array sent from a request
        """
        var_array = []
        last_index = None
        count = 0
        for key in self:
            if re.match(rf"{re.escape(var)}\[[0-9]+\]$",key):
                var_array.append(self[key])
            match_re = re.match(rf"{re.escape(var)}\[(?P<index>[0-9]+)\]\[(?P<option_key>[a-zA-Z0-9_]+)\]",key)
            if match_re:
                try:
                    var_array[int(match_re.group('index'))][match_re.group('option_key')] = self[key]
                except IndexError as e:
                    var_array.insert(int(match_re.group('index')),{})
                    var_array[int(match_re.group('index'))][match_re.group('option_key')] = self[key]
        return var_array
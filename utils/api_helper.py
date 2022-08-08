import re
from includes.request import POST

"""
    API helper for view classes and methods
"""

""" API Response Maker """
def response_maker(response_type='success',message=None,count=None,data=None):
    response = dict({'response_type':'Success','message':message,'count':count,'data':data})
    if response_type == 'error':
        response = dict({'response_type':'Error','message':message,'data':data})

    if not message:
        response.pop('message',None)

    if data is None:
        response.pop('data',None)

    if not count:
         response.pop('count',None)

    return response

""" A function decorator to normalize request POST or GET data"""
def request_data_normalizer(func):

    def wrapper(request, **Kwargs):
        #Serialize POST data
        new_data = {}
        try:
            data = request.POST
            if isinstance(data, (dict)):
                for key, value in data.items():
                    if isinstance(value, (list)):
                        new_data[key] = value[0]
                    elif isinstance(value, (str)):
                        new_data[key] = value
                    else:
                        pass
            elif isinstance(data, (list)):
                new_data = []
                for index, row in data:
                    new_data[index] = {}
                    if isinstance(row, (dict)):
                        for key, value in row.items():
                            if isinstance(value, (list)):
                                new_data[index][key] = value[0]
                            elif isinstance(value, (str)):
                                new_data[index][key] = value
                            else:
                                pass
                    else:
                        pass
            request._POST = POST(new_data)
        except Exception as e:
            raise(str(e))
        #Do for GET
        try:
            data = request.GET
            if isinstance(data, (dict)):
                for key, value in data.items():
                    if isinstance(value, (list)):
                        new_data[key] = value[0]
                    elif isinstance(value, (str)):
                        new_data[key] = value
                    else:
                        pass
            elif isinstance(data, (list)):
                new_data = []
                for index, row in data:
                    new_data[index] = {}
                    if isinstance(row, (dict)):
                        for key, value in row.items():
                            if isinstance(value, (list)):
                                new_data[index][key] = value[0]
                            elif isinstance(value, (str)):
                                new_data[index][key] = value
                            else:
                                pass
                    else:
                        pass
            request._GET = new_data
        except Exception as e:
            raise(str(e))
        return func(request, **Kwargs)
    return wrapper
            
"""
    Get list of array sent from a request
"""
def getlistWrapper(data):
    def getlist(var):
        var_array = []
        for key in data:
            if re.match(rf"{re.escape(var)}\[[0-9]+\]",key):
                var_array.append(data[key])
        return var_array
    return getlist
from collections import defaultdict

class Request:
    def __init__(self, environ):
        self.queries = defaultdict()
        for key, val in environ.items():

            setattr(self, key.replace(".", "_").lower(), val)
            
        if self.query_string:
            req_quires = self.query_string.split("&")
            for query in req_quires:
                query_key , query_val = query.split("=")
                
                self.queries[query_key] = query_val

import inspect
import types
from typing import Any
from request import Request
from parse import *

from response import Response

SUPPORTED_METHODS = {"GET", "POST", "DELETE"}

class SlowAPI:
    def __init__(self, middlewares) -> None:
        
        self.routes = dict()
        self.middlewares = middlewares
        self.routes_middlewares = dict()
    
    
    def __call__(self, environ, start_response) -> Any:
        response = Response()
        request = Request(environ)
        print(environ)
        
        
        
        
        for middleware in self.middlewares:
            if isinstance(middleware, types.FunctionType):
                middleware(request)
            else:
                raise TypeError("You can only pass functions")
        
        for path, handler_dict in self.routes.items():
            
            res = parse(path, request.path_info)
            
            for request_method, handler in handler_dict.items():
                if request.request_method == request_method and res is not None:
                    
                    middleware_list = self.routes_middlewares[path][request_method]
                    
                    for mw in middleware_list:
                        if isinstance(mw, types.FunctionType):
                            mw(request)
                        else:
                            raise TypeError("You can only pass functions")
                    
                    handler(request, response, **res.named)
                    return response.as_wsgi(start_response)
                    
        return response.as_wsgi(start_response)
        
                
    def route_common(self, path, handler, method_name, middlewares=[]):
        
        # {
        #     "/users":{
        #         "GET":handler,
        #        "POST":handler2
        #     }
        # }
            
        path_name = path or "/"
        if path_name not in self.routes:
            self.routes[path_name] = {}
            
            
        
        self.routes[path_name][method_name] = handler   

        if path_name not in self.routes_middlewares:
            self.routes_middlewares[path_name] = {}
        self.routes_middlewares[path_name][method_name] = middlewares
        
        # {
        #     "/users/{id}":{
        #         "GET":[fn1, fn2],
        #         "POST":[fn3, fn4]
        #     }
        # }
        
        
        return handler

    def get(self, path=None, middlewares=[]):
        def wrapper(handler):
            return self.route_common(path, handler, "GET", middlewares)       
        return wrapper
    
    def post(self, path=None, middlewares=[]):
        def wrapper(handler):
            return self.route_common(path, handler, "POST",middlewares)
        return wrapper
    
    def delete(self, path=None, middlewares=[]):
        def wrapper(handler):
            return self.route_common(path, handler, "DELETE", middlewares)
        return wrapper
    
    def route(self, path=None, middlewares=[]):
        def wrapper(handler):
            if isinstance(handler, type):
                
                class_members = inspect.getmembers(handler, lambda x: inspect.isfunction(x) and not (
                    x.__name__.startswith("__") and x.__name__.endswith("__")
                ) and x.__name__.upper() in SUPPORTED_METHODS)
                
                print(class_members)
                
                for fn_name , fn_handler in class_members:
                    self.route_common(path or f"/{handler.__name__}", fn_handler, fn_name.upper())
                    
                    
                
                
            else:
                raise ValueError("only class is accepted")
        return wrapper
            




# Python Backend Framework

A minimal backend framework for Python, inspired by WSGI and designed for simplicity and extensibility.

## Overview
This project aims to build a simple, lightweight backend framework for Python web applications. It provides basic request and response handling, and is designed to be easy to understand, extend, and use for learning or small projects.

### Features Implemented
- **Request and Response Handling:** Core classes for HTTP request and response abstraction (`request.py`, `response.py`).
- **WSGI Compatibility:** The framework is designed to work with any WSGI-compliant server (e.g., Gunicorn, uWSGI, waitress).
- **Basic Routing:** Example usage in `example.py` demonstrates how to handle routes and responses.

- **Add routing and middleware support**

- **Added support for static files and templates**

### Example Usage
See `example.py` for a simple demonstration:

```python


# Simulate a WSGI app

from werkzeug.serving import run_simple
from main import SlowAPI

def global_middleware(request):
    print("This will run first before any request.")
    
    
def local_middleware(request):
    """middlewares for specific routes"""
    print("This middleware will be executed before a route function execute")
    print(request)

app = SlowAPI(middlewares=[global_middleware])

@app.get()
def hello(req, res):
    res.send("server working")

@app.get("/users/{id}", middlewares=[local_middleware])
def get_users(req, res, id):
    res.send(f"hello user {id}", 200)
    
@app.get("/users", middlewares=[local_middleware])
def get_users(req, res):
    res.render("index", context={"message":"Hello Users"})
    

run_simple("127.0.0.1",8080, app, use_reloader=True, use_debugger=True)
```

To run with a WSGI server (e.g., waitress, werkzeug(for auto reloading)):
```bash
pip install waitress werkzeug
python example.py
```

## How to Use
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd Python-Backend-Framework
   ```
2. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```
3. Run the example:
   ```bash
   python example.py
   ```
4. Integrate with a WSGI server for production use.

## Project Structure
- `main.py` - Entry point for the framework (future expansion)
- `request.py` - Request abstraction
- `response.py` - Response abstraction
- `example.py` - Example usage
- `index.html` - Static file example

## Future Plans
- Provide Body data acceptance (till now only queries and path is handled)
- Provide more examples and documentation


## Goal
The clear goal is to build a simple backend framework for Python that is easy to use, understand, and extend. It should serve as a learning tool and a foundation for small web projects.

## WSGI and Server
This framework is WSGI-compatible, meaning it can run on any WSGI server. WSGI (Web Server Gateway Interface) is a standard interface between web servers and Python web applications. By following WSGI, your app can be deployed using popular servers like Gunicorn, uWSGI, or waitress.



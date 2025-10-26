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
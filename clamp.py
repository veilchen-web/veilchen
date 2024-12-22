from veilchen import Veilchen as Bottle

from veilchen import Route
from functools import cached_property



app = Bottle()

@app.route("/foo")
def foo():
    return "Hello from /foo"

@app.route("/foo/:name")
def foo_name(name):
    return f"Hello, {name}!"

@app.route("/bar/baz", method="POST")
def bar_baz():
    return "POST to /bar/baz"

# Access the routes
print("Routes (first access):", app.router.routes)
print("Routes (cached access):", app.router.routes)

# Add a new route
@app.route("/new/route")
def new_route():
    return "New Route"

@app.route("/json")
def new_route():
    return {"222":"1111"}

# Access routes again (cache invalidated)
print("Routes (after adding a route):", app.router.routes)


from veilchen import run

run(app)

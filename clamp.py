from bottle import Veilchen as Bottle

from bottle import Route
from functools import cached_property
import urllib.parse


class TrieNode:
    def __init__(self, path="/", method="GET"):
        self.path = path  # Full path for this node
        self.method = method  # HTTP method for this node
        self.callback = None  # Function to call for this route
        self.is_dynamic = False  # Whether this node represents a dynamic segment
        self.children = {}  # Child nodes in the Trie
        self.rule = path  # Rule or name for dynamic segment, e.g., ":name"

    def __repr__(self):
        return f"TrieNode(path={self.path}, method={self.method}, callback={self.callback})"

class TrieRouter:
    def __init__(self, app=None):
        self.root = TrieNode(path="/")
        self.app = app  # Reference to the application instance

    @cached_property
    def routes(self):
        """Dynamically collect all routes by traversing the Trie."""
        collected_routes = []

        def collect_routes(node):
            if node.callback:
                if not callable(node.callback):
                    raise TypeError(
                        f"Callback for route {node.path} is not callable: {node.callback}"
                    )
                collected_routes.append(
                    Route(self.app, node.path, node.method, node.callback)
                )
            for child in node.children.values():
                collect_routes(child)

        collect_routes(self.root)
        return collected_routes

    def add(self, rule, method="GET", callback=None, name=None, **config):
        if callback is None:
            raise ValueError("A callback function must be provided for a route.")
        if isinstance(callback, Route):
            callback_function = callback.callback
        else:
            callback_function = callback
        if not callable(callback_function):
            raise TypeError(f"Provided callback is not callable: {callback_function}")
        parts = self._split_path(rule)
        current_node = self.root
        current_path = ""

        for part in parts:
            is_dynamic = part.startswith(":")
            key = ":" if is_dynamic else part
            if key not in current_node.children:
                child_path = f"{current_path}/{part}" if current_path else f"/{part}"
                current_node.children[key] = TrieNode(path=child_path, method=method)
                if is_dynamic:
                    current_node.children[key].is_dynamic = True
            current_node = current_node.children[key]
            current_path = current_node.path

        current_node.callback = callback_function
        if "routes" in self.__dict__:
            del self.__dict__["routes"]

    def match(self, environ):
        full_path = environ["PATH_INFO"]
        method = environ["REQUEST_METHOD"]
        query_string = environ.get("QUERY_STRING", "")
        parts = self._split_path(full_path)
        current_node = self.root
        path_params = {}

        for part in parts:
            if part in current_node.children:
                current_node = current_node.children[part]
            elif ":" in current_node.children:
                dynamic_key = current_node.children[":"].rule.split("/")[-1][1:]
                current_node = current_node.children[":"]
                path_params[dynamic_key] = part
            else:
                raise ValueError(f"No route matches path: {full_path}")

        if current_node.method != method:
            raise ValueError(
                f"Method not allowed for path {full_path}. Expected {current_node.method}."
            )

        if not current_node.callback:
            raise ValueError(f"No handler found for path: {full_path}")

        query_params = self._parse_query_string(query_string)
        combined_params = {**path_params, **query_params}

        # Return the Route object instead of the raw callback
        route = Route(self.app, current_node.path, current_node.method, current_node.callback)
        return route, combined_params

    def _split_path(self, path):
        return [part for part in path.strip("/").split("/") if part]

    def _parse_query_string(self, query_string):
        return dict(urllib.parse.parse_qsl(query_string))

    def print_trie(self, node=None, depth=0):
        if node is None:
            node = self.root
        indent = "  " * depth
        handler_name = node.callback.__name__ if callable(node.callback) else None
        print(f"{indent}{node.path} (Method: {node.method}, Handler: {handler_name})")
        for child in node.children.values():
            self.print_trie(child, depth + 1)


class CustomBottle(Bottle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.router
        self.router = TrieRouter(self)  # Pass the app instance to TrieRouter


app = CustomBottle()

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

# Introduction to Pyodide - Python for WASM

## Getting Starting
Install the required dependencies: <br>
```pip install -r requirements.txt```

Run the application using Flask: <br>
```
flask --app .\app.py --debug run
```

Navigate to the URL the server recommends (some cli let you ctrl+click on the URL to launch it in a browser). The url should be something like:

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)


## Other Resources
- See the [Pyodide site](https://pyodide.org/en/stable/) for other ways of running Python using WASM
- Note, not all modules are available - however almost every module with a PyPy version is available. For more details [see here](https://pyodide.org/en/stable/usage/wasm-constraints.html)

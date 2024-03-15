"""
Demo by MoCo Makers

License:  MIT License
"""

import js
from pyodide.code import run_js 

div = js.document.getElementById("main-area")
div.innerHTML = "<h1>This element was created from Python</h1>"

js_script = """
let mydiv_again = document.getElementById("main-area");
mydiv_again.innerHTML = "<h1>This element has been changed with JS called in PY!</h2>";
"""

run_js(js_script)